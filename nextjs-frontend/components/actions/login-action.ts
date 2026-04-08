"use server";

// 读取/写入 Cookie（服务端 Action 可直接操作）。
import { cookies } from "next/headers";

// 自动生成的登录接口函数。
import { authJwtLogin } from "@/app/clientService";
// redirect 用于服务端直接跳转页面。
import { redirect } from "next/navigation";
// 登录表单 Zod 校验规则。
import { loginSchema } from "@/lib/definitions";
// 统一错误文案提取函数。
import { getErrorMessage } from "@/lib/utils";

// 登录 Server Action：由登录表单提交触发。
export async function login(prevState: unknown, formData: FormData) {
  // 先做前端层校验，避免把明显非法数据发给后端。
  const validatedFields = loginSchema.safeParse({
    // 从 formData 读取 username（模板中实际填的是 email）。
    username: formData.get("username") as string,
    // 从 formData 读取 password。
    password: formData.get("password") as string,
  });

  // 若校验失败，返回字段错误给 UI 显示。
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  // 解构出已经校验过的数据。
  const { username, password } = validatedFields.data;

  // 组织接口入参对象（符合 openapi 生成函数的签名）。
  const input = {
    body: {
      username,
      password,
    },
  };

  try {
    // 调用后端登录接口。
    const { data, error } = await authJwtLogin(input);
    // 若后端返回业务错误（如账号密码错误），返回给页面展示。
    if (error) {
      return { server_validation_error: getErrorMessage(error) };
    }
    // 登录成功：把 access_token 写入 Cookie，供后续受保护请求使用。
    (await cookies()).set("accessToken", data.access_token);
  } catch (err) {
    // 兜底异常处理（网络错误/意外错误）。
    console.error("Login error:", err);
    return {
      server_error: "An unexpected error occurred. Please try again later.",
    };
  }
  // 登录成功后跳转到仪表盘页面。
  redirect("/dashboard");
}
