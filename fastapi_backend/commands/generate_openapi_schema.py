"""OpenAPI 导出脚本：生成给前端使用的接口 schema 文件。"""

# json 用于把 schema 写成格式化 JSON 文本。
import json
# Path 用于跨平台路径处理。
from pathlib import Path
# 导入 FastAPI app，以便读取 app.openapi()。
from app.main import app
# os 用于读取环境变量。
import os

# load_dotenv 用于加载 .env 文件。
from dotenv import load_dotenv

# 先加载 .env，确保可读取 OPENAPI_OUTPUT_FILE。
load_dotenv()

# 读取输出文件路径（如 ../nextjs-frontend/openapi.json）。
OUTPUT_FILE = os.getenv("OPENAPI_OUTPUT_FILE")


# 生成并写出 OpenAPI schema。
def generate_openapi_schema(output_file):
    # 从 FastAPI 应用获取标准 OpenAPI 结构（字典）。
    schema = app.openapi()
    # 构建输出路径对象。
    output_path = Path(output_file)

    # 对 operationId 做一次清理，便于前端生成更短的方法名。
    updated_schema = remove_operation_id_tag(schema)

    # 以 2 空格缩进写入 JSON 文件。
    output_path.write_text(json.dumps(updated_schema, indent=2))
    # 打印成功日志。
    print(f"OpenAPI schema saved to {output_file}")


# 移除 operationId 中的 tag 前缀（例如 auth-login -> login）。
def remove_operation_id_tag(schema):
    """
    去掉 OpenAPI operationId 的 tag 前缀。

    这样前端生成的 SDK 方法名会更短、更清晰。
    """
    # 遍历所有 path（接口路径）。
    for path_data in schema["paths"].values():
        # 遍历该路径下的各 HTTP 方法定义。
        for operation in path_data.values():
            # 取第一个 tag 作为前缀。
            tag = operation["tags"][0]
            # 获取原 operationId。
            operation_id = operation["operationId"]
            # 计算待移除前缀（例如 "auth-"）。
            to_remove = f"{tag}-"
            # 去掉前缀得到新 operationId。
            new_operation_id = operation_id[len(to_remove) :]
            # 回写修改后的 operationId。
            operation["operationId"] = new_operation_id
    # 返回处理后的 schema。
    return schema


# 允许该文件被直接执行：python -m commands.generate_openapi_schema
if __name__ == "__main__":
    generate_openapi_schema(OUTPUT_FILE)
