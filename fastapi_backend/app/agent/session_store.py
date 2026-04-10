# 这个模块只负责会话/消息落库。
# 这样可以让路由层更薄，后续迁移到其他项目更容易复用。

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import ChatMessage, ChatSession


async def get_or_create_chat_session(
    db: AsyncSession,
    session_id: str,
    user_id: str,
) -> ChatSession:
    # 按前端传入的 session_id 查找会话。
    stmt = select(ChatSession).where(ChatSession.session_id == session_id)
    result = await db.execute(stmt)
    existing = result.scalars().first()

    # 找到就直接返回。
    if existing is not None:
        return existing

    # 没找到就新建会话。
    created = ChatSession(
        session_id=session_id,
        user_id=user_id,
    )
    db.add(created)

    # flush 后才能拿到 created.id（主键）。
    await db.flush()

    return created


async def add_chat_message(
    db: AsyncSession,
    chat_session_id,
    role: str,
    content: str,
) -> ChatMessage:
    # 写一条消息。
    row = ChatMessage(
        chat_session_id=chat_session_id,
        role=role,
        content=content,
    )
    db.add(row)

    # flush 让这条记录进入当前事务，便于后续逻辑继续使用。
    await db.flush()

    return row
