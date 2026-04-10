# 聊天流式接口（MVP 版）
# 作用：接收请求 -> 调用 LangGraph -> 落库 -> SSE 返回

import asyncio
import json

from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.agent.graph import run_agent
from app.agent.session_store import add_chat_message, get_or_create_chat_session
from app.database import get_async_session
from app.schemas import ChatRequest

# OpenAPI 分组标签
router = APIRouter(tags=["chat"])


def split_for_stream(text: str, step: int = 14) -> list[str]:
    # 防御：空文本直接返回空列表
    if not text:
        return []

    # 按固定长度切片，模拟 token 流式输出
    return [text[i : i + step] for i in range(0, len(text), step)]


@router.post("/stream")
async def chat_stream(
    payload: ChatRequest,
    db: AsyncSession = Depends(get_async_session),
):
    # 1) 先跑编排图，拿最终回答
    result = run_agent(payload)
    answer = result.get("final_answer", "(空回答)")

    # 2) 把会话和消息写入数据库
    try:
        # 保证会话存在（有则复用，无则创建）
        chat_session = await get_or_create_chat_session(
            db=db,
            session_id=payload.session_id,
            user_id=payload.user_id,
        )

        # 存用户消息
        await add_chat_message(
            db=db,
            chat_session_id=chat_session.id,
            role="user",
            content=payload.message,
        )

        # 存模型消息（这里先存完整答案）
        await add_chat_message(
            db=db,
            chat_session_id=chat_session.id,
            role="assistant",
            content=answer,
        )

        # 提交事务
        await db.commit()
    except Exception:
        # 出错回滚，防止脏数据
        await db.rollback()
        raise

    # 3) SSE 流式返回给前端
    chunks = split_for_stream(answer, 14)

    async def event_generator():
        # 流开始事件
        yield (
            "event: start\ndata: "
            + json.dumps({"session_id": payload.session_id}, ensure_ascii=False)
            + "\n\n"
        )

        # 逐片返回 delta
        for part in chunks:
            await asyncio.sleep(0.05)
            yield (
                "event: message\ndata: "
                + json.dumps({"delta": part}, ensure_ascii=False)
                + "\n\n"
            )

        # 流结束事件
        yield "event: done\ndata: " + json.dumps({"finish_reason": "stop"}) + "\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
