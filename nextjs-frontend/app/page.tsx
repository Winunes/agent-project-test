// 导入项目封装的按钮组件。
import { Button } from "@/components/ui/button";
// Next.js 的无刷新跳转组件。
import Link from "next/link";
// GitHub 图标组件。
import { FaGithub } from "react-icons/fa";
// 徽章样式组件。
import { Badge } from "@/components/ui/badge";

// 首页组件。
export default function Home() {
  return (
    // 页面主容器：全屏高度、居中布局、浅色/深色背景。
    <main className="flex min-h-screen flex-col items-center justify-center bg-gray-50 dark:bg-gray-900 p-8">
      {/* 内容容器：居中且限制最大宽度。 */}
      <div className="text-center max-w-2xl">
        {/* 首页大标题。 */}
        <h1 className="text-5xl font-bold text-gray-800 dark:text-white mb-6">
          Welcome to the Next.js & FastAPI Boilerplate
        </h1>
        {/* 首页说明文案。 */}
        <p className="text-lg text-gray-600 dark:text-gray-300 mb-8">
          A simple and powerful template to get started with full-stack
          development using Next.js and FastAPI.
        </p>

        {/* 跳转到 Dashboard 的主按钮。 */}
        <Link href="/dashboard">
          <Button className="px-8 py-4 text-xl font-semibold rounded-full shadow-lg bg-gradient-to-r from-blue-500 to-indigo-500 text-white hover:from-blue-600 hover:to-indigo-600 focus:ring-4 focus:ring-blue-300">
            Go to Dashboard
          </Button>
        </Link>

        {/* GitHub 链接徽章区域。 */}
        <div className="mt-6">
          <Badge
            variant="outline"
            className="text-sm flex items-center gap-2 px-3 py-2 rounded-lg border-gray-300 dark:border-gray-700"
          >
            {/* GitHub 图标。 */}
            <FaGithub className="w-5 h-5 text-black dark:text-white" />
            {/* 外链到模板仓库。 */}
            <Link
              href="https://github.com/vintasoftware/nextjs-fastapi-template"
              target="_blank"
              className="hover:underline"
            >
              View on GitHub
            </Link>
          </Badge>
        </div>
      </div>
    </main>
  );
}
