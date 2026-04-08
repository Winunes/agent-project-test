// 导入登录/注册接口的错误类型，用于类型安全地解析错误结构。
import { AuthJwtLoginError, RegisterRegisterError } from "@/app/clientService";
// clsx 用于按条件拼接 className 字符串。
import { clsx, type ClassValue } from "clsx";
// twMerge 用于合并 Tailwind 类名并处理冲突（后者覆盖前者）。
import { twMerge } from "tailwind-merge";

// 通用 className 工具：先 clsx，再 twMerge。
export function cn(...inputs: ClassValue[]) {
  // 返回最终可用于 JSX 的 class 字符串。
  return twMerge(clsx(inputs));
}

// 统一提取后端错误文案，便于页面直接展示。
export function getErrorMessage(
  error: RegisterRegisterError | AuthJwtLoginError,
): string {
  // 默认兜底文案，避免出现 undefined。
  let errorMessage = "An unknown error occurred";

  // 情况 1：detail 直接是字符串。
  if (typeof error.detail === "string") {
    // 直接使用后端返回文本。
    errorMessage = error.detail;
  } else if (typeof error.detail === "object" && "reason" in error.detail) {
    // 情况 2：detail 是对象且带 reason 字段。
    errorMessage = error.detail["reason"];
  }

  // 返回统一后的错误信息。
  return errorMessage;
}
