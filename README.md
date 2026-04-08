## Next.js FastAPI Template

<a href="https://www.vintasoftware.com/blog/next-js-fastapi-template"><img src="docs/images/banner.png" alt="Next.js FastAPI Template" width="auto"></a>
<p align="center">
    <em>Next.js FastAPI Template：Python + 现代 TypeScript 技术栈，内置 Zod 校验。</em>
</p>
<p align="center">
<a href="https://github.com/vintasoftware/nextjs-fastapi-template/actions/workflows/ci.yml" target="_blank">
    <img src="https://github.com/vintasoftware/nextjs-fastapi-template/actions/workflows/ci.yml/badge.svg" alt="CI">
</a>
<a href="https://coveralls.io/github/vintasoftware/nextjs-fastapi-template" target="_blank">
    <img src="https://coveralls.io/repos/github/vintasoftware/nextjs-fastapi-template/badge.svg" alt="Coverage">
</a>
</p>

---

**Documentation**: <a href="https://vintasoftware.github.io/nextjs-fastapi-template/" target="_blank">https://vintasoftware.github.io/nextjs-fastapi-template/</a>

**Source Code**: <a href="https://github.com/vintasoftware/nextjs-fastapi-template/" target="_blank">https://github.com/vintasoftware/nextjs-fastapi-template/</a>

---

Next.js FastAPI Template 为可扩展、高性能的 Web 应用提供了坚实基础，遵循清晰架构与工程最佳实践。它将 FastAPI、Pydantic 与 Next.js（TypeScript + Zod）组合在一起，帮助你在前后端之间实现端到端类型安全与结构校验。

FastAPI 后端支持完全异步执行，可优化数据库查询、API 路由处理和测试效率。部署体验也很顺畅：前后端都可直接部署到 Vercel，用较少配置快速上线产品。

### Key features
- 端到端类型安全：基于 OpenAPI 自动生成强类型客户端，前后端接口契约保持一致。
- 热更新联动：后端路由变更后可自动更新客户端，让 FastAPI 与 Next.js 持续同步。
- 通用项目底座：同时适用于 MVP 与生产环境，内置认证系统和 API 基础层。
- 快速部署：只需少量步骤即可在 Vercel 部署完整全栈应用（含认证流程与仪表盘）。
- 生产可用认证：预置认证与用户管理界面，上手即可开发业务功能。

## Technology stack
该模板采用了一组经过实践验证的技术方案，兼顾开发效率、可扩展性和可维护性：

- Zod + TypeScript：全栈类型安全与数据结构校验。
- fastapi-users：完整认证体系，包含：
    - 安全密码哈希
    - JWT 认证
- 基于邮箱的密码找回。
- shadcn/ui：基于 Tailwind CSS 的预构建 React 组件。
- OpenAPI-fetch：基于 OpenAPI 自动生成强类型客户端。
- UV：简化 Python 依赖管理与打包。
- Docker Compose：统一开发与生产环境。
- Pre-commit hooks：提交前自动执行 lint、格式化与校验。
- Vercel 部署：Serverless 后端 + 可扩展前端，低配置即可上线。

以上只是模板技术栈的一部分，完整列表可查看 [Technology selection](https://vintasoftware.github.io/nextjs-fastapi-template/technology-selection/)。

## Get Started

想开始使用这个模板，请阅读 [Get Started](https://vintasoftware.github.io/nextjs-fastapi-template/get-started/) 并按步骤操作。

## Using the template? Let's talk!

我们很期待看到社区如何基于它构建项目、并把它用到真实业务里。欢迎通过以下方式参与：

- 在 [GitHub Discussions](https://github.com/vintasoftware/nextjs-fastapi-template/discussions) 参与讨论
- 通过 [issues](https://github.com/vintasoftware/nextjs-fastapi-template/issues) 报告问题或提出改进建议
- 查看 [Contributing](https://vintasoftware.github.io/nextjs-fastapi-template/contributing/) 指南并参与贡献

本项目由 [Vinta Software](https://www.vinta.com.br/) 维护，并已用于我们为客户构建的生产系统。若你需要专家支持，可联系我们获取免费技术评估：contact@vinta.com.br。

*免责声明：本项目与 Vercel 无官方隶属关系。*
