/* eslint-disable @typescript-eslint/no-require-imports */
// 引入 chokidar：文件监听库。
const chokidar = require("chokidar");
// 引入 exec：执行 shell 命令。
const { exec } = require("child_process");
// 引入 dotenv：读取 .env.local。
const { config } = require("dotenv");

// 加载前端环境变量。
config({ path: ".env.local" });

// 读取要监听的 OpenAPI 文件路径。
const openapiFile = process.env.OPENAPI_OUTPUT_FILE;
// 监听该文件变化。
chokidar.watch(openapiFile).on("change", (path) => {
  // 文件变化后打印日志。
  console.log(`File ${path} has been modified. Running generate-client...`);
  // 执行前端 SDK 生成命令。
  exec("pnpm run generate-client", (error, stdout, stderr) => {
    // 命令执行报错时输出错误并结束。
    if (error) {
      console.error(`Error: ${error.message}`);
      return;
    }
    // 若有标准错误输出，也打印出来。
    if (stderr) {
      console.error(`stderr: ${stderr}`);
      return;
    }
    // 打印标准输出（生成成功日志）。
    console.log(`stdout: ${stdout}`);
  });
});
