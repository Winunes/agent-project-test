"""FastAPI 应用入口：创建 app、挂载中间件、注册全部路由。"""

# FastAPI 主类。
from fastapi import FastAPI
# 分页扩展注册函数。
from fastapi_pagination import add_pagination
# 用户相关请求/响应 Schema。
from .schemas import UserCreate, UserRead, UserUpdate
# 用户鉴权系统对象和认证路径前缀。
from .users import auth_backend, fastapi_users, AUTH_URL_PATH
# CORS 中间件（处理跨域请求）。
from fastapi.middleware.cors import CORSMiddleware
# 自定义 OpenAPI operationId 生成函数。
from .utils import simple_generate_unique_route_id
# Item 业务路由。
from app.routes.items import router as items_router
# 全局配置。
from app.config import settings
# 健康检查路由
from app.routes.health import router as health_router
# 聊天路由
from app.routes.chat import router as chat_router
# 会话历史路由
from app.routes.sessions import router as sessions_router
# 文档入库路由
from app.routes.ingest import router as ingest_router

# 创建 FastAPI 应用实例。
app = FastAPI(
    # 使用自定义 operationId，便于前端生成更稳定的 SDK 方法名。
    generate_unique_id_function=simple_generate_unique_route_id,
    # OpenAPI 文档地址可通过环境变量控制。
    openapi_url=settings.OPENAPI_URL,
)

# 添加 CORS 中间件，允许前端跨域访问后端接口。
app.add_middleware(
    CORSMiddleware,
    # 允许访问的来源列表（从配置读取）。
    allow_origins=settings.CORS_ORIGINS,
    # 是否允许携带 cookie/认证头等凭据。
    allow_credentials=True,
    # 允许所有 HTTP 方法（GET/POST/PUT/DELETE...）。
    allow_methods=["*"],
    # 允许所有请求头。
    allow_headers=["*"],
)

# 注册登录/登出相关认证路由（例如 /auth/jwt/login）。
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix=f"/{AUTH_URL_PATH}/jwt",
    tags=["auth"],
)
# 注册用户注册路由（例如 /auth/register）。
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix=f"/{AUTH_URL_PATH}",
    tags=["auth"],
)
# 注册忘记密码/重置密码路由。
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix=f"/{AUTH_URL_PATH}",
    tags=["auth"],
)
# 注册邮箱验证相关路由。
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix=f"/{AUTH_URL_PATH}",
    tags=["auth"],
)
# 注册用户信息路由（当前用户、按 ID 用户等）。
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)

# 注册 Item 业务路由，前缀为 /items。
app.include_router(items_router, prefix="/items")
# 注册健康检查路由，前缀为 /health。
app.include_router(health_router, prefix="/health")
# Agent 聊天流式接口前缀
app.include_router(chat_router, prefix="/api/v1/chat")
# 会话历史接口前缀
app.include_router(sessions_router, prefix="/api/v1/sessions")
# 文档入库接口前缀
app.include_router(ingest_router, prefix="/api/v1/ingest")

# 启用 fastapi-pagination 功能（必须调用一次）。
add_pagination(app)
