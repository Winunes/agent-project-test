# Contributing

欢迎参与 Next.js FastAPI Template 的改进！你可以直接认领现有 [issues](https://github.com/vintasoftware/nextjs-fastapi-template/issues)。
如果你有新的想法，欢迎在 [Discussions](https://github.com/vintasoftware/django-ai-assistant/discussions) 发起讨论。

在提交 Pull Request 之前，请先按本指南完成本地开发与测试环境准备。

## Local Dev Setup

### Clone the repo

```bash
git clone git@github.com:vintasoftware/nextjs-fastapi-template.git
```

请先阅读 [Get Started](get-started.md#setup) 完成基础环境配置。

## Install pre-commit hooks

请参考 [Additional Settings - Install pre-commit hooks](additional-settings.md#pre-commit-setup) 完成配置。

在推送代码前执行 pre-commit 很重要，这能确保代码风格统一并避免 lint 错误。

## Updating the OpenAPI schema

当你修改 FastAPI 路由或相关文件时，必须同步更新 OpenAPI schema。

请参考 [Additional Settings - Manual execution of hot reload commands](additional-settings.md#manual-execution-of-hot-reload-commands) 执行对应命令。

## Tests

请参考 [Additional Settings - Testing](additional-settings.md#testing) 的说明运行测试。

## Documentation

文档由 [mkdocs-material](https://squidfunk.github.io/mkdocs-material/) 从 Markdown 文件生成，文档源文件位于 `docs` 目录。

如需本地预览文档，请执行：

```bash
uv run mkdocs serve
```

## Release

!!! info
    后端与前端使用同一版本号进行发布，也就是说两者版本号应保持一致。

发布新版本的步骤如下：

1. 更新 `fastapi_backend/pyproject.toml` 与 `nextjs-frontend/package.json` 中的版本号。
2. 更新 `CHANGELOG.md`。
3. 提交并创建 PR。
4. PR 合并后，运行 [Release GitHub Action](https://github.com/vintasoftware/nextjs-fastapi-template/actions/workflows/release.yml) 生成草稿版 Release。
5. 检查草稿 Release，确认描述中至少包含本次变更对应的 changelog 条目，然后发布。
