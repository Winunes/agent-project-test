#!/bin/bash

# 判断当前是否运行在 Docker 容器中。
if [ -f /.dockerenv ]; then
    # Docker 场景：直接使用系统内 fastapi 命令启动开发服务（后台运行）。
    echo "Running in Docker"
    fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload &
    # Docker 场景下启动后端 watcher（监听变更并生成 OpenAPI）。
    python watcher.py
else
    # 本机场景：通过 uv 执行命令，确保使用项目虚拟环境依赖。
    echo "Running locally with uv"
    uv run fastapi dev app/main.py --host 0.0.0.0 --port 8000 --reload &
    # 本机场景下也启动 watcher。
    uv run python watcher.py
fi

# 等待后台任务结束，避免脚本提前退出。
wait
