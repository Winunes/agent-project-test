// 导入自动生成客户端中的底层 client 实例。
import { client } from "@/app/openapi-client/client.gen";

// 封装客户端配置逻辑，便于后续扩展（如统一 headers、超时等）。
const configureClient = () => {
  // 从环境变量读取后端 API 根地址。
  const baseURL = process.env.API_BASE_URL;

  // 将 baseURL 注入 SDK 客户端，后续所有接口调用都会使用它。
  client.setConfig({
    baseURL: baseURL,
  });
};

// 模块加载时立即执行一次初始化。
configureClient();
