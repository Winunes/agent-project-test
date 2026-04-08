// 按钮组件。
import { Button } from "@/components/ui/button";
// 路由链接组件。
import Link from "next/link";
// 分页图标。
import {
  ChevronLeftIcon,
  ChevronRightIcon,
  DoubleArrowLeftIcon,
  DoubleArrowRightIcon,
} from "@radix-ui/react-icons";

// 分页组件入参定义。
interface PagePaginationProps {
  // 当前页码。
  currentPage: number;
  // 总页数。
  totalPages: number;
  // 每页条数。
  pageSize: number;
  // 数据总条数。
  totalItems: number;
  // 基础路径（默认 /dashboard）。
  basePath?: string;
}

// 通用分页组件。
export function PagePagination({
  currentPage,
  totalPages,
  pageSize,
  totalItems,
  basePath = "/dashboard",
}: PagePaginationProps) {
  // 是否存在下一页。
  const hasNextPage = currentPage < totalPages;
  // 是否存在上一页。
  const hasPreviousPage = currentPage > 1;

  // 根据页码拼接目标 URL。
  const buildUrl = (page: number) =>
    `${basePath}?page=${page}&size=${pageSize}`;

  return (
    <div className="flex items-center justify-between my-4">
      {/* 左侧：当前展示范围说明。 */}
      <div className="text-sm text-gray-600">
        {totalItems === 0 ? (
          <>Showing 0 of 0 results</>
        ) : (
          <>
            Showing {(currentPage - 1) * pageSize + 1} to{" "}
            {Math.min(currentPage * pageSize, totalItems)} of {totalItems}{" "}
            results
          </>
        )}
      </div>

      {/* 右侧：分页按钮组。 */}
      <div className="flex items-center space-x-2">
        {/* 跳转第一页。 */}
        <Link
          href={buildUrl(1)}
          className={!hasPreviousPage ? "pointer-events-none opacity-50" : ""}
        >
          <Button variant="outline" size="sm" disabled={!hasPreviousPage}>
            <DoubleArrowLeftIcon className="h-4 w-4" />
          </Button>
        </Link>

        {/* 跳转上一页。 */}
        <Link
          href={buildUrl(currentPage - 1)}
          className={!hasPreviousPage ? "pointer-events-none opacity-50" : ""}
        >
          <Button variant="outline" size="sm" disabled={!hasPreviousPage}>
            <ChevronLeftIcon className="h-4 w-4" />
          </Button>
        </Link>

        {/* 当前页信息。 */}
        {totalPages > 0 && (
          <span className="text-sm font-medium">
            Page {currentPage} of {totalPages}
          </span>
        )}

        {/* 跳转下一页。 */}
        <Link
          href={buildUrl(currentPage + 1)}
          className={hasNextPage ? "" : "pointer-events-none opacity-50"}
        >
          <Button variant="outline" size="sm" disabled={!hasNextPage}>
            <ChevronRightIcon className="h-4 w-4" />
          </Button>
        </Link>

        {/* 跳转最后一页。 */}
        <Link
          href={buildUrl(totalPages)}
          className={hasNextPage ? "" : "pointer-events-none opacity-50"}
        >
          <Button variant="outline" size="sm" disabled={!hasNextPage}>
            <DoubleArrowRightIcon className="h-4 w-4" />
          </Button>
        </Link>
      </div>
    </div>
  );
}
