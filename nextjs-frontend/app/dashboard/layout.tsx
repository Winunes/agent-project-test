// Next.js 路由跳转组件。
import Link from "next/link";
// 图标组件：主页、用户、列表。
import { Home, Users2, List } from "lucide-react";
// Next.js 图片组件（带优化能力）。
import Image from "next/image";

import AgentSidebarShell from "@/features/agent/AgentSidebarShell";
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
    // 顶层布局：左侧导航 + 右侧工作区
    <div className="flex min-h-screen">
      {/* 左侧固定导航栏（保留模板原有结构） */}
      <aside className="fixed inset-y-0 left-0 z-10 w-16 flex flex-col border-r bg-background p-4">
        <div className="flex flex-col items-center gap-8">
          {/* Logo */}
          <Link href="/" className="flex items-center justify-center rounded-full">
            <Image
              src="/images/vinta.png"
              alt="Vinta"
              width={64}
              height={64}
              className="object-cover transition-transform duration-200 hover:scale-105"
            />
          </Link>

          {/* Dashboard */}
          <Link
            href="/dashboard"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <List className="h-5 w-5" />
          </Link>

          {/* Customers（占位） */}
          <Link
            href="/customers"
            className="flex items-center gap-2 text-muted-foreground hover:text-foreground"
          >
            <Users2 className="h-5 w-5" />
          </Link>
        </div>
      </aside>

      {/* 右侧工作区：主内容 + 右侧停靠式 Agent 侧栏 */}
      <div className="ml-16 flex min-h-screen w-[calc(100%-4rem)] bg-muted/40">
        {/* 主内容区 */}
        <main className="flex min-w-0 flex-1 flex-col p-8">
          <header className="mb-6 flex items-center justify-between">
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
                  <button className="flex h-10 w-10 items-center justify-center rounded-full bg-gray-300 hover:bg-gray-400">
                    <Avatar>
                      <AvatarFallback>U</AvatarFallback>
                    </Avatar>
                  </button>
                </DropdownMenuTrigger>
                <DropdownMenuContent align="end" side="bottom">
                  <DropdownMenuItem>
                    <Link
                      href="/support"
                      className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                    >
                      Support
                    </Link>
                  </DropdownMenuItem>
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

          <section className="grid min-h-0 gap-6">{children}</section>
        </main>

        {/* 右侧停靠式 Agent 侧栏（展开时主内容自动让出空间） */}
        <AgentSidebarShell />
      </div>
    </div>
  );
}
