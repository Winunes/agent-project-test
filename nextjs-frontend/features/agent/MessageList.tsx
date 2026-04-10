"use client";

import { useEffect, useRef } from "react";
import { ChatMessage } from "./types";

interface MessageListProps {
  messages: ChatMessage[];
}

export default function MessageList({ messages }: MessageListProps) {
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages]);

  return (
    <div className="min-h-0 flex-1 overflow-y-auto px-4 py-3">
      {messages.length === 0 ? (
        <p className="text-sm text-gray-500">先问我一个问题吧。</p>
      ) : null}

      <div className="space-y-3">
        {messages.map((msg) => {
          const isUser = msg.role === "user";

          return (
            <div key={msg.id} className="flex w-full min-w-0">
              <div
                className={`min-w-0 w-fit max-w-[85%] whitespace-pre-wrap break-words [overflow-wrap:anywhere] rounded-2xl px-3 py-2 text-sm leading-6 shadow-sm ${
                    isUser
                      ? "ml-auto bg-gray-300 text-gray-900 rounded-br-md border border-gray-400"
                      : "mr-auto bg-gray-100 text-gray-900 rounded-bl-md border border-gray-300"
                }`}
              >
                {msg.content || (isUser ? "" : "思考中...")}
              </div>
            </div>
          );
        })}
        <div ref={bottomRef} />
      </div>
    </div>
  );
}
