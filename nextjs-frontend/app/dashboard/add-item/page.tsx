"use client";

// 输入框组件。
import { Input } from "@/components/ui/input";
// 表单标签组件。
import { Label } from "@/components/ui/label";
// 新增 Item 的 Server Action。
import { addItem } from "@/components/actions/items-action";
// React Hook：处理服务端 Action 的提交状态和返回值。
import { useActionState } from "react";
// 提交按钮组件（含 pending 态）。
import { SubmitButton } from "@/components/ui/submitButton";

// 表单初始状态。
const initialState = { message: "" };

// 新建 Item 页面组件（客户端组件）。
export default function CreateItemPage() {
  // 绑定 addItem Action：state 是返回状态，dispatch 绑定到 form action。
  const [state, dispatch] = useActionState(addItem, initialState);

  return (
    // 页面背景与最小高度设置。
    <div className="bg-gray-50 dark:bg-gray-900 min-h-screen">
      {/* 内容容器。 */}
      <div className="max-w-4xl mx-auto p-6">
        {/* 页面标题区域。 */}
        <header className="mb-6">
          <h1 className="text-3xl font-semibold text-gray-800 dark:text-white">
            Create New Item
          </h1>
          <p className="text-lg text-gray-600 dark:text-gray-400">
            Enter the details of the new item below.
          </p>
        </header>

        {/* 表单：提交到 dispatch，即触发 addItem Server Action。 */}
        <form
          action={dispatch}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8 space-y-6"
        >
          <div className="space-y-6">
            {/* 名称字段。 */}
            <div className="space-y-3">
              <Label
                htmlFor="name"
                className="text-gray-700 dark:text-gray-300"
              >
                Item Name
              </Label>
              <Input
                id="name"
                name="name"
                type="text"
                placeholder="Item name"
                required
                className="w-full border-gray-300 dark:border-gray-600"
              />
              {/* 名称字段错误提示。 */}
              {state.errors?.name && (
                <p className="text-red-500 text-sm">{state.errors.name}</p>
              )}
            </div>

            {/* 描述字段。 */}
            <div className="space-y-3">
              <Label
                htmlFor="description"
                className="text-gray-700 dark:text-gray-300"
              >
                Item Description
              </Label>
              <Input
                id="description"
                name="description"
                type="text"
                placeholder="Description of the item"
                required
                className="w-full border-gray-300 dark:border-gray-600"
              />
              {/* 描述字段错误提示。 */}
              {state.errors?.description && (
                <p className="text-red-500 text-sm">
                  {state.errors.description}
                </p>
              )}
            </div>

            {/* 数量字段。 */}
            <div className="space-y-3">
              <Label
                htmlFor="quantity"
                className="text-gray-700 dark:text-gray-300"
              >
                Quantity
              </Label>
              <Input
                id="quantity"
                name="quantity"
                type="number"
                placeholder="Quantity"
                required
                className="w-full border-gray-300 dark:border-gray-600"
              />
              {/* 数量字段错误提示。 */}
              {state.errors?.quantity && (
                <p className="text-red-500 text-sm">{state.errors.quantity}</p>
              )}
            </div>
          </div>

          {/* 提交按钮。 */}
          <SubmitButton text="Create Item" />

          {/* 表单级错误提示。 */}
          {state?.message && (
            <div className="mt-2 text-center text-sm text-red-500">
              <p>{state.message}</p>
            </div>
          )}
        </form>
      </div>
    </div>
  );
}
