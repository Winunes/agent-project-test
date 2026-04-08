"use client";

// 下拉选择框组件集合。
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
// 客户端路由对象，用于跳转并更新查询参数。
import { useRouter } from "next/navigation";

// 组件入参类型：当前每页条数。
interface PageSizeSelectorProps {
  currentSize: number;
}

// 每页条数选择器组件。
export function PageSizeSelector({ currentSize }: PageSizeSelectorProps) {
  // 获取路由实例。
  const router = useRouter();
  // 预设可选页容量。
  const pageSizeOptions = [5, 10, 20, 50, 100];

  // 当用户修改每页条数时，回到第一页并带上新的 size 参数。
  const handleSizeChange = (newSize: string) => {
    router.push(`/dashboard?page=1&size=${newSize}`);
  };

  return (
    <div className="flex items-center space-x-2">
      <span className="text-sm text-gray-600">Items per page:</span>
      <Select value={currentSize.toString()} onValueChange={handleSizeChange}>
        <SelectTrigger className="w-20">
          <SelectValue />
        </SelectTrigger>
        <SelectContent>
          {pageSizeOptions.map((option) => (
            <SelectItem key={option} value={option.toString()}>
              {option}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
    </div>
  );
}
