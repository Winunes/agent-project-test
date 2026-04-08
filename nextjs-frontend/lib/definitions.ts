// 导入 Zod，用于表单数据校验与类型推导。
import { z } from "zod";

// 抽出“密码规则”作为复用 Schema，避免注册/重置密码重复定义。
const passwordSchema = z
  // 密码必须是字符串。
  .string()
  // 最小长度 8。
  .min(8, "Password should be at least 8 characters.")
  // 必须包含至少一个大写字母。
  .refine((password) => /[A-Z]/.test(password), {
    message: "Password should contain at least one uppercase letter.",
  })
  // 必须包含至少一个特殊字符。
  .refine((password) => /[!@#$%^&*(),.?":{}|<>]/.test(password), {
    message: "Password should contain at least one special character.",
  });

// “确认重置密码”页面的表单校验规则。
export const passwordResetConfirmSchema = z
  // 定义基础字段结构。
  .object({
    // 新密码字段复用通用密码规则。
    password: passwordSchema,
    // 确认密码字段先按普通字符串校验。
    passwordConfirm: z.string(),
    // 重置令牌必须存在（来自 URL 参数）。
    token: z.string({ required_error: "Token is required" }),
  })
  // 二次校验：两次密码必须一致。
  .refine((data) => data.password === data.passwordConfirm, {
    // 不一致时返回提示文案。
    message: "Passwords must match.",
    // 把错误挂到 passwordConfirm 字段上，便于 UI 定位提示。
    path: ["passwordConfirm"],
  });

// 注册表单校验规则。
export const registerSchema = z.object({
  // 密码使用统一密码规则。
  password: passwordSchema,
  // 邮箱必须是合法 email 格式。
  email: z.string().email({ message: "Invalid email address" }),
});

// 登录表单校验规则。
export const loginSchema = z.object({
  // 密码不能为空字符串。
  password: z.string().min(1, { message: "Password is required" }),
  // 用户名（实际传邮箱）不能为空字符串。
  username: z.string().min(1, { message: "Username is required" }),
});

// Item 新建表单校验规则。
export const itemSchema = z.object({
  // 名称必填。
  name: z.string().min(1, { message: "Name is required" }),
  // 描述必填。
  description: z.string().min(1, { message: "Description is required" }),
  // 数量先按字符串接收（来自 formData）。
  quantity: z
    .string()
    // 必填校验。
    .min(1, { message: "Quantity is required" })
    // 转成整数，供后续接口调用。
    .transform((val) => parseInt(val, 10))
    // 校验必须为正整数。
    .refine((val) => Number.isInteger(val) && val > 0, {
      message: "Quantity must be a positive integer",
    }),
});
