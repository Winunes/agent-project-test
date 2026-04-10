from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from app.schemas import ChatRequest


class AgentState(TypedDict, total=False):
    user_id: str
    session_id: str
    message: str
    page_context: dict[str, Any]
    route: str
    final_answer: str


def build_context(state: AgentState) -> AgentState:
    # MVP 先保留直通，后续可在这里拼历史会话
    return {}


def decide_route(state: AgentState) -> AgentState:
    page_context = state.get("page_context", {})
    page_title = str(page_context.get("page_title") or "").strip()
    module_name = str(page_context.get("module_name") or "").strip()
    page_url = str(page_context.get("page_url") or "").strip()
    visible_summary = str(page_context.get("visible_text_summary") or "").strip()

    has_page_context = bool(page_title or module_name or page_url or visible_summary)
    route = "EXPLAIN_PAGE" if has_page_context else "DIRECT"
    return {"route": route}


def direct_answer(state: AgentState) -> AgentState:
    return {
        "final_answer": f"你问的是：{state.get('message', '')}。这是 DIRECT 路径（MVP）。"
    }


def explain_page(state: AgentState) -> AgentState:
    page_context = state.get("page_context", {})
    page_title = str(page_context.get("page_title") or "").strip()
    module_name = str(page_context.get("module_name") or "").strip()
    visible_summary = str(page_context.get("visible_text_summary") or "").strip()

    preview = visible_summary[:160] if visible_summary else "（页面摘要为空）"
    return {
        "final_answer": (
            f"你问的是：{state.get('message', '')}。"
            f"我基于当前页面「{page_title or module_name or '未命名页面'}」回答。"
            f"页面摘要：{preview}。这是 EXPLAIN_PAGE 路径（MVP）。"
        )
    }


def _route_selector(state: AgentState) -> str:
    return state.get("route", "DIRECT")


def build_agent_graph():
    builder = StateGraph(AgentState)

    builder.add_node("build_context", build_context)
    builder.add_node("decide_route", decide_route)
    builder.add_node("direct_answer", direct_answer)
    builder.add_node("explain_page", explain_page)

    builder.set_entry_point("build_context")
    builder.add_edge("build_context", "decide_route")
    builder.add_conditional_edges(
        "decide_route",
        _route_selector,
        {
            "DIRECT": "direct_answer",
            "EXPLAIN_PAGE": "explain_page",
        },
    )
    builder.add_edge("direct_answer", END)
    builder.add_edge("explain_page", END)

    return builder.compile()


_agent_graph = build_agent_graph()


def run_agent(payload: ChatRequest) -> AgentState:
    initial_state: AgentState = {
        "user_id": payload.user_id,
        "session_id": payload.session_id,
        "message": payload.message,
        "page_context": payload.page_context or {},
    }
    return _agent_graph.invoke(initial_state)
