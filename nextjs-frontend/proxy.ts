// NextResponse 用于构造中间件响应（放行、重定向等）。
import { NextResponse } from "next/server";
// NextRequest 是中间件收到的请求类型。
import type { NextRequest } from "next/server";
// 调用后端“当前用户”接口，用于校验 token 是否有效。
import { usersCurrentUser } from "@/app/clientService";

// Next.js 中间件函数：每次访问受保护路由时先执行这里。
export async function proxy(request: NextRequest) {
  // 从 cookie 中读取 accessToken。
  const token = request.cookies.get("accessToken");

  // 没有 token 直接跳转登录页。
  if (!token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // 组装请求头，把 token 作为 Bearer 令牌发给后端。
  const options = {
    headers: {
      Authorization: `Bearer ${token.value}`,
    },
  };

  // 调用后端接口验证当前用户身份。
  const { error } = await usersCurrentUser(options);

  // 若 token 无效或过期，重定向到登录页。
  if (error) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  // 验证通过，继续访问目标页面。
  return NextResponse.next();
}

// 声明中间件匹配范围：仅拦截 /dashboard 下的所有路径。
export const config = {
  matcher: ["/dashboard/:path*"],
};
