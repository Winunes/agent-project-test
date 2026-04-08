"""数据库基础设施模块：负责创建引擎、会话和用户仓储依赖。"""

# AsyncGenerator 用于声明“异步生成器”返回类型（yield session）。
from typing import AsyncGenerator
# urlparse 用于拆解 DATABASE_URL，便于重组为 asyncpg 连接串。
from urllib.parse import urlparse

# Depends 用于 FastAPI 依赖注入。
from fastapi import Depends
# fastapi-users 的 SQLAlchemy 用户数据库适配器。
from fastapi_users.db import SQLAlchemyUserDatabase
# NullPool 表示禁用连接池（更适合某些无状态/Serverless 场景）。
from sqlalchemy import NullPool
# AsyncSession/async_sessionmaker/create_async_engine 是 SQLAlchemy 异步三件套。
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

# 读取全局配置对象。
from .config import settings
# 导入 ORM 基类和用户模型。
from .models import Base, User


# 解析环境变量里的数据库连接串。
parsed_db_url = urlparse(settings.DATABASE_URL)

# 重新拼接异步驱动连接串，确保使用 postgresql+asyncpg。
async_db_connection_url = (
    f"postgresql+asyncpg://{parsed_db_url.username}:{parsed_db_url.password}@"
    f"{parsed_db_url.hostname}{':' + str(parsed_db_url.port) if parsed_db_url.port else ''}"
    f"{parsed_db_url.path}"
)

# 创建异步数据库引擎，并禁用连接池（模板面向 Vercel 等场景）。
engine = create_async_engine(async_db_connection_url, poolclass=NullPool)

# 创建异步 Session 工厂，控制 commit 后对象是否过期。
async_session_maker = async_sessionmaker(
    engine,
    expire_on_commit=settings.EXPIRE_ON_COMMIT,
)


# 初始化数据库表（仅开发或初次启动时常用，生产通常用 Alembic 迁移）。
async def create_db_and_tables():
    # 开启一个数据库连接上下文。
    async with engine.begin() as conn:
        # 同步 ORM 元数据建表动作通过 run_sync 在异步连接中执行。
        await conn.run_sync(Base.metadata.create_all)


# FastAPI 依赖：为每个请求提供一个独立的异步 Session。
async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    # 进入 Session 上下文。
    async with async_session_maker() as session:
        # 把 session 交给使用方（路由/服务层）。
        yield session
        # 上下文结束时自动关闭 session。


# FastAPI 依赖：给 fastapi-users 提供用户数据库访问对象。
async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    # 基于当前请求 session 构建用户数据库适配器并返回。
    yield SQLAlchemyUserDatabase(session, User)
