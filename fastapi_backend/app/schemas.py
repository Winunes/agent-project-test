"""Pydantic 模式定义：用于接口请求体校验与响应体序列化。"""

# uuid 模块用于给 fastapi-users 的泛型参数提供 UUID 类型。
import uuid

# fastapi-users 内置了用户相关的请求/响应 Schema 基类。
from fastapi_users import schemas
# BaseModel 是 Pydantic 的基础数据模型类。
from pydantic import BaseModel
# UUID 类型用于声明字段类型。
from uuid import UUID


# 用户读取模型（响应返回给前端的数据结构）。
class UserRead(schemas.BaseUser[uuid.UUID]):
    # 继承 fastapi-users 默认字段即可（无需额外字段）。
    pass


# 用户注册模型（前端注册时提交的数据结构）。
class UserCreate(schemas.BaseUserCreate):
    # 使用 fastapi-users 的标准定义。
    pass


# 用户更新模型（用户资料更新时的数据结构）。
class UserUpdate(schemas.BaseUserUpdate):
    # 使用 fastapi-users 的标准定义。
    pass


# Item 基础字段：创建和读取都会复用。
class ItemBase(BaseModel):
    # 条目名称（必填）。
    name: str
    # 条目描述（可空）。
    description: str | None = None
    # 数量（可空）。
    quantity: int | None = None


# 创建 Item 时的请求体模型（当前与 ItemBase 相同）。
class ItemCreate(ItemBase):
    # 继承基础字段即可。
    pass


# 读取 Item 时的响应体模型。
class ItemRead(ItemBase):
    # 条目主键 ID。
    id: UUID
    # 所属用户 ID。
    user_id: UUID

    # 允许从 ORM 对象直接构造响应模型（Pydantic v2 写法）。
    model_config = {"from_attributes": True}

# ---------------------------
# Agent Chat: request schema
# ---------------------------

class ChatRequest(BaseModel):
    # 当前用户 ID（后续可和登录用户做一致性校验）
    user_id: str
    # 会话 ID（同一会话多轮对话复用）
    session_id: str
    # 用户本轮输入
    message: str
    # 页面上下文（先可选，后面阶段会真正使用）
    page_context: dict | None = None
