// defineConfig 用于声明 openapi-ts 代码生成配置。
import { defineConfig } from "@hey-api/openapi-ts";
// dotenv 用于加载 .env.local 中的变量。
import { config } from "dotenv";

// 加载前端本地环境变量文件。
config({ path: ".env.local" });

// 读取 OpenAPI schema 文件路径（例如 openapi.json）。
const openapiFile = process.env.OPENAPI_OUTPUT_FILE;

// 导出 openapi-ts 的配置对象。
export default defineConfig({
  // 输入：后端生成的 OpenAPI JSON 文件。
  input: openapiFile as string,
  // 输出配置。
  output: {
    // 生成后用 prettier 格式化代码。
    format: "prettier",
    // 生成后用 eslint 校验代码。
    lint: "eslint",
    // 生成文件目录。
    path: "app/openapi-client",
  },
  // 使用 axios 客户端插件生成 SDK。
  plugins: ["@hey-api/client-axios"],
});
