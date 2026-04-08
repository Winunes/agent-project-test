"""用户与鉴权模块：封装注册、登录、JWT、密码策略等逻辑。"""

# uuid 用于用户主键类型。
import uuid
# re 用于密码复杂度正则校验。
import re

# Optional 用于声明可选的 Request 参数。
from typing import Optional

# Depends 用于依赖注入，Request 用于回调钩子中拿请求上下文。
from fastapi import Depends, Request
# fastapi-users 的核心组件。
from fastapi_users import (
    BaseUserManager,  # 用户管理器基类
    FastAPIUsers,  # 生成路由与依赖的高层封装
    UUIDIDMixin,  # 指定用户 ID 是 UUID
    InvalidPasswordException,  # 密码校验失败异常
)

# fastapi-users 的认证相关组件。
from fastapi_users.authentication import (
    AuthenticationBackend,  # 认证后端配置
    BearerTransport,  # Bearer Token 传输方式
    JWTStrategy,  # JWT 生成/校验策略
)
# fastapi-users 的 SQLAlchemy 用户数据库适配器类型。
from fastapi_users.db import SQLAlchemyUserDatabase

# 导入项目配置。
from .config import settings
# 导入用户数据库依赖。
from .database import get_user_db
# 导入发送重置密码邮件函数。
from .email import send_reset_password_email
# 导入用户 ORM 模型。
from .models import User
# 导入注册数据 Schema（用于密码校验中读取邮箱）。
from .schemas import UserCreate

# 认证路由统一前缀片段（最终会组合成 /auth/...）。
AUTH_URL_PATH = "auth"


# 自定义用户管理器：可覆写注册后、忘记密码后、密码规则等行为。
class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    # 设置重置密码令牌签名密钥。
    reset_password_token_secret = settings.RESET_PASSWORD_SECRET_KEY
    # 设置邮箱验证令牌签名密钥。
    verification_token_secret = settings.VERIFICATION_SECRET_KEY

    # 注册成功后的钩子。
    async def on_after_register(self, user: User, request: Optional[Request] = None):
        # 这里简单打印日志；生产可替换为审计日志或埋点。
        print(f"User {user.id} has registered.")

    # 用户发起“忘记密码”后的钩子。
    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # 发送包含 token 的密码重置邮件。
        await send_reset_password_email(user, token)

    # 用户请求邮箱验证后的钩子。
    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        # 这里示例为打印日志；生产建议改为异步邮件发送。
        print(f"Verification requested for user {user.id}. Verification token: {token}")

    # 自定义密码校验规则。
    async def validate_password(
        self,
        password: str,
        user: UserCreate,
    ) -> None:
        # 收集所有不满足规则的错误信息，统一返回给前端。
        errors = []

        # 规则 1：至少 8 位。
        if len(password) < 8:
            errors.append("Password should be at least 8 characters.")
        # 规则 2：不能包含邮箱字符串。
        if user.email in password:
            errors.append("Password should not contain e-mail.")
        # 规则 3：必须包含至少一个大写字母。
        if not any(char.isupper() for char in password):
            errors.append("Password should contain at least one uppercase letter.")
        # 规则 4：必须包含至少一个特殊字符。
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password should contain at least one special character.")

        # 若有错误，抛出标准异常让 fastapi-users 统一包装响应。
        if errors:
            raise InvalidPasswordException(reason=errors)


# FastAPI 依赖：为每次请求创建一个 UserManager 实例。
async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    # 把 user_db 注入 UserManager 后 yield 出去。
    yield UserManager(user_db)


# 指定客户端如何携带 token：Authorization: Bearer <token>。
bearer_transport = BearerTransport(tokenUrl=f"{AUTH_URL_PATH}/jwt/login")


# 返回 JWT 策略对象（签名密钥 + 过期时间）。
def get_jwt_strategy() -> JWTStrategy:
    # secret 用于签名和校验 JWT；lifetime_seconds 控制有效期。
    return JWTStrategy(
        secret=settings.ACCESS_SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS,
    )


# 配置认证后端（命名为 jwt，传输方式 Bearer，策略为 JWT）。
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# 创建 fastapi-users 主对象：后续由它生成 auth/users 路由与依赖。
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])

# 获取“当前已登录且激活用户”的依赖，可直接注入到受保护路由。
current_active_user = fastapi_users.current_user(active=True)
