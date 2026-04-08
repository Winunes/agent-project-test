这个模板用于快速构建 [FastAPI](https://fastapi.tiangolo.com/) API 与 [Next.js](https://nextjs.org/) 动态前端。它通过 [@hey-api/openapi-ts](https://github.com/hey-ai/openapi-ts) 打通前后端：自动从 OpenAPI 生成类型安全客户端，并配合监听脚本自动更新 schema 与客户端代码，保持开发过程顺畅且同步。

- [Next.js](https://nextjs.org/)：高性能、SEO 友好的前端框架。  
- [FastAPI](https://fastapi.tiangolo.com/)：高性能 Python 后端框架。  
- [SQLAlchemy](https://www.sqlalchemy.org/)：功能强大的 Python ORM/SQL 工具。  
- [PostgreSQL](https://www.postgresql.org/)：成熟稳定的开源关系型数据库。  
- [Pydantic](https://docs.pydantic.dev/)：基于类型注解的数据校验与配置管理。  
- [Zod](https://zod.dev/) + [TypeScript](https://www.typescriptlang.org/)：实现端到端类型安全与结构校验。  
- [fastapi-users](https://fastapi-users.github.io/fastapi-users/)：完整认证方案，包含：
  - 默认安全密码哈希
  - JWT（JSON Web Token）认证
  - 邮箱找回密码
- [Shadcn/ui](https://ui.shadcn.com/)：可定制、现代化的 React 组件库。  
- [OpenAPI-fetch](https://github.com/Hey-AI/openapi-fetch)：基于 OpenAPI 自动生成强类型客户端。  
- [fastapi-mail](https://sabuhish.github.io/fastapi-mail/)：FastAPI 邮件发送能力。  
- [uv](https://docs.astral.sh/uv/)：高速 Python 包与项目管理工具。  
- [Pytest](https://docs.pytest.org/)：Python 主流测试框架。  
- 代码质量工具：
  - [Ruff](https://github.com/astral-sh/ruff)：高性能 Python Linter。
  - [ESLint](https://eslint.org/)：JavaScript/TypeScript 代码质量检查。  
- 热更新监听：
  - 后端：[Watchdog](https://github.com/gorakhargosh/watchdog) 负责监听文件变化。  
  - 前端：[Chokidar](https://github.com/paulmillr/chokidar) 负责监听并触发更新。  
- [Docker](https://www.docker.com/) + [Docker Compose](https://docs.docker.com/compose/)：统一开发与生产运行环境。  
- [MailHog](https://github.com/mailhog/MailHog)：本地开发邮件服务器。  
- [Pre-commit hooks](https://pre-commit.com/)：提交前自动执行格式与质量检查。  
- [OpenAPI JSON schema](https://swagger.io/specification/)：集中管理 API 文档与客户端生成输入。  

有了这套组合，你可以显著减少前后端对接成本，提升开发效率与可维护性。
