"use server";

// redirect 用于注册成功后跳转登录页。
import { redirect } from "next/navigation";

// 自动生成的注册接口函数。
import { registerRegister } from "@/app/clientService";

// 注册表单校验规则。
import { registerSchema } from "@/lib/definitions";
// 错误文案提取工具。
import { getErrorMessage } from "@/lib/utils";

// 注册 Server Action：由注册表单提交触发。
export async function register(prevState: unknown, formData: FormData) {
  // 先校验用户输入（邮箱格式、密码复杂度等）。
  const validatedFields = registerSchema.safeParse({
    // 读取邮箱字段。
    email: formData.get("email") as string,
    // 读取密码字段。
    password: formData.get("password") as string,
  });

  // 校验失败时返回字段错误给页面展示。
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  // 取出合法数据。
  const { email, password } = validatedFields.data;

  // 组装接口请求体。
  const input = {
    body: {
      email,
      password,
    },
  };
  try {
    // 调用后端注册接口。
    const { error } = await registerRegister(input);
    // 若后端返回业务校验错误，透传到 UI。
    if (error) {
      return { server_validation_error: getErrorMessage(error) };
    }
  } catch (err) {
    // 捕获意外异常。
    console.error("Registration error:", err);
    return {
      server_error: "An unexpected error occurred. Please try again later.",
    };
  }
  // 注册成功后跳转登录页。
  redirect(`/login`);
}
