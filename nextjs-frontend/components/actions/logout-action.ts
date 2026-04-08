"use server";

// 读取/删除登录 Cookie。
import { cookies } from "next/headers";
// 自动生成的退出登录接口函数。
import { authJwtLogout } from "@/app/clientService";
// 退出后跳转到登录页。
import { redirect } from "next/navigation";

// 退出登录 Server Action。
export async function logout() {
  // 读取 cookie 容器。
  const cookieStore = await cookies();
  // 提取 accessToken。
  const token = cookieStore.get("accessToken")?.value;

  // 没有 token 时直接返回提示。
  if (!token) {
    return { message: "No access token found" };
  }

  // 通知后端执行注销（若后端实现了黑名单/会话失效逻辑会在这里生效）。
  const { error } = await authJwtLogout({
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  // 后端返回错误则透传。
  if (error) {
    return { message: error };
  }

  // 前端侧删除 accessToken Cookie。
  cookieStore.delete("accessToken");
  // 跳转登录页，结束当前会话流程。
  redirect(`/login`);
}
