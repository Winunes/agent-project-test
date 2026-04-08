// Next.js 路由跳转组件。
import Link from "next/link";
// 图标组件：主页、用户、列表。
import { Home, Users2, List } from "lucide-react";
// Next.js 图片组件（带优化能力）。
import Image from "next/image";

// 面包屑 UI 组件。
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
// 下拉菜单 UI 组件。
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
// 头像 UI 组件。
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
// 退出登录 Server Action。
import { logout } from "@/components/actions/logout-action";

// Dashboard 专属布局：侧边栏 + 顶部栏 + 内容区。
export default function DashboardLayout({
  children,
}: {
  // children 是 dashboard 下各子页面内容。
  children: React.ReactNode;
}) {
  return (
    // 总体横向布局容器。
    <div className="flex min-h-screen">
      {/* 左侧固定导航栏。 */}
      <aside className="fixed inset-y-0 left-0 z-10 w-16 flex flex-col border-r bg-background p-4">
        <div className="flex flex-col items-center gap-8">
          {/* Logo：点击回首页。 */}
          <Link
            href="/"
            className="flex items-center justify-center rounded-full"
          >
            <Image
              src="/images/vinta.png"
              alt="Vinta"
              width={64}
              height={64}
              className="object-cover transition-transform duration-200 hover:scale-105"
            />
          </Link>
          {/* 导航：仪表盘。 */}
          <Link
            href="/dashboard"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <List className="h-5 w-5" />
          </Link>
          {/* 导航：客户页（当前模板可能还未实现页面）。 */}
          <Link
            href="/customers"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <Users2 className="h-5 w-5" />
          </Link>
        </div>
      </aside>
      {/* 主内容区（左侧留出侧边栏宽度）。 */}
      <main className="ml-16 w-full p-8 bg-muted/40">
        {/* 顶部栏：左面包屑 + 右侧用户菜单。 */}
        <header className="flex justify-between items-center mb-6">
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href="/" className="flex items-center gap-2">
                    <Home className="h-4 w-4" />
                    <span>Home</span>
                  </Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator>/</BreadcrumbSeparator>
              <BreadcrumbItem>
                <BreadcrumbLink asChild>
                  <Link href="/dashboard" className="flex items-center gap-2">
                    <List className="h-4 w-4" />
                    <span>Dashboard</span>
                  </Link>
                </BreadcrumbLink>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
          <div className="relative">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                {/* 头像按钮，点击弹出下拉菜单。 */}
                <button className="flex items-center justify-center w-10 h-10 rounded-full bg-gray-300 hover:bg-gray-400">
                  <Avatar>
                    <AvatarFallback>U</AvatarFallback>
                  </Avatar>
                </button>
              </DropdownMenuTrigger>
              <DropdownMenuContent align="end" side="bottom">
                {/* 跳转支持页。 */}
                <DropdownMenuItem>
                  <Link
                    href="/support"
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Support
                  </Link>
                </DropdownMenuItem>
                {/* 执行退出登录动作。 */}
                <DropdownMenuItem>
                  <button
                    onClick={logout}
                    className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                  >
                    Logout
                  </button>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </header>
        {/* 子页面渲染区域。 */}
        <section className="grid gap-6">{children}</section>
      </main>
    </div>
  );
}
