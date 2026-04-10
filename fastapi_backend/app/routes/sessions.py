# 会话读取路由（MVP）
# 作用：按 session_id 返回该会话下的历史消息

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.models import ChatMessage, ChatSession

# 路由分组标签
router = APIRouter(tags=["sessions"])


@router.get("/{session_id}")
async def get_session_history(
    session_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    # 1) 先找会话主记录
    session_stmt = select(ChatSession).where(ChatSession.session_id == session_id)
    session_result = await db.execute(session_stmt)
    session_row = session_result.scalars().first()

    # 2) 如果会话不存在，返回 404
    if session_row is None:
        raise HTTPException(status_code=404, detail="Session not found")

    # 3) 查询该会话下所有消息，按创建时间升序（从早到晚）
    message_stmt = (
        select(ChatMessage)
        .where(ChatMessage.chat_session_id == session_row.id)
        .order_by(ChatMessage.created_at.asc())
    )
    message_result = await db.execute(message_stmt)
    message_rows = message_result.scalars().all()

    # 4) 组装返回结构（先用 dict，MVP 足够）
    return {
        "session_id": session_row.session_id,
        "user_id": session_row.user_id,
        "created_at": session_row.created_at.isoformat() if session_row.created_at else None,
        "updated_at": session_row.updated_at.isoformat() if session_row.updated_at else None,
        "messages": [
            {
                "id": str(msg.id),
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat() if msg.created_at else None,
            }
            for msg in message_rows
        ],
    }
