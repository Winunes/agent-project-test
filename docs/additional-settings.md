### Production-Ready Authentication & Dashboard features
这个模板内置了可直接使用的认证系统和简洁的仪表盘界面，你可以马上在此基础上开发带用户管理能力的应用。

### Hot Reload on development
项目包含两套热更新机制（后端一套、前端一套），当检测到文件变化时会自动重启本地服务，避免频繁手动重启。

- **后端热更新**：监听后端代码变更。
- **前端热更新**：监听前端代码变更，以及后端生成的 `openapi.json` 文件变更。

### Manual Execution of Hot Reload Commands
你也可以手动执行热更新机制在变更时调用的同一批命令：

1. 导出 `openapi.json`：
   ```bash
   cd fastapi_backend && uv run python -m commands.generate_openapi_schema
   ```
   或使用 Docker：
   ```bash
   docker compose run --rm --no-deps -T backend uv run python -m commands.generate_openapi_schema
   ```

2. 生成前端 API 客户端：
   ```bash
   cd nextjs-frontend && npm run generate-client
   ```
   或使用 Docker：
   ```bash
   docker compose run --rm --no-deps -T frontend npm run generate-client
   ```

### Testing
运行测试前，需要先启动测试数据库容器：
```bash
make docker-up-test-db
```

然后在本地执行测试：
```bash
make test-backend
make test-frontend
```

或者使用 Docker 执行测试：
```bash
make docker-test-backend
make docker-test-frontend
```

### Pre-Commit Setup
为了保证代码质量和风格一致，项目提供了两份 pre-commit 配置：

- `.pre-commit-config.yaml`：用于本地环境执行 pre-commit 检查。
- `.pre-commit-config.docker.yaml`：用于 Docker 环境执行 pre-commit 检查。

### Installing and Activating Pre-Commit Hooks
要启用 pre-commit 钩子，请分别对两份配置执行安装命令：

- **本地配置文件**：
  ```bash
  pre-commit install -c .pre-commit-config.yaml
  ```

- **Docker 配置文件**：
  ```bash
  pre-commit install -c .pre-commit-config.docker.yaml
  ```

### Localhost Email Server Setup
如果要在本地调试邮件功能，需要先启动 [MailHog](https://github.com/mailhog/MailHog)：
```bash
make docker-up-mailhog
```

- **邮件查看地址**：`http://localhost:8025`。

### Running Pre-Commit Checks
手动对所有文件执行 pre-commit 检查：

```bash
pre-commit run --all-files -c .pre-commit-config.yaml
```

或：

```bash
pre-commit run --all-files -c .pre-commit-config.docker.yaml
```

### Updating Pre-Commit Hooks
更新钩子到最新版本：

```bash
pre-commit autoupdate
```

### Alembic Database Migrations
如果你需要新建数据库迁移：
```bash
make docker-db-schema migration_name="add users"
```
然后把迁移应用到数据库：
```bash
make docker-migrate-db
```

### GitHub Actions
项目已预配置 GitHub Actions 来支持 CI/CD；工作流文件位于 `.github/workflows` 目录中，你可以按项目需要进一步定制。

### Secrets Configuration
为保证工作流正常运行，请在 GitHub 仓库中进入 `Settings > Secrets and variables > Actions` 并添加以下密钥：
```text
DATABASE_URL: 主数据库连接字符串。
TEST_DATABASE_URL: 测试数据库连接字符串。
ACCESS_SECRET_KEY: 访问令牌签名密钥。
RESET_PASSWORD_SECRET_KEY: 重置密码功能密钥。
VERIFICATION_SECRET_KEY: 用户/邮箱验证功能密钥。
```

## Makefile

本项目提供了 `Makefile`，用于简化日常操作（如启动前后端、运行测试、构建 Docker 镜像等）。

### Available Commands

在终端执行以下命令可查看所有可用命令及说明：

```bash
make help
```

