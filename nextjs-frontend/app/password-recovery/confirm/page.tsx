"use client";

// 管理 Server Action 状态。
import { useActionState } from "react";
// notFound: 无 token 时返回 404；useSearchParams: 读取 URL 查询参数。
import { notFound, useSearchParams } from "next/navigation";
// 确认重置密码 Server Action。
import { passwordResetConfirm } from "@/components/actions/password-reset-action";
// 提交按钮。
import { SubmitButton } from "@/components/ui/submitButton";
// 卡片 UI 组件集合。
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
// 标签组件。
import { Label } from "@/components/ui/label";
// 输入框组件。
import { Input } from "@/components/ui/input";
// Suspense 用于包裹依赖 searchParams 的渲染逻辑。
import { Suspense } from "react";
// 错误展示组件。
import { FieldError, FormError } from "@/components/ui/FormError";

// 重置密码表单主体。
function ResetPasswordForm() {
  // 绑定确认重置 Action。
  const [state, dispatch] = useActionState(passwordResetConfirm, undefined);
  // 读取当前 URL 参数。
  const searchParams = useSearchParams();
  // 取出 token（邮件链接里带过来）。
  const token = searchParams.get("token");

  // 没有 token 说明链接无效，返回 404 页面。
  if (!token) {
    notFound();
  }

  return (
    // 表单提交触发确认重置动作。
    <form action={dispatch}>
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle className="text-2xl">Reset your Password</CardTitle>
          <CardDescription>
            Enter the new password and confirm it.
          </CardDescription>
        </CardHeader>
        <CardContent className="grid gap-4">
          {/* 新密码字段。 */}
          <div className="grid gap-2">
            <Label htmlFor="password">Password</Label>
            <Input id="password" name="password" type="password" required />
          </div>
          <FieldError state={state} field="password" />
          {/* 确认密码字段。 */}
          <div className="grid gap-2">
            <Label htmlFor="passwordConfirm">Password Confirm</Label>
            <Input
              id="passwordConfirm"
              name="passwordConfirm"
              type="password"
              required
            />
          </div>
          <FieldError state={state} field="passwordConfirm" />
          {/* 隐藏字段：把 token 一并提交给后端。 */}
          <input
            type="hidden"
            id="resetToken"
            name="resetToken"
            value={token}
            readOnly
          />
          {/* 提交按钮。 */}
          <SubmitButton text={"Send"} />
          {/* 表单级错误提示。 */}
          <FormError state={state} />
        </CardContent>
      </Card>
    </form>
  );
}

// 页面组件：外层布局 + Suspense 包裹。
export default function Page() {
  return (
    <div className="flex h-screen w-full items-center justify-center px-4">
      <Suspense fallback={<div>Loading reset form...</div>}>
        <ResetPasswordForm />
      </Suspense>
    </div>
  );
}
