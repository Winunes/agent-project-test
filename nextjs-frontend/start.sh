#!/bin/bash

# 启动 Next.js 开发服务器（后台运行）。
pnpm run dev &

# 启动前端 watcher：监听 OpenAPI 文件变化并自动生成客户端代码。
node watcher.js

# 等待后台任务，保持脚本常驻。
wait
