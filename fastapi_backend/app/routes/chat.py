# 聊天流式接口（MVP）
# 作用：接收请求 -> 可选检索 -> LangGraph 编排 -> 落库 -> SSE 返回

# 导入异步 sleep。
import asyncio
# 导入 JSON 编解码。
import json

# 导入 FastAPI 路由与依赖注入。
from fastapi import APIRouter, Depends
# 导入 SSE 响应类型。
from fastapi.responses import StreamingResponse
# 导入异步数据库会话类型。
from sqlalchemy.ext.asyncio import AsyncSession

# 导入 LangGraph 执行入口。
from app.agent.graph import run_agent
# 导入会话/消息落库方法。
from app.agent.session_store import add_chat_message, get_or_create_chat_session
# 导入数据库 session 依赖。
from app.database import get_async_session
# 导入检索服务。
from app.retrieval.service import search_chunks_by_keyword
# 导入请求体模型。
from app.schemas import ChatRequest

# 定义路由对象（main.py 会从这里 import router）。
router = APIRouter(tags=["chat"])


# 把完整答案切成小片，模拟流式输出。
def split_for_stream(text: str, step: int = 14) -> list[str]:
    # 空文本返回空列表。
    if not text:
        return []
    # 按步长切片。
    return [text[i : i + step] for i in range(0, len(text), step)]


# 简单规则：判断是否应触发检索
def should_retrieve(message: str) -> bool:
    # 统一小写并去空白
    m = (message or "").strip().lower()

    # 空消息直接不检索
    if not m:
        return False

    # 文档/规则类关键词（原有）
    doc_keywords = ["规则", "流程", "文档", "faq", "sop", "说明", "政策", "手册"]

    # 业务规则类关键词（新增）
    biz_keywords = ["退款", "退货", "售后", "费用", "时效", "限制", "条件", "是否", "能否", "可以"]

    # 只要命中任一关键词就走检索
    return any(k in m for k in (doc_keywords + biz_keywords))



@router.post("/stream")
async def chat_stream(
    # 聊天请求体。
    payload: ChatRequest,
    # 注入数据库会话。
    db: AsyncSession = Depends(get_async_session),
):
    # 初始化检索结果。
    retrieved_docs: list[dict] = []

    # 如果命中检索规则，先检索证据片段。
    if should_retrieve(payload.message):
        retrieved_docs = await search_chunks_by_keyword(
            db=db,
            query=payload.message,
            limit=5,
        )

    # 运行 LangGraph，把检索结果喂进去。
    result = run_agent(payload, retrieved_docs=retrieved_docs)

    # 提取最终回答文本。
    answer = result.get("final_answer", "(空回答)")

    # 落库：会话 + 用户消息 + 助手消息。
    try:
        # 查或建会话。
        chat_session = await get_or_create_chat_session(
            db=db,
            session_id=payload.session_id,
            user_id=payload.user_id,
        )

        # 保存用户消息。
        await add_chat_message(
            db=db,
            chat_session_id=chat_session.id,
            role="user",
            content=payload.message,
        )

        # 保存助手消息。
        await add_chat_message(
            db=db,
            chat_session_id=chat_session.id,
            role="assistant",
            content=answer,
        )

        # 提交事务。
        await db.commit()
    except Exception:
        # 出错回滚。
        await db.rollback()
        raise

    # 切片用于 SSE。
    chunks = split_for_stream(answer, 14)

    # SSE 事件生成器。
    async def event_generator():
        # 发送开始事件。
        yield (
            "event: start\ndata: "
            + json.dumps({"session_id": payload.session_id}, ensure_ascii=False)
            + "\n\n"
        )

        # 发送 message 事件（delta）。
        for part in chunks:
            await asyncio.sleep(0.05)
            yield (
                "event: message\ndata: "
                + json.dumps({"delta": part}, ensure_ascii=False)
                + "\n\n"
            )

        # 发送结束事件。
        yield "event: done\ndata: " + json.dumps({"finish_reason": "stop"}) + "\n\n"

    # 返回 SSE 响应。
    return StreamingResponse(event_generator(), media_type="text/event-stream")
