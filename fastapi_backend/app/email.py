"""邮件发送模块：负责构建邮件配置并发送重置密码邮件。"""

# Path 用于拼接模板目录路径。
from pathlib import Path
# urllib.parse 用于安全地编码 URL 查询参数。
import urllib.parse

# fastapi-mail 提供邮件连接配置、消息结构和发送器。
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
# 项目全局配置。
from .config import settings
# 用户模型（用于读取用户邮箱）。
from .models import User


# 构建并返回邮件连接配置对象。
def get_email_config():
    # 从 settings 读取所有 SMTP 参数。
    conf = ConnectionConfig(
        MAIL_USERNAME=settings.MAIL_USERNAME,
        MAIL_PASSWORD=settings.MAIL_PASSWORD,
        MAIL_FROM=settings.MAIL_FROM,
        MAIL_PORT=settings.MAIL_PORT,
        MAIL_SERVER=settings.MAIL_SERVER,
        MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
        MAIL_STARTTLS=settings.MAIL_STARTTLS,
        MAIL_SSL_TLS=settings.MAIL_SSL_TLS,
        USE_CREDENTIALS=settings.USE_CREDENTIALS,
        VALIDATE_CERTS=settings.VALIDATE_CERTS,
        TEMPLATE_FOLDER=Path(__file__).parent / settings.TEMPLATE_DIR,
    )
    # 返回配置对象给调用方。
    return conf


# 发送重置密码邮件。
async def send_reset_password_email(user: User, token: str):
    # 获取邮件配置。
    conf = get_email_config()
    # 取出收件人邮箱。
    email = user.email
    # 构造前端密码重置页面地址（基础路径）。
    base_url = f"{settings.FRONTEND_URL}/password-recovery/confirm?"
    # 把 token 作为查询参数传给前端页面。
    params = {"token": token}
    # URL 编码查询参数，避免特殊字符破坏链接格式。
    encoded_params = urllib.parse.urlencode(params)
    # 拼接最终跳转链接。
    link = f"{base_url}{encoded_params}"
    # 构造邮件消息体。
    message = MessageSchema(
        subject="Password recovery",
        recipients=[email],
        template_body={"username": email, "link": link},
        subtype=MessageType.html,
    )

    # 创建发送器实例。
    fm = FastMail(conf)
    # 使用 HTML 模板发送邮件。
    await fm.send_message(message, template_name="password_reset.html")
