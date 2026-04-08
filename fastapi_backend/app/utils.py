"""工具函数模块：放置可复用的小型通用方法。"""

# APIRoute 类型用于给函数参数提供更准确的类型提示。
from fastapi.routing import APIRoute


# 生成 OpenAPI operationId 的简化函数。
def simple_generate_unique_route_id(route: APIRoute):
    # 规则：使用“首个标签-路由函数名”，例如 "auth-login"。
    return f"{route.tags[0]}-{route.name}"
