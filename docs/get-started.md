要把这个模板用于你自己的项目，可以按下面步骤操作：

1. 按照 GitHub 的 [模板仓库指南](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template#creating-a-repository-from-a-template) 用该模板创建新仓库。
2. 克隆你新建的仓库，并进入目录：`cd your-project-name`
3. 确保你已安装 Python 3.12。

完成后，请继续阅读下方的 [Setup](#setup)。

## Setup

### Installing Required Tools

#### 1. uv
`uv` 用于管理后端 Python 依赖，请按 [官方安装指南](https://docs.astral.sh/uv/getting-started/installation/) 安装。

#### 2. Node.js, npm, and pnpm
运行前端前，请先安装 Node.js 和 npm，可参考 [Node.js 安装页面](https://nodejs.org/en/download/)。
安装完成后执行：
```bash
npm install -g pnpm
```

#### 3. Docker
项目建议使用容器化环境运行，请根据你的系统安装 Docker：

- [Install Docker for Mac](https://docs.docker.com/docker-for-mac/install/)
- [Install Docker for Windows](https://docs.docker.com/docker-for-windows/install/)
- [Get Docker CE for Linux](https://docs.docker.com/install/linux/docker-ce/)

#### 4. Docker Compose
请确保已安装 `docker-compose`，可参考 [Docker Compose 安装指南](https://docs.docker.com/compose/install/)。

### Setting Up Environment Variables

**Backend (`fastapi_backend/.env`)：**

将 `.env.example` 复制为 `.env`，然后按需修改变量：
```bash
cd fastapi_backend && cp .env.example .env
```

通常你只需要更新密钥相关字段；可用以下命令生成新密钥：
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

- `DATABASE`、`MAIL`、`OPENAPI`、`CORS`、`FRONTEND_URL` 的本地默认值一般可直接使用。
- 如果使用 Docker，`DATABASE` 和 `MAIL` 已在 Docker Compose 中预配置。
- `OPENAPI_URL` 默认被注释；取消注释后会隐藏 `/docs` 和 `openapi.json`，更适合生产环境。

更多变量说明可查看 `.env.example`。

**Frontend (`nextjs-frontend/.env.local`)：**

将 `.env.example` 复制为 `.env.local`；这些值通常无需改动：
```bash
cd nextjs-frontend && cp .env.example .env.local
```

### Running the Database
建议用 Docker 启动数据库，避免本地数据库安装与兼容问题：
```bash
docker compose build db
docker compose up -d db
```

然后执行数据库迁移：
```bash
make docker-migrate-db
```

### Build the project (without Docker):
如果你想在本机直接跑前后端，可执行以下命令：

#### Backend
进入 `fastapi_backend` 后执行：
```bash
uv sync
```

#### Frontend
进入 `nextjs-frontend` 后执行：
```bash
pnpm install
```

### Build the project (with Docker):

构建前后端容器：
```bash
make docker-build
```

## Running the Application

**不使用 Docker：**

启动 FastAPI：
```bash
make start-backend
```

启动 Next.js：
```bash
make start-frontend
```

**使用 Docker：**

启动 FastAPI 容器：
```bash
make docker-start-backend
```

启动 Next.js 容器：
```bash
make docker-start-frontend
```

- **Backend**：访问 `http://localhost:8000`
- **Frontend**：访问 `http://localhost:3000`

## Important Considerations
- **Environment Variables**：请确保 `.env` 文件内容是最新且正确的。
- **Database Setup**：即使前后端在本机运行，也建议数据库走 Docker，以减少环境冲突。
- **Consistency**：不建议频繁在“本机运行”和“Docker 运行”之间切换，以免出现权限或环境差异问题；选一种方式长期使用更稳。

