"""会话历史查看脚本（MVP 调试工具）。

用法示例：
1) 指定 session_id 查询：
   uv run python tests/test_session_history.py --session-id <SESSION_ID>

2) 自动查最近一条会话并查询：
   uv run python tests/test_session_history.py --latest

3) 自动查某个用户最近会话并查询：
   uv run python tests/test_session_history.py --latest --user-id u_abcd1234
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any

# 关键：把 fastapi_backend 根目录加入 sys.path
# 这样用“python tests/test_session_history.py”也能 import app.*
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import httpx
from sqlalchemy import select

from app.database import async_session_maker
from app.models import ChatSession


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="查看会话历史（通过后端 sessions API）")
    parser.add_argument("--session-id", type=str, default="", help="要查询的 session_id")
    parser.add_argument("--latest", action="store_true", help="自动查询数据库中最近一条会话的 session_id")
    parser.add_argument("--user-id", type=str, default="", help="和 --latest 一起使用，只查这个 user_id 的最近会话")
    parser.add_argument(
        "--api-base-url",
        type=str,
        default="http://127.0.0.1:8000",
        help="后端 API 基地址，默认 http://127.0.0.1:8000",
    )
    parser.add_argument("--raw", action="store_true", help="打印原始 JSON，不做格式化展示")

    args = parser.parse_args()
    if not args.session_id and not args.latest:
        parser.error("请提供 --session-id 或使用 --latest")
    return args


async def get_latest_session_id(user_id: str = "") -> str:
    async with async_session_maker() as db:
        stmt = select(ChatSession)
        if user_id:
            stmt = stmt.where(ChatSession.user_id == user_id)
        stmt = stmt.order_by(ChatSession.created_at.desc()).limit(1)

        result = await db.execute(stmt)
        row = result.scalars().first()
        return row.session_id if row else ""


async def fetch_session_history(api_base_url: str, session_id: str) -> dict[str, Any]:
    url = f"{api_base_url.rstrip('/')}/api/v1/sessions/{session_id}"
    async with httpx.AsyncClient(timeout=20.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


def print_history(data: dict[str, Any]) -> None:
    print("=" * 80)
    print("会话信息")
    print(f"session_id: {data.get('session_id')}")
    print(f"user_id:    {data.get('user_id')}")
    print(f"created_at: {data.get('created_at')}")
    print(f"updated_at: {data.get('updated_at')}")
    print("=" * 80)

    messages = data.get("messages", [])
    print(f"消息条数: {len(messages)}")

    for idx, msg in enumerate(messages, start=1):
        role = msg.get("role", "unknown")
        content = msg.get("content", "")
        created_at = msg.get("created_at", "")
        print("-" * 80)
        print(f"#{idx} [{role}] {created_at}")
        print(content)

    print("=" * 80)


async def main() -> int:
    args = parse_args()

    session_id = args.session_id.strip()
    if args.latest:
        session_id = await get_latest_session_id(user_id=args.user_id.strip())

    if not session_id:
        print("未找到可用的 session_id。请先发起一次聊天，或检查 --user-id。")
        return 1

    print(f"准备查询 session_id: {session_id}")

    try:
        data = await fetch_session_history(args.api_base_url, session_id)
    except httpx.HTTPStatusError as exc:
        print(f"请求失败：HTTP {exc.response.status_code} - {exc.response.text}")
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"请求失败：{exc}")
        return 1

    if args.raw:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print_history(data)

    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
