# 项目结构一句话说明

本清单覆盖根目录文件夹、根目录文件、Git 跟踪文件及本地常见环境文件（如 `.env`），不展开 `.git` 内部对象与 `.venv/.mypy_cache/__pycache__` 等缓存产物。

## 根目录文件夹

- `.git`：Git 版本管理数据库与历史元数据目录，通常不手动修改内部文件。
- `.github`：存放 GitHub 协作模板与 CI/CD 工作流配置。
- `.idea`：JetBrains IDE 的本地工程配置目录，主要服务开发者本机编辑体验。
- `docs`：项目文档站点源文件与文档资源目录。
- `fastapi_backend`：后端服务代码、数据库迁移、测试与部署配置目录。
- `local-shared-data`：前后端共享的 OpenAPI 文件等中间产物目录。
- `nextjs-frontend`：前端应用代码、测试、构建配置与静态资源目录。
- `overrides`：MkDocs 主题覆盖模板目录。

## 根目录文件

- `.gitattributes`：统一跨平台换行符和二进制文件处理策略的 Git 属性配置。
- `.gitignore`：定义 Git 提交时需要忽略的本地文件与目录规则。
- `.pre-commit-config.docker.yaml`：在 Docker 场景下执行 pre-commit 检查的配置文件。
- `.pre-commit-config.yaml`：代码提交前自动格式化与静态检查的 pre-commit 配置。
- `CHANGELOG.md`：记录模板版本变更历史与发布说明。
- `docker-compose.yml`：一键编排前端、后端、数据库和邮件服务的容器配置。
- `LICENSE.txt`：项目开源许可证文本文件。
- `Makefile`：封装常用开发、测试和 Docker 命令的快捷入口。
- `mkdocs.yml`：文档站点构建与导航配置文件。
- `prod-backend-deploy.yml`：后端生产部署流程或模板配置文件。
- `prod-frontend-deploy.yml`：前端生产部署流程或模板配置文件。
- `README.md`：项目总览、技术栈和快速开始说明。

## `.github` 目录文件

- `.github/PULL_REQUEST_TEMPLATE.md`：规范 PR 描述内容的模板文件。
- `.github/workflows/ci.yml`：持续集成流水线配置（如测试、检查、构建）。
- `.github/workflows/pre-commit.yml`：在 CI 中执行 pre-commit 检查的工作流配置。
- `.github/workflows/release.yml`：自动化发布流程的工作流配置。

## `.idea` 目录文件

- `.idea/agent-project-test.iml`：IDEA 工程模块定义文件。
- `.idea/modules.xml`：IDEA 模块列表与映射配置文件。
- `.idea/vcs.xml`：IDEA 版本控制集成设置文件。
- `.idea/workspace.xml`：IDEA 工作区个性化配置文件。
- `.idea/inspectionProfiles/profiles_settings.xml`：IDEA 代码检查规则配置文件。

## `docs` 目录文件

- `docs/README.md`：文档站点的首页内容文件。
- `docs/CHANGELOG.md`：文档本身的更新记录文件。
- `docs/additional-settings.md`：补充配置项与进阶设置说明文档。
- `docs/contributing.md`：贡献流程、规范与协作指南文档。
- `docs/deployment.md`：部署步骤与环境要求说明文档。
- `docs/get-started.md`：从零启动模板的入门操作指南。
- `docs/support.md`：常见支持渠道与问题反馈说明文档。
- `docs/technology-selection.md`：技术选型与依赖组件说明文档。
- `docs/stylesheets/extra.css`：文档站点的样式覆盖文件。
- `docs/images/banner.png`：文档页头横幅图片资源。
- `docs/images/footer-logo.svg`：文档页脚 Logo 矢量图资源。
- `docs/images/github-favicon.png`：文档或仓库展示用图标资源。
- `docs/images/nav-logo.png`：文档导航栏 Logo 图片资源。
- `docs/images/thumbnail.png`：文档/项目缩略图资源。
- `docs/images/vinta-logo.png`：品牌或合作方 Logo 图片资源。

## `fastapi_backend` 目录文件

- `fastapi_backend/.env`：后端本地运行时环境变量文件（本地私有）。
- `fastapi_backend/.env.example`：后端环境变量模板文件。
- `fastapi_backend/.gitignore`：后端子目录的忽略规则配置。
- `fastapi_backend/Dockerfile`：后端服务镜像构建脚本。
- `fastapi_backend/alembic.ini`：Alembic 数据库迁移工具主配置。
- `fastapi_backend/mypy.ini`：后端静态类型检查配置。
- `fastapi_backend/pyproject.toml`：后端 Python 项目元数据与依赖声明。
- `fastapi_backend/pytest.ini`：后端测试框架 pytest 配置。
- `fastapi_backend/requirements.txt`：后端依赖列表（兼容 pip 方式）。
- `fastapi_backend/start.sh`：后端开发启动与 watcher 联动脚本。
- `fastapi_backend/uv.lock`：uv 锁定的后端依赖精确版本文件。
- `fastapi_backend/vercel.json`：后端在 Vercel 的部署配置（开发/默认）。
- `fastapi_backend/vercel.prod.json`：后端在 Vercel 的生产部署配置。
- `fastapi_backend/watcher.py`：监听后端文件变更并自动生成 OpenAPI 的脚本。
- `fastapi_backend/api/index.py`：后端 Serverless 入口适配文件。

## `fastapi_backend/alembic_migrations` 目录文件

- `fastapi_backend/alembic_migrations/README`：数据库迁移目录使用说明文件。
- `fastapi_backend/alembic_migrations/env.py`：Alembic 迁移执行环境初始化脚本。
- `fastapi_backend/alembic_migrations/script.py.mako`：Alembic 迁移文件模板。
- `fastapi_backend/alembic_migrations/versions/402d067a8b92_added_user_table.py`：创建用户表的迁移脚本。
- `fastapi_backend/alembic_migrations/versions/b389592974f8_add_item_model.py`：创建 Item 表的迁移脚本。

## `fastapi_backend/app` 目录文件

- `fastapi_backend/app/__init__.py`：后端应用包初始化文件。
- `fastapi_backend/app/config.py`：集中定义并加载后端环境配置。
- `fastapi_backend/app/database.py`：数据库引擎、会话与依赖注入定义。
- `fastapi_backend/app/email.py`：邮件配置与密码重置邮件发送逻辑。
- `fastapi_backend/app/main.py`：FastAPI 应用入口与路由注册中心。
- `fastapi_backend/app/models.py`：SQLAlchemy ORM 数据模型定义。
- `fastapi_backend/app/schemas.py`：Pydantic 请求/响应数据结构定义。
- `fastapi_backend/app/users.py`：用户鉴权、密码策略与 fastapi-users 配置。
- `fastapi_backend/app/utils.py`：后端通用工具函数集合。
- `fastapi_backend/app/email_templates/__init__.py`：邮件模板包初始化文件。
- `fastapi_backend/app/email_templates/password_reset.html`：密码重置邮件 HTML 模板。
- `fastapi_backend/app/routes/__init__.py`：路由子包初始化文件。
- `fastapi_backend/app/routes/items.py`：Item 资源的增删查分页接口路由。

## `fastapi_backend/commands` 目录文件

- `fastapi_backend/commands/__init__.py`：命令模块包初始化文件。
- `fastapi_backend/commands/generate_openapi_schema.py`：从 FastAPI 应用导出 OpenAPI JSON 的命令脚本。

## `fastapi_backend/tests` 目录文件

- `fastapi_backend/tests/__init__.py`：测试包初始化文件。
- `fastapi_backend/tests/conftest.py`：pytest 全局 fixture 与测试环境配置。
- `fastapi_backend/tests/test_database.py`：数据库层相关测试用例。
- `fastapi_backend/tests/test_email.py`：邮件发送逻辑相关测试用例。
- `fastapi_backend/tests/main/__init__.py`：主应用测试子包初始化文件。
- `fastapi_backend/tests/main/test_main.py`：主入口与基础接口行为测试。
- `fastapi_backend/tests/routes/__init__.py`：路由测试子包初始化文件。
- `fastapi_backend/tests/routes/test_items.py`：Item 路由行为测试用例。
- `fastapi_backend/tests/utils/__init__.py`：工具测试子包初始化文件。
- `fastapi_backend/tests/utils/test_utils.py`：工具函数行为测试用例。
- `fastapi_backend/tests/commands/__init__.py`：命令测试子包初始化文件。
- `fastapi_backend/tests/commands/test_generate_openapi_schema.py`：OpenAPI 生成命令测试用例。
- `fastapi_backend/tests/commands/files/openapi_test.json`：命令测试输入用 OpenAPI 样例文件。
- `fastapi_backend/tests/commands/files/openapi_test_output.json`：命令测试期望输出样例文件。

## `local-shared-data` 目录文件

- `local-shared-data/openapi.json`：前后端共享的 OpenAPI 描述文件。

## `nextjs-frontend` 目录文件

- `nextjs-frontend/.env.local`：前端本地运行环境变量文件（本地私有）。
- `nextjs-frontend/.env.example`：前端环境变量模板文件。
- `nextjs-frontend/.gitignore`：前端子目录忽略规则配置。
- `nextjs-frontend/.prettierignore`：前端代码格式化忽略配置。
- `nextjs-frontend/Dockerfile`：前端服务镜像构建脚本。
- `nextjs-frontend/components.json`：shadcn/ui 组件生成器配置文件。
- `nextjs-frontend/eslint.config.mjs`：前端 ESLint 规则配置文件。
- `nextjs-frontend/jest.config.ts`：前端 Jest 测试配置文件。
- `nextjs-frontend/next.config.mjs`：Next.js 应用构建与运行配置文件。
- `nextjs-frontend/openapi-ts.config.ts`：OpenAPI 客户端代码生成配置文件。
- `nextjs-frontend/openapi.json`：前端侧使用的 OpenAPI 输入文件。
- `nextjs-frontend/package.json`：前端依赖与脚本入口配置文件。
- `nextjs-frontend/package-lock.json`：npm 依赖锁定文件。
- `nextjs-frontend/pnpm-lock.yaml`：pnpm 依赖锁定文件。
- `nextjs-frontend/pnpm-workspace.yaml`：pnpm workspace 配置文件。
- `nextjs-frontend/postcss.config.js`：PostCSS 构建配置文件。
- `nextjs-frontend/proxy.ts`：受保护路由鉴权拦截中间件。
- `nextjs-frontend/start.sh`：前端开发服务与 watcher 联动启动脚本。
- `nextjs-frontend/tailwind.config.js`：Tailwind CSS 主题与扫描配置。
- `nextjs-frontend/tsconfig.json`：TypeScript 编译配置文件。
- `nextjs-frontend/vercel.json`：前端在 Vercel 的部署配置文件。
- `nextjs-frontend/watcher.js`：监听 OpenAPI 变更并自动重生前端 SDK 的脚本。

## `nextjs-frontend/__tests__` 目录文件

- `nextjs-frontend/__tests__/login.test.tsx`：登录表单行为测试用例。
- `nextjs-frontend/__tests__/loginPage.test.tsx`：登录页面渲染测试用例。
- `nextjs-frontend/__tests__/passwordReset.test.tsx`：密码找回流程测试用例。
- `nextjs-frontend/__tests__/passwordResetConfirm.test.tsx`：密码重置确认逻辑测试用例。
- `nextjs-frontend/__tests__/passwordResetConfirmPage.test.tsx`：密码重置确认页渲染测试用例。
- `nextjs-frontend/__tests__/passwordResetPage.test.tsx`：密码找回页渲染测试用例。
- `nextjs-frontend/__tests__/register.test.ts`：注册逻辑测试用例。
- `nextjs-frontend/__tests__/registerPage.test.tsx`：注册页面渲染测试用例。

## `nextjs-frontend/app` 目录文件

- `nextjs-frontend/app/clientService.ts`：导出并初始化自动生成的 API 客户端服务入口。
- `nextjs-frontend/app/globals.css`：全站全局样式定义文件。
- `nextjs-frontend/app/layout.tsx`：前端根布局组件与全局字体配置。
- `nextjs-frontend/app/page.tsx`：前端首页页面组件。
- `nextjs-frontend/app/login/page.tsx`：登录页面组件。
- `nextjs-frontend/app/register/page.tsx`：注册页面组件。
- `nextjs-frontend/app/password-recovery/page.tsx`：忘记密码页面组件。
- `nextjs-frontend/app/password-recovery/confirm/page.tsx`：密码重置确认页面组件。
- `nextjs-frontend/app/dashboard/layout.tsx`：仪表盘路由共享布局组件。
- `nextjs-frontend/app/dashboard/page.tsx`：仪表盘列表主页面组件。
- `nextjs-frontend/app/dashboard/deleteButton.tsx`：仪表盘删除条目按钮组件。
- `nextjs-frontend/app/dashboard/add-item/page.tsx`：新增条目页面组件。
- `nextjs-frontend/app/fonts/GeistMonoVF.woff`：前端等宽字体文件资源。
- `nextjs-frontend/app/fonts/GeistVF.woff`：前端无衬线字体文件资源。

## `nextjs-frontend/app/openapi-client` 目录文件

- `nextjs-frontend/app/openapi-client/index.ts`：自动生成 SDK 的统一导出入口。
- `nextjs-frontend/app/openapi-client/types.gen.ts`：自动生成的接口类型定义文件。
- `nextjs-frontend/app/openapi-client/sdk.gen.ts`：自动生成的接口调用方法文件。
- `nextjs-frontend/app/openapi-client/client.gen.ts`：自动生成的客户端实例配置文件。
- `nextjs-frontend/app/openapi-client/client/index.ts`：自动生成客户端子模块导出入口。
- `nextjs-frontend/app/openapi-client/client/types.gen.ts`：自动生成客户端底层类型定义文件。
- `nextjs-frontend/app/openapi-client/client/utils.gen.ts`：自动生成客户端工具函数文件。
- `nextjs-frontend/app/openapi-client/client/client.gen.ts`：自动生成客户端封装实现文件。
- `nextjs-frontend/app/openapi-client/core/auth.gen.ts`：自动生成鉴权相关底层处理代码。
- `nextjs-frontend/app/openapi-client/core/bodySerializer.gen.ts`：自动生成请求体序列化逻辑。
- `nextjs-frontend/app/openapi-client/core/params.gen.ts`：自动生成请求参数处理逻辑。
- `nextjs-frontend/app/openapi-client/core/pathSerializer.gen.ts`：自动生成路径参数序列化逻辑。
- `nextjs-frontend/app/openapi-client/core/serverSentEvents.gen.ts`：自动生成 SSE 相关底层支持代码。
- `nextjs-frontend/app/openapi-client/core/types.gen.ts`：自动生成核心层类型定义文件。
- `nextjs-frontend/app/openapi-client/core/utils.gen.ts`：自动生成核心层工具函数文件。

## `nextjs-frontend/components` 目录文件

- `nextjs-frontend/components/page-pagination.tsx`：通用分页控制条组件。
- `nextjs-frontend/components/page-size-selector.tsx`：每页条数切换下拉组件。
- `nextjs-frontend/components/actions/items-action.ts`：条目查询、新增、删除的服务端动作集合。
- `nextjs-frontend/components/actions/login-action.ts`：登录表单提交的服务端动作实现。
- `nextjs-frontend/components/actions/logout-action.ts`：登出动作实现并清理登录态。
- `nextjs-frontend/components/actions/password-reset-action.ts`：密码找回与重置动作实现。
- `nextjs-frontend/components/actions/register-action.ts`：注册表单提交的服务端动作实现。
- `nextjs-frontend/components/ui/FormError.tsx`：表单级与字段级错误展示组件。
- `nextjs-frontend/components/ui/avatar.tsx`：头像 UI 基础组件。
- `nextjs-frontend/components/ui/badge.tsx`：徽章 UI 基础组件。
- `nextjs-frontend/components/ui/breadcrumb.tsx`：面包屑 UI 基础组件。
- `nextjs-frontend/components/ui/button.tsx`：按钮 UI 基础组件。
- `nextjs-frontend/components/ui/card.tsx`：卡片 UI 基础组件。
- `nextjs-frontend/components/ui/dropdown-menu.tsx`：下拉菜单 UI 基础组件。
- `nextjs-frontend/components/ui/form.tsx`：表单结构 UI 基础组件。
- `nextjs-frontend/components/ui/input.tsx`：输入框 UI 基础组件。
- `nextjs-frontend/components/ui/label.tsx`：标签 UI 基础组件。
- `nextjs-frontend/components/ui/select.tsx`：选择器 UI 基础组件。
- `nextjs-frontend/components/ui/submitButton.tsx`：带提交状态的按钮组件。
- `nextjs-frontend/components/ui/table.tsx`：表格 UI 基础组件。
- `nextjs-frontend/components/ui/tabs.tsx`：标签页 UI 基础组件。

## `nextjs-frontend/lib` 目录文件

- `nextjs-frontend/lib/clientConfig.ts`：统一设置 API 客户端基础配置。
- `nextjs-frontend/lib/definitions.ts`：Zod 表单校验规则与共享数据定义。
- `nextjs-frontend/lib/utils.ts`：前端通用工具函数与错误文案提取逻辑。

## `nextjs-frontend/public` 目录文件

- `nextjs-frontend/public/images/vinta.png`：前端页面展示用静态图片资源。

## `overrides` 目录文件

- `overrides/main.html`：MkDocs 主题主模板覆盖文件。



```
一、总览主链
浏览器页面(Next.js)
→ Next 中间件 proxy(request) [只匹配 /dashboard/:path*]
→ Dashboard Server Component / Server Action
→ clientService.ts 重新导出的 OpenAPI SDK
→ sdk.gen.ts 里的 readItem/createItem/deleteItem/usersCurrentUser
→ client.gen.ts 的 beforeRequest() + request()
→ Axios 发 HTTP 请求到 FastAPI
→ FastAPI 的 CORSMiddleware（后端中间件）
→ FastAPI 路由函数（/items、/users/me、/auth/jwt/login）
→ Depends 注入：current_active_user + get_async_session
→ SQLAlchemy 异步查询/写入
→ PostgreSQL
→ SQLAlchemy 结果转 Pydantic 响应
→ Axios 收到 response.data
→ Server Action/Server Component 返回
→ Next.js 渲染 HTML/更新 UI
→ 浏览器展示
```

```
二、访问 Dashboard（鉴权校验链）
GET /dashboard
→ proxy.ts: 读 accessToken cookie
→ 无 token：redirect /login（结束）
→ 有 token：usersCurrentUser({ Authorization: Bearer ... })
→ FastAPI /users/me
→ current_active_user 校验 JWT
→ 校验失败：401 → proxy 重定向 /login
→ 校验成功：NextResponse.next()
→ 继续进入 /dashboard 页面逻辑
```

```
三、登录链（authJwtLogin）
登录页 form 提交
→ useActionState 触发 login Server Action
→ login-action.ts: zod 校验
→ authJwtLogin(input)
→ POST /auth/jwt/login
→ FastAPI Users: authenticate(email/password)
→ 成功生成 JWT(access_token)
→ 返回 {access_token, token_type}
→ Server Action 写 cookie: accessToken
→ redirect /dashboard
→ 下次访问 /dashboard 时由 proxy 校验并放行
```

```
四、读列表链（/items）
Dashboard page.tsx
→ fetchItems(page,size) Server Action
→ readItem({ query, headers.Authorization })
→ GET /items/
→ FastAPI read_item()
→ Depends(current_active_user) 先鉴权
→ Depends(get_async_session) 拿 DB session
→ select(Item).filter(Item.user_id == user.id)
→ PostgreSQL 返回该用户分页数据
→ Page[ItemRead] JSON 返回前端
→ Table 渲染 items
```

```
五、新增链（/items POST）
Add Item 页面 form 提交
→ addItem Server Action
→ zod 校验表单
→ createItem({ body, Authorization })
→ POST /items/
→ FastAPI create_item()
→ current_active_user 鉴权
→ Item(**item.model_dump(), user_id=user.id)
→ db.add → db.commit → db.refresh
→ 返回新记录
→ Server Action redirect /dashboard
→ 页面重新读取列表并展示新数据
```

```
六、删除链（/items/{id} DELETE）
点击 DeleteButton
→ removeItem(itemId) Server Action
→ deleteItem({ path.item_id, Authorization })
→ DELETE /items/{item_id}
→ FastAPI delete_item()
→ current_active_user 鉴权
→ 查询 Item.id == item_id 且 Item.user_id == user.id
→ 找不到：404（无权限或不存在）
→ 找到：db.delete → db.commit
→ 返回成功消息
→ revalidatePath('/dashboard')
→ 前端列表刷新
```

```
七、中间件到底在哪里（最简图）
浏览器请求 /dashboard
→ Next proxy 中间件（前端入口守卫）
→ Next 页面/Action
→ FastAPI CORSMiddleware（后端全局中间件）
→ FastAPI 路由 + Depends 依赖
→ 数据库
```

