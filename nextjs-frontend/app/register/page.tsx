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

// 注册 Server Action。
import { register } from "@/components/actions/register-action";
// 绑定并管理 Action 状态。
import { useActionState } from "react";
// 提交按钮组件。
import { SubmitButton } from "@/components/ui/submitButton";
// 页面跳转组件。
import Link from "next/link";
// 错误展示组件。
import { FieldError, FormError } from "@/components/ui/FormError";

// 注册页组件。
export default function Page() {
  // 绑定注册 Action。
  const [state, dispatch] = useActionState(register, undefined);
  return (
    // 页面容器：全屏居中。
    <div className="flex h-screen w-full items-center justify-center bg-gray-50 dark:bg-gray-900 px-4">
      {/* 表单提交触发 register Action。 */}
      <form action={dispatch}>
        <Card className="w-full max-w-sm rounded-lg shadow-lg border border-gray-300 dark:border-gray-700 bg-white dark:bg-gray-800">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl font-semibold text-gray-800 dark:text-white">
              Sign Up
            </CardTitle>
            <CardDescription className="text-sm text-gray-600 dark:text-gray-400">
              Enter your email and password below to create your account.
            </CardDescription>
          </CardHeader>
          <CardContent className="grid gap-6 p-6">
            {/* 邮箱字段。 */}
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
              <FieldError state={state} field="email" />
            </div>
            {/* 密码字段。 */}
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
              <FieldError state={state} field="password" />
            </div>
            {/* 提交注册。 */}
            <SubmitButton text="Sign Up" />
            {/* 表单级错误。 */}
            <FormError state={state} />
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
