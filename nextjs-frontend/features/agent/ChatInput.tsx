"use client";

import { FormEvent, KeyboardEvent, useRef, useState } from "react";

interface ChatInputProps {
  onSend: (text: string) => void | Promise<void>;
  disabled?: boolean;
}

export default function ChatInput({ onSend, disabled = false }: ChatInputProps) {
  const [text, setText] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  function autoResize() {
    const el = textareaRef.current;
    if (!el) return;
    el.style.height = "auto";
    el.style.height = `${Math.min(el.scrollHeight, 160)}px`;
  }

  async function submit() {
    const value = text.trim();
    if (!value || disabled) return;
    setText("");
    await onSend(value);
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  }

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    await submit();
  }

  async function handleKeyDown(e: KeyboardEvent<HTMLTextAreaElement>) {
    // Enter 发送，Shift+Enter 换行
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      await submit();
    }
  }

  return (
    <form onSubmit={handleSubmit} className="border-t p-3">
      <div className="flex items-end gap-2">
        <textarea
          ref={textareaRef}
          value={text}
          onChange={(e) => {
            setText(e.target.value);
            autoResize();
          }}
          onKeyDown={handleKeyDown}
          rows={1}
          placeholder={disabled ? "正在生成回复..." : "输入你的问题..."}
          disabled={disabled}
          className="max-h-40 min-h-[40px] flex-1 resize-none overflow-y-auto rounded-md border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-blue-500 disabled:cursor-not-allowed disabled:bg-gray-100"
        />
        <button
          type="submit"
          disabled={disabled}
          className="rounded-md bg-blue-600 px-3 py-2 text-sm text-white hover:bg-blue-700 disabled:cursor-not-allowed disabled:opacity-60"
        >
          发送
        </button>
      </div>
    </form>
  );
}
