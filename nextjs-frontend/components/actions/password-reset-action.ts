"use server";

// 自动生成的“忘记密码/重置密码”接口。
import { resetForgotPassword, resetResetPassword } from "@/app/clientService";
// 成功后跳转登录页。
import { redirect } from "next/navigation";
// 重置密码确认表单的校验规则。
import { passwordResetConfirmSchema } from "@/lib/definitions";
// 错误信息提取工具。
import { getErrorMessage } from "@/lib/utils";

// 第一步：提交邮箱，发送密码重置邮件。
export async function passwordReset(prevState: unknown, formData: FormData) {
  // 组织请求体，只需要 email。
  const input = {
    body: {
      email: formData.get("email") as string,
    },
  };

  try {
    // 调用后端“忘记密码”接口。
    const { error } = await resetForgotPassword(input);
    // 后端业务错误时返回给页面。
    if (error) {
      return { server_validation_error: getErrorMessage(error) };
    }
    // 成功时给页面一条成功提示。
    return { message: "Password reset instructions sent to your email." };
  } catch (err) {
    // 捕获意外异常并返回兜底错误。
    console.error("Password reset error:", err);
    return {
      server_error: "An unexpected error occurred. Please try again later.",
    };
  }
}

// 第二步：携带 token + 新密码，确认重置。
export async function passwordResetConfirm(
  prevState: unknown,
  formData: FormData,
) {
  // 校验 token、密码强度、两次密码一致性。
  const validatedFields = passwordResetConfirmSchema.safeParse({
    token: formData.get("resetToken") as string,
    password: formData.get("password") as string,
    passwordConfirm: formData.get("passwordConfirm") as string,
  });

  // 校验失败时返回字段错误。
  if (!validatedFields.success) {
    return {
      errors: validatedFields.error.flatten().fieldErrors,
    };
  }

  // 取出合法数据（这里只需要 token 和 password）。
  const { token, password } = validatedFields.data;
  // 组织后端接口参数。
  const input = {
    body: {
      token,
      password,
    },
  };
  try {
    // 调用后端“确认重置密码”接口。
    const { error } = await resetResetPassword(input);
    // 若后端有业务错误，返回给页面。
    if (error) {
      return { server_validation_error: getErrorMessage(error) };
    }
    // 成功后跳转登录页。
    redirect(`/login`);
  } catch (err) {
    // 捕获意外异常并返回兜底提示。
    console.error("Password reset confirmation error:", err);
    return {
      server_error: "An unexpected error occurred. Please try again later.",
    };
  }
}
