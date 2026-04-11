# LangGraph 编排（MVP）
# 当前支持三条分支：
# 1) DIRECT：通用直答
# 2) EXPLAIN_PAGE：页面解释
# 3) RETRIEVE：知识检索回答（RAG MVP）

# 导入类型定义工具。
from typing import Any, TypedDict

# 导入 LangGraph 构图对象和结束节点常量。
from langgraph.graph import END, StateGraph

# 导入请求模型（用于构造初始状态）。
from app.schemas import ChatRequest


# 定义状态结构（图中节点共享这一份状态）。
class AgentState(TypedDict, total=False):
    # 用户 ID。
    user_id: str
    # 会话 ID。
    session_id: str
    # 用户问题。
    message: str
    # 页面上下文。
    page_context: dict[str, Any]
    # 路由结果：DIRECT / EXPLAIN_PAGE / RETRIEVE。
    route: str
    # 检索到的文档片段。
    retrieved_docs: list[dict[str, Any]]
    # 最终回答。
    final_answer: str


# 构建上下文节点（MVP 先保留空实现）。
def build_context(state: AgentState) -> AgentState:
    return {}


# 路由决策节点（MVP 规则版）。
def decide_route(state: AgentState) -> AgentState:
    # 取问题文本。
    message = str(state.get("message") or "").lower()

    # 取页面上下文。
    page_context = state.get("page_context", {})
    page_title = str(page_context.get("page_title") or "").strip()
    module_name = str(page_context.get("module_name") or "").strip()
    page_url = str(page_context.get("page_url") or "").strip()
    visible_summary = str(page_context.get("visible_text_summary") or "").strip()

    # 是否存在页面上下文。
    has_page_context = bool(page_title or module_name or page_url or visible_summary)

    # 简单检索触发词（MVP 规则，可后续替换为 LLM 路由）。
    retrieve_keywords = [
        "规则", "流程", "文档", "faq", "sop", "说明", "政策", "手册",
        "退款", "退货", "售后", "费用", "时效", "限制", "条件", "是否", "能否", "可以"
    ]


    # 如果问题里包含检索触发词，优先走 RETRIEVE。
    if any(k in message for k in retrieve_keywords):
        return {"route": "RETRIEVE"}

    # 否则有页面上下文时走 EXPLAIN_PAGE。
    if has_page_context:
        return {"route": "EXPLAIN_PAGE"}

    # 其余走 DIRECT。
    return {"route": "DIRECT"}


# DIRECT 节点：直答。
def direct_answer(state: AgentState) -> AgentState:
    return {
        "final_answer": f"你问的是：{state.get('message', '')}。这是 DIRECT 路径（MVP）。"
    }


# EXPLAIN_PAGE 节点：页面解释。
def explain_page(state: AgentState) -> AgentState:
    # 取页面上下文。
    page_context = state.get("page_context", {})
    page_title = str(page_context.get("page_title") or "").strip()
    module_name = str(page_context.get("module_name") or "").strip()
    visible_summary = str(page_context.get("visible_text_summary") or "").strip()

    # 摘要预览。
    preview = visible_summary[:160] if visible_summary else "（页面摘要为空）"

    # 组装页面解释回答。
    return {
        "final_answer": (
            f"你问的是：{state.get('message', '')}。"
            f"我基于当前页面「{page_title or module_name or '未命名页面'}」回答。"
            f"页面摘要：{preview}。这是 EXPLAIN_PAGE 路径（MVP）。"
        )
    }


# RETRIEVE 节点：这里先占位（真正检索在 route 层异步执行）。
def retrieve_knowledge(state: AgentState) -> AgentState:
    # 保持状态不变，检索由外层异步流程处理。
    return {}


# 基于检索证据生成回答（调试增强版：显示命中来源）
def answer_with_retrieval(state: AgentState) -> AgentState:
    # 取检索结果
    docs = state.get("retrieved_docs") or []

    # 没命中时兜底
    if not docs:
        return {
            "final_answer": (
                "我尝试检索知识库，但暂未找到匹配内容。"
                "你可以换个问法，或先确认文档是否已入库。"
            )
        }

    # 取前 3 条证据
    top_docs = docs[:3]

    # 每条证据展示行
    evidence_lines: list[str] = []
    # 汇总命中来源（用于总览）
    source_set: set[str] = set()

    # 逐条组装
    for d in top_docs:
        # 元数据
        metadata = d.get("metadata") or {}

        # 兼容两种来源字段：
        # 1) 融合检索后的 sources（如 ["vector", "fts"]）
        # 2) 单路 match_type（如 "ilike"）
        sources = metadata.get("sources") or []
        if not sources:
            mt = metadata.get("match_type")
            if mt:
                sources = [mt]

        # 最终兜底
        if not sources:
            sources = ["unknown"]

        # 汇总来源
        for s in sources:
            source_set.add(str(s))

        # 分数（融合分）
        score = float(d.get("score") or 0.0)
        # 内容
        content = str(d.get("content") or "").strip()

        # 行文本：带来源和分数
        evidence_lines.append(
            f"- [{'/'.join(sources)}] (score={score:.4f}) {content}"
        )

    # 命中来源总览
    source_summary = "、".join(sorted(source_set))

    # 组装最终回答
    return {
        "final_answer": (
            f"你问的是：{state.get('message', '')}。\n"
            f"命中来源：{source_summary}\n"
            f"我从知识库检索到以下证据：\n"
            f"{chr(10).join(evidence_lines)}\n"
            "这是 RETRIEVE 路径（MVP）。"
        )
    }



# 条件边选择器：根据 route 决定下一节点。
def _route_selector(state: AgentState) -> str:
    return state.get("route", "DIRECT")


# 构图函数：定义节点与边关系。
def build_agent_graph():
    # 创建状态图。
    builder = StateGraph(AgentState)

    # 注册节点。
    builder.add_node("build_context", build_context)
    builder.add_node("decide_route", decide_route)
    builder.add_node("direct_answer", direct_answer)
    builder.add_node("explain_page", explain_page)
    builder.add_node("retrieve_knowledge", retrieve_knowledge)
    builder.add_node("answer_with_retrieval", answer_with_retrieval)

    # 设置入口节点。
    builder.set_entry_point("build_context")

    # 固定边：build_context -> decide_route。
    builder.add_edge("build_context", "decide_route")

    # 条件边：按 route 分支。
    builder.add_conditional_edges(
        "decide_route",
        _route_selector,
        {
            "DIRECT": "direct_answer",
            "EXPLAIN_PAGE": "explain_page",
            "RETRIEVE": "retrieve_knowledge",
        },
    )

    # RETRIEVE 后再进入证据回答节点。
    builder.add_edge("retrieve_knowledge", "answer_with_retrieval")

    # 终止边。
    builder.add_edge("direct_answer", END)
    builder.add_edge("explain_page", END)
    builder.add_edge("answer_with_retrieval", END)

    # 编译并返回图执行器。
    return builder.compile()


# 模块级单例图执行器。
_agent_graph = build_agent_graph()


# 外部调用入口：把 ChatRequest 转成状态并执行图。
def run_agent(payload: ChatRequest, retrieved_docs: list[dict[str, Any]] | None = None) -> AgentState:
    # 构造初始状态。
    initial_state: AgentState = {
        "user_id": payload.user_id,
        "session_id": payload.session_id,
        "message": payload.message,
        "page_context": payload.page_context or {},
        "retrieved_docs": retrieved_docs or [],
    }

    # 执行并返回最终状态。
    return _agent_graph.invoke(initial_state)
