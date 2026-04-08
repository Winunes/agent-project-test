// 重新导出自动生成的 OpenAPI 客户端（types + sdk 方法）。
export * from "./openapi-client";

// 引入客户端初始化逻辑（设置 baseURL 等全局配置）。
// 仅导入即可触发执行，不需要显式调用函数。
import "@/lib/clientConfig";
