"""应用配置模块：负责把 .env 中的配置读取成可类型检查的对象。"""

# 引入 Set，用来声明“允许跨域来源”的集合类型。
from typing import Set

# BaseSettings: Pydantic 提供的配置基类，支持从环境变量自动读取。
# SettingsConfigDict: 用于声明 BaseSettings 的读取行为（如 .env 路径）。
from pydantic_settings import BaseSettings, SettingsConfigDict


# 统一定义整个应用的配置结构。
class Settings(BaseSettings):
    # OpenAPI 文档 JSON 的访问路径；默认暴露为 /openapi.json。
    OPENAPI_URL: str = "/openapi.json"

    # 主数据库连接串（必须配置）。
    DATABASE_URL: str
    # 测试数据库连接串（可选，测试环境用）。
    TEST_DATABASE_URL: str | None = None
    # SQLAlchemy 提交事务后是否让对象失效（默认 False，便于后续直接读取对象属性）。
    EXPIRE_ON_COMMIT: bool = False

    # JWT 访问令牌签名密钥（必须配置）。
    ACCESS_SECRET_KEY: str
    # 重置密码令牌签名密钥（必须配置）。
    RESET_PASSWORD_SECRET_KEY: str
    # 邮箱验证令牌签名密钥（必须配置）。
    VERIFICATION_SECRET_KEY: str
    # JWT 签名算法，默认 HS256。
    ALGORITHM: str = "HS256"
    # JWT 访问令牌过期秒数，默认 1 小时。
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600

    # 发件邮箱用户名（可选，本地开发可为空）。
    MAIL_USERNAME: str | None = None
    # 发件邮箱密码（可选）。
    MAIL_PASSWORD: str | None = None
    # 发件人邮箱地址（可选）。
    MAIL_FROM: str | None = None
    # 邮件服务器地址（可选）。
    MAIL_SERVER: str | None = None
    # 邮件服务器端口（可选）。
    MAIL_PORT: int | None = None
    # 发件人展示名称。
    MAIL_FROM_NAME: str = "FastAPI template"
    # 是否启用 STARTTLS。
    MAIL_STARTTLS: bool = True
    # 是否启用 SSL/TLS（与 STARTTLS 二选一为主）。
    MAIL_SSL_TLS: bool = False
    # 是否使用用户名/密码认证。
    USE_CREDENTIALS: bool = True
    # 是否校验证书。
    VALIDATE_CERTS: bool = True
    # 邮件模板目录（相对于 app 目录）。
    TEMPLATE_DIR: str = "email_templates"

    # 前端根地址，用于生成邮件中的回跳链接。
    FRONTEND_URL: str = "http://localhost:3000"

    # CORS 允许来源集合（例如 ["http://localhost:3000"]）。
    CORS_ORIGINS: Set[str]

    # 声明配置读取行为：从 .env 读取、UTF-8 编码、忽略未声明的多余字段。
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


# 在模块加载时创建全局 settings 实例，供全项目直接导入使用。
settings = Settings()
