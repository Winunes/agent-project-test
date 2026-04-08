"use client";

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

// 忘记密码 Server Action。
import { passwordReset } from "@/components/actions/password-reset-action";
// 管理 Action 状态。
import { useActionState } from "react";
// 提交按钮。
import { SubmitButton } from "@/components/ui/submitButton";
// 跳转组件。
import Link from "next/link";
// 表单级错误组件。
import { FormError } from "@/components/ui/FormError";

// 密码找回页（第一步：提交邮箱）。
export default function Page() {
  // 绑定忘记密码 Action。
  const [state, dispatch] = useActionState(passwordReset, undefined);

  return (
    // 页面容器。
    <div className="flex h-screen w-full items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      {/* 提交后调用 dispatch -> passwordReset。 */}
      <form action={dispatch}>
        <Card className="w-full max-w-sm rounded-lg shadow-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-semibold text-gray-800 dark:text-white">
              Password Recovery
            </CardTitle>
            <CardDescription className="text-sm text-gray-600 dark:text-gray-400">
              Enter your email to receive instructions to reset your password.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-6 p-6">
            {/* 邮箱输入。 */}
            <div className="grid gap-3">
              <Label
                htmlFor="email"
                className="text-gray-700 dark:text-gray-300"
              >
                Email
              </Label>
              <Input
                id="email"
                name="email"
                type="email"
                placeholder="m@example.com"
                required
                className="border-gray-300 dark:border-gray-600"
              />
            </div>
            {/* 提交按钮。 */}
            <SubmitButton text="Send" />
            {/* 错误提示。 */}
            <FormError state={state} />
            {/* 成功提示。 */}
            <div className="mt-2 text-sm text-center text-blue-500">
              {state?.message && <p>{state.message}</p>}
            </div>
            {/* 返回登录页。 */}
            <div className="mt-4 text-center text-sm text-gray-600 dark:text-gray-400">
              <Link
                href="/login"
                className="text-blue-500 hover:text-blue-600 dark:text-blue-400 dark:hover:text-blue-500"
              >
                Back to login
              </Link>
            </div>
          </CardContent>
        </Card>
      </form>
    </div>
  );
}
