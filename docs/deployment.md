### Overview

该模板支持部署到 **Vercel**，并分别提供 **Frontend** 与 **Backend** 的一键部署按钮。为了保证功能正常，部署前后都需要完成一些配置。

---

### Frontend Deployment

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvintasoftware%2Fnextjs-fastapi-template%2Ftree%2Fmain%2Fnextjs-frontend&env=API_BASE_URL&envDescription=The%20API_BASE_URL%20is%20the%20backend%20URL%20where%20the%20frontend%20sends%20requests.)

- 点击上方 **Frontend** 按钮开始部署。  
- 部署时会要求填写 `API_BASE_URL`，先填占位值（例如 `https://`）即可，后续再替换为后端地址。  
- 后续配置请继续看 [Post-Deployment Configuration](#post-deployment-configuration)。

### Backend Deployment

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https%3A%2F%2Fgithub.com%2Fvintasoftware%2Fnextjs-fastapi-template%2Ftree%2Fmain%2Ffastapi_backend&env=CORS_ORIGINS,ACCESS_SECRET_KEY,RESET_PASSWORD_SECRET_KEY,VERIFICATION_SECRET_KEY&stores=%5B%7B%22type%22%3A%22postgres%22%7D%5D)

- 点击上方 **Backend** 按钮开始部署。  
- 先按向导初始化数据库，连接配置默认会自动处理，一般可直接通过。  
- 部署过程中会要求配置以下环境变量：

  - **CORS_ORIGINS**  
    - 初始可设为 `["*"]` 以允许所有来源，前端部署完成后再改成前端真实域名。

  - **ACCESS_SECRET_KEY**, **RESET_PASSWORD_SECRET_KEY**, **VERIFICATION_SECRET_KEY**  
    - 部署时可以先临时填普通字符串（例如 `examplekey`），但上线后请在 **Post-Deployment Configuration** 中替换为安全密钥。

- 后续配置请继续看 [Post-Deployment Configuration](#post-deployment-configuration)。


## CI (GitHub Actions) Setup for Production Deployment

仓库根目录提供了 `prod-backend-deploy.yml` 与 `prod-frontend-deploy.yml`，用于生产环境的 GitHub Actions 持续部署；把它们移动到 `.github/workflows/` 即可启用。

可用以下命令移动：
```bash
mv prod-backend-deploy.yml .github/workflows/prod-backend-deploy.yml
mv prod-frontend-deploy.yml .github/workflows/prod-frontend-deploy.yml
```

### Prerequisites
1. **Create a Vercel Token**：  
   - 先生成 [Vercel Access Token](https://vercel.com/account/tokens)。  
   - 把它保存到 GitHub Secrets，变量名为 `VERCEL_TOKEN`。

2. **Install Vercel CLI**：  
   ```bash
   pnpm i -g vercel@latest
   ```

3. 登录 Vercel 账号：  
   ```bash
   vercel login
   ```

### Database Creation (Required)

1. **Choosing a Database**
   - 你可以使用自托管数据库，也可以使用与 Vercel 集成较好的 [Neon](https://neon.tech/docs/introduction)。

2. **Setting Up a Neon Database via Vercel**
   - 在 Vercel 的 **Projects dashboard** 页面进入 **Storage**。  
   - 选择 **Create a Database** 创建 Neon 数据库。

3. **Configuring the Database URL**
   - 数据库创建后，复制 Neon 提供的 **Database URL**。  
   - 在项目 **Environment Variables** 中配置到 `DATABASE_URL`。

4. **Migrating the Database**
   - GitHub Actions 部署时会自动执行数据库迁移，创建所需表和结构。

### Frontend Setup

1. 关联 `nextjs-frontend` 项目。

2. 进入 `nextjs-frontend` 目录并执行：
   ```bash
   cd nextjs-frontend
   vercel link
   ```

3. 按提示选择：
   - Link to existing project? `No`
   - Modify settings? `No`

4. 保存项目 ID 并写入 GitHub Secrets：
   - 打开 `nextjs-frontend/.vercel/project.json`，把以下值添加到仓库 Secrets：
     - `projectId` -> `VERCEL_PROJECT_ID_FRONTEND`
     - `orgId` -> `VERCEL_ORG_ID`

### Backend Setup

1. 关联 `fastapi_backend` 项目。

2. 进入 `fastapi_backend` 目录并执行：
   ```bash
   cd fastapi_backend
   vercel link --local-config=vercel.prod.json
   ```
   - 这里使用了专用配置文件，因此需要传 `--local-config`。

3. 按提示选择：
   - Link to existing project? `No`
   - Modify settings? `No`

4. 保存项目 ID 并写入 GitHub Secrets：
   - 打开 `fastapi_backend/.vercel/project.json`，把以下值添加到仓库 Secrets：
     - `projectId` -> `VERCEL_PROJECT_ID_BACKEND`
     - `orgId` -> `VERCEL_ORG_ID`（如果之前已配置可复用）

5. 更新 `requirements.txt`：
   ```bash
   cd fastapi_backend
   uv export > requirements.txt
   ```
   - 当 `uv.lock` 发生变化时，Vercel 部署前通常需要重新导出 `requirements.txt`。

### Notes
- 所有配置完成后，执行 `git push` 即可触发自动部署。  
- 前端和后端需要分别完成各自的 Vercel 关联与密钥配置。  
- 更多命令可参考 [Vercel CLI Documentation](https://vercel.com/docs/cli)。  
- `project_id` 可在 Vercel 项目设置页查看。  
- `organization_id` 可在 Vercel 组织设置页查看。  

## Post-Deployment Configuration

### Frontend
- 进入已部署前端项目的 **Settings** 页面。  
- 打开 **Environment Variables**。  
- 后端部署完成后，把 `API_BASE_URL` 更新为后端实际地址。

### Backend
- 进入已部署后端项目的 **Settings** 页面。  
- 打开 **Environment Variables**，并把以下变量更新为安全值：

  - **CORS_ORIGINS**  
    - 当前端上线后，请将 `["*"]` 改为前端真实域名。

  - **ACCESS_SECRET_KEY**  
    - 用于 API 访问令牌签名，请设置为强随机密钥。

  - **RESET_PASSWORD_SECRET_KEY**  
    - 用于重置密码流程，请设置为强随机密钥。

  - **VERIFICATION_SECRET_KEY**  
    - 用于用户验证流程，请设置为强随机密钥。

- 密钥配置细节可参考 [Setting up Environment Variables](get-started.md#setting-up-environment-variables)。

### Fluid serverless activation
[Fluid](https://vercel.com/docs/functions/fluid-compute) 是 Vercel 新的 Serverless 并发模型：单次函数执行可处理多个请求，而不是每个请求都冷启动新实例，从而提升性能、减少冷启动并优化资源利用率。

可按这份 [官方指南](https://vercel.com/docs/functions/fluid-compute#how-to-enable-fluid-compute) 开启 Fluid。
