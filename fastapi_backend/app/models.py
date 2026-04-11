"""ORM models."""

from uuid import uuid4

from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, relationship


# 所有模型统一继承的基类（承载 metadata）。
class Base(DeclarativeBase):
    # 这里不定义字段，仅作为声明式模型根基类。
    pass


# 用户模型：在 fastapi-users 的默认用户字段基础上扩展关系字段。
class User(SQLAlchemyBaseUserTableUUID, Base):
    # 与 Item 的一对多关系：一个用户可以有多个 Item。
    # back_populates="user" 对应 Item.user。
    # cascade="all, delete-orphan" 表示删除用户时级联删除其 Item。
    items = relationship("Item", back_populates="user", cascade="all, delete-orphan")


# 业务模型：用户的条目数据（示例领域对象）。
class Item(Base):
    # 数据库表名。
    __tablename__ = "items"

    # 主键：UUID，默认自动生成。
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # 条目名称，必填。
    name = Column(String, nullable=False)
    # 条目描述，可空。
    description = Column(String, nullable=True)
    # 数量，可空（模板允许不填）。
    quantity = Column(Integer, nullable=True)
    # 所属用户 ID，外键关联 user.id，必填。
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)

    # 多对一关系：每个 Item 归属于一个 User。
    user = relationship("User", back_populates="items")


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    # 前端传入的会话 ID（字符串），用于跨请求串起同一会话
    session_id = Column(String, nullable=False, unique=True, index=True)
    # MVP 先用字符串 user_id（前端当前也是字符串）
    user_id = Column(String, nullable=False, index=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="ChatMessage.created_at",
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    chat_session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role = Column(String, nullable=False)  # user | assistant | system
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    session = relationship("ChatSession", back_populates="messages")

class Document(Base):
    __tablename__ = "documents"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_id = Column(String, nullable=False, unique=True, index=True)
    source = Column(String, nullable=False, index=True)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentChunk.chunk_index",
    )


class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    document_pk = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    chunk_index = Column(Integer, nullable=False)
    chunk_text = Column(Text, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    document = relationship("Document", back_populates="chunks")