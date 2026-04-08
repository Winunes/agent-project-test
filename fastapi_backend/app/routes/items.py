"""Item 业务路由：提供列表查询、创建、删除接口。"""

# UUID 类型用于路径参数 item_id。
from uuid import UUID

# APIRouter: 创建路由分组；Depends: 注入依赖；HTTPException: 主动抛 HTTP 错误；Query: 查询参数约束。
from fastapi import APIRouter, Depends, HTTPException, Query
# Page/Params 用于分页响应和分页参数。
from fastapi_pagination import Page, Params
# apaginate 是 SQLAlchemy 异步分页函数。
from fastapi_pagination.ext.sqlalchemy import apaginate
# 异步数据库会话类型。
from sqlalchemy.ext.asyncio import AsyncSession
# select 用于构造查询语句。
from sqlalchemy.future import select

# 导入用户类型和数据库会话依赖。
from app.database import User, get_async_session
# 导入 Item ORM 模型。
from app.models import Item
# 导入 Item 的请求/响应 Schema。
from app.schemas import ItemRead, ItemCreate
# 导入“当前登录用户”依赖（需要鉴权）。
from app.users import current_active_user

# 创建路由对象，打上 item 标签，便于文档分类。
router = APIRouter(tags=["item"])


# 分页结果转换器：把 ORM Item 对象转成 ItemRead 响应模型。
def transform_items(items):
    # 对每个 ORM 对象执行 model_validate，保证返回结构受 Pydantic 约束。
    return [ItemRead.model_validate(item) for item in items]


# GET /items/：分页读取当前用户的 Item 列表。
@router.get("/", response_model=Page[ItemRead])
async def read_item(
    # 注入数据库会话。
    db: AsyncSession = Depends(get_async_session),
    # 注入当前已登录用户。
    user: User = Depends(current_active_user),
    # 页码参数：默认 1，且最小为 1。
    page: int = Query(1, ge=1, description="Page number"),
    # 每页数量参数：默认 10，范围 1~100。
    size: int = Query(10, ge=1, le=100, description="Page size"),
):
    # 组装分页参数对象。
    params = Params(page=page, size=size)
    # 只查询当前用户的数据，避免越权读取。
    query = select(Item).filter(Item.user_id == user.id)
    # 执行异步分页查询，并把结果转换为 ItemRead。
    return await apaginate(db, query, params, transformer=transform_items)


# POST /items/：创建一条新的 Item。
@router.post("/", response_model=ItemRead)
async def create_item(
    # 接收并校验请求体。
    item: ItemCreate,
    # 注入数据库会话。
    db: AsyncSession = Depends(get_async_session),
    # 注入当前已登录用户（用于写入 user_id）。
    user: User = Depends(current_active_user),
):
    # 把请求体展开后构造成 ORM 对象，并绑定当前用户 ID。
    db_item = Item(**item.model_dump(), user_id=user.id)
    # 将对象加入事务会话。
    db.add(db_item)
    # 提交事务。
    await db.commit()
    # 刷新对象，从数据库取回最新状态（如默认值）。
    await db.refresh(db_item)
    # 返回创建后的对象（将按 response_model 序列化）。
    return db_item


# DELETE /items/{item_id}：删除指定 Item（且必须属于当前用户）。
@router.delete("/{item_id}")
async def delete_item(
    # 路径参数：待删除的 Item ID。
    item_id: UUID,
    # 注入数据库会话。
    db: AsyncSession = Depends(get_async_session),
    # 注入当前用户，用于鉴权过滤。
    user: User = Depends(current_active_user),
):
    # 查询“ID 匹配且属于当前用户”的 Item。
    result = await db.execute(
        select(Item).filter(Item.id == item_id, Item.user_id == user.id)
    )
    # 取第一条记录（没有则为 None）。
    item = result.scalars().first()

    # 若记录不存在（或不属于当前用户），返回 404。
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")

    # 执行删除。
    await db.delete(item)
    # 提交事务。
    await db.commit()

    # 返回删除成功提示。
    return {"message": "Item successfully deleted"}
