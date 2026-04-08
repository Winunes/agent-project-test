"use client";

// 页面内导航组件。
import Link from "next/link";
// 卡片 UI 组件集合。
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
// 输入框组件。
import { Input } from "@/components/ui/input";
// 标签组件。
import { Label } from "@/components/ui/label";

// 登录 Server Action。
import { login } from "@/components/actions/login-action";
// 客户端处理 Server Action 状态的 Hook。
import { useActionState } from "react";
// 提交按钮组件（会自动显示提交状态）。
import { SubmitButton } from "@/components/ui/submitButton";
// 字段级与表单级错误展示组件。
import { FieldError, FormError } from "@/components/ui/FormError";

// 登录页组件。
export default function Page() {
  // 绑定登录 Action。
  const [state, dispatch] = useActionState(login, undefined);
  return (
    // 页面外层：全屏居中布局。
    <div className="flex h-screen w-full items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      {/* 表单提交会触发 dispatch -> login Server Action。 */}
      <form action={dispatch}>
        <Card className="w-full max-w-sm rounded-lg shadow-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-semibold text-gray-800 dark:text-white">
              Login
            </CardTitle>
            <CardDescription className="text-sm text-gray-600 dark:text-gray-400">
              Enter your email below to log in to your account.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-6 p-6">
            {/* 用户名（邮箱）输入区。 */}
            <div className="grid gap-3">
              <Label
                htmlFor="username"
                className="text-gray-700 dark:text-gray-300"
              >
                Username
              </Label>
              <Input
                id="username"
                name="username"
                type="email"
                placeholder="m@example.com"
                required
                className="border-gray-300 dark:border-gray-600"
              />
              {/* 用户名字段错误。 */}
              <FieldError state={state} field="username" />
            </div>
            {/* 密码输入区。 */}
            <div className="grid gap-3">
              <Label
                htmlFor="password"
                className="text-gray-700 dark:text-gray-300"
              >
                Password
              </Label>
              <Input
                id="password"
                name="password"
                type="password"
                required
                className="border-gray-300 dark:border-gray-600"
              />
              {/* 密码字段错误。 */}
              <FieldError state={state} field="password" />
              {/* 跳转到忘记密码页。 */}
              <Link
                href="/password-recovery"
                className="ml-auto inline-block text-sm text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-500"
              >
                Forgot your password?
              </Link>
            </div>
            {/* 提交登录。 */}
            <SubmitButton text="Sign In" />
            {/* 表单级错误显示。 */}
            <FormError state={state} />
            {/* 跳转注册页。 */}
            <div className="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
              Don&apos;t have an account?{" "}
              <Link
                href="/register"
                className="text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-500"
              >
                Sign up
              </Link>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}
