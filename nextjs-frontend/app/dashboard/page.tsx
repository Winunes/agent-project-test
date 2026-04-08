// 表格组件集合。
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TableHeader,
} from "@/components/ui/table";
// 下拉菜单组件集合。
import {
  DropdownMenu,
  DropdownMenuTrigger,
  DropdownMenuContent,
  DropdownMenuItem,
} from "@/components/ui/dropdown-menu";
// 获取 Item 列表的 Server Action。
import { fetchItems } from "@/components/actions/items-action";
// 删除按钮组件（内部会调用删除 Action）。
import { DeleteButton } from "./deleteButton";
// OpenAPI 生成的分页响应类型。
import { ReadItemResponse } from "@/app/openapi-client";
// 按钮组件。
import { Button } from "@/components/ui/button";
// Next.js 路由跳转组件。
import Link from "next/link";
// 每页数量选择器组件。
import { PageSizeSelector } from "@/components/page-size-selector";
// 分页组件。
import { PagePagination } from "@/components/page-pagination";

// Dashboard 页面接收的查询参数类型定义。
interface DashboardPageProps {
  // searchParams 在 Next.js 新版本中是 Promise 形式。
  searchParams: Promise<{
    // 页码参数，可选。
    page?: string;
    // 每页数量参数，可选。
    size?: string;
  }>;
}

// Dashboard 主页面（服务端组件）。
export default async function DashboardPage({
  searchParams,
}: DashboardPageProps) {
  // 解析 URL 查询参数。
  const params = await searchParams;
  // 把 page 转成数字，默认第 1 页。
  const page = Number(params.page) || 1;
  // 把 size 转成数字，默认每页 10 条。
  const size = Number(params.size) || 10;

  // 获取分页数据，并断言为生成的响应类型。
  const items = (await fetchItems(page, size)) as ReadItemResponse;
  // 计算总页数（总数为空时按 0 处理）。
  const totalPages = Math.ceil((items.total || 0) / size);

  return (
    <div>
      {/* 页面标题。 */}
      <h2 className="text-2xl font-semibold mb-6">Welcome to your Dashboard</h2>
      {/* 页面说明。 */}
      <p className="text-lg mb-6">
        Here, you can see the overview of your items and manage them.
      </p>

      {/* 跳转到“新增 Item”页面。 */}
      <div className="mb-6">
        <Link href="/dashboard/add-item">
          <Button variant="outline" className="text-lg px-4 py-2">
            Add New Item
          </Button>
        </Link>
      </div>

      {/* 列表卡片容器。 */}
      <section className="p-6 bg-white rounded-lg shadow-lg mt-8">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold">Items</h2>
          {/* 切换每页条数。 */}
          <PageSizeSelector currentSize={size} />
        </div>

        {/* Item 数据表格。 */}
        <Table className="min-w-full text-sm">
          <TableHeader>
            <TableRow>
              <TableHead className="w-[120px]">Name</TableHead>
              <TableHead>Description</TableHead>
              <TableHead className="text-center">Quantity</TableHead>
              <TableHead className="text-center">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {/* 无数据时展示空状态。 */}
            {!items.items?.length ? (
              <TableRow>
                <TableCell colSpan={4} className="text-center">
                  No results.
                </TableCell>
              </TableRow>
            ) : (
              // 有数据时逐行渲染。
              items.items.map((item, index) => (
                <TableRow key={index}>
                  <TableCell>{item.name}</TableCell>
                  <TableCell>{item.description}</TableCell>
                  <TableCell className="text-center">{item.quantity}</TableCell>
                  <TableCell className="text-center">
                    <DropdownMenu>
                      <DropdownMenuTrigger className="cursor-pointer p-1 text-gray-600 hover:text-gray-800">
                        <span className="text-lg font-semibold">...</span>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent className="p-2">
                        {/* 编辑功能目前占位禁用。 */}
                        <DropdownMenuItem disabled={true}>
                          Edit
                        </DropdownMenuItem>
                        {/* 删除功能。 */}
                        <DeleteButton itemId={item.id} />
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>

        {/* 分页控件。 */}
        <PagePagination
          currentPage={page}
          totalPages={totalPages}
          pageSize={size}
          totalItems={items.total || 0}
          basePath="/dashboard"
        />
      </section>
    </div>
  );
}
