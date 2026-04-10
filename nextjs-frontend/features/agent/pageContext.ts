export interface PageContext {
  page_url: string;
  page_title: string;
  module_name: string;
  selected_text: string;
  visible_text_summary: string;
}

function getSelectedText(): string {
  if (typeof window === "undefined") return "";
  return window.getSelection()?.toString().trim() ?? "";
}

function getVisibleTextSummary(maxChars: number = 3000): string {
  if (typeof document === "undefined") return "";

  const chunks: string[] = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);

  while (walker.nextNode()) {
    const node = walker.currentNode;
    const text = node.textContent?.replace(/\s+/g, " ").trim();
    if (!text) continue;

    const parent = node.parentElement;
    if (!parent) continue;

    // 跳过脚本/样式/隐藏区域
    const tag = parent.tagName.toLowerCase();
    if (["script", "style", "noscript"].includes(tag)) continue;
    const style = window.getComputedStyle(parent);
    if (style.display === "none" || style.visibility === "hidden") continue;

    chunks.push(text);

    const total = chunks.join(" ").length;
    if (total >= maxChars) break;
  }

  return chunks.join(" ").slice(0, maxChars);
}

function getModuleNameFromPath(pathname: string): string {
  const parts = pathname.split("/").filter(Boolean);
  return parts[0] ?? "home";
}

export function collectPageContext(): PageContext {
  if (typeof window === "undefined") {
    return {
      page_url: "",
      page_title: "",
      module_name: "",
      selected_text: "",
      visible_text_summary: "",
    };
  }

  return {
    page_url: window.location.href,
    page_title: document.title || "",
    module_name: getModuleNameFromPath(window.location.pathname),
    selected_text: getSelectedText(),
    visible_text_summary: getVisibleTextSummary(3000),
  };
}
