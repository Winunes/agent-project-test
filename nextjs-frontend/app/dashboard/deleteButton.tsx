"use client";

// 删除 Item 的 Server Action。
import { removeItem } from "@/components/actions/items-action";
// 下拉菜单项 UI 组件。
import { DropdownMenuItem } from "@/components/ui/dropdown-menu";

// 组件入参类型：需要目标 Item 的 ID。
interface DeleteButtonProps {
  itemId: string;
}

// 删除按钮组件。
export function DeleteButton({ itemId }: DeleteButtonProps) {
  // 点击后调用删除 Action。
  const handleDelete = async () => {
    await removeItem(itemId);
  };

  return (
    <DropdownMenuItem
      className="text-red-500 cursor-pointer"
      onClick={handleDelete}
    >
      Delete
    </DropdownMenuItem>
  );
}
