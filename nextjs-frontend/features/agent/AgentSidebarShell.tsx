"use client";

import { useEffect, useRef, useState } from "react";
import { PanelRightClose, PanelRightOpen } from "lucide-react";
import MessageList from "./MessageList";
import ChatInput from "./ChatInput";
import { ChatMessage } from "./types";
import { collectPageContext } from "./pageContext";

const MIN_WIDTH = 320;
const MAX_WIDTH = 760;
const COLLAPSED_WIDTH = 56;

export default function AgentSidebarShell() {
  const [open, setOpen] = useState(true);
  const [width, setWidth] = useState(420);
  const [dragging, setDragging] = useState(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  // 固定初始值，保证服务端和客户端首帧一致，避免 hydration mismatch
  const [displaySessionId, setDisplaySessionId] = useState("");



  const dragRef = useRef<{ startX: number; startWidth: number } | null>(null);
  const sessionIdRef = useRef<string>("");
  const userIdRef = useRef<string>("");

  useEffect(() => {
    const storedSessionId = sessionStorage.getItem("agent_session_id");
    const sessionId = storedSessionId ?? crypto.randomUUID();
    if (!storedSessionId) {
      sessionStorage.setItem("agent_session_id", sessionId);
    }
    sessionIdRef.current = sessionId;
    setDisplaySessionId(sessionId);

    const storedUserId = localStorage.getItem("agent_user_id");
    const userId = storedUserId ?? `u_${crypto.randomUUID().slice(0, 8)}`;
    if (!storedUserId) {
      localStorage.setItem("agent_user_id", userId);
    }
    userIdRef.current = userId;
  }, []);

  function clampWidth(next: number) {
    const screenMax = Math.floor(window.innerWidth * 0.65);
    const max = Math.min(MAX_WIDTH, screenMax);
    return Math.max(MIN_WIDTH, Math.min(next, max));
  }

  function handleResizePointerDown(e: React.PointerEvent<HTMLDivElement>) {
    if (!open) return;
    e.preventDefault();
    e.currentTarget.setPointerCapture(e.pointerId);

    dragRef.current = {
      startX: e.clientX,
      startWidth: width,
    };
    setDragging(true);
  }

  useEffect(() => {
    if (!dragging) return;

    function onPointerMove(e: PointerEvent) {
      if (!dragRef.current) return;
      const delta = dragRef.current.startX - e.clientX;
      const next = dragRef.current.startWidth + delta;
      setWidth(clampWidth(next));
    }

    function onPointerUp() {
      setDragging(false);
      dragRef.current = null;
    }

    window.addEventListener("pointermove", onPointerMove);
    window.addEventListener("pointerup", onPointerUp);

    document.body.style.userSelect = "none";
    document.body.style.cursor = "col-resize";

    return () => {
      window.removeEventListener("pointermove", onPointerMove);
      window.removeEventListener("pointerup", onPointerUp);
      document.body.style.userSelect = "";
      document.body.style.cursor = "";
    };
  }, [dragging]);

  async function handleSend(text: string) {
    const userMsg: ChatMessage = {
      id: crypto.randomUUID(),
      role: "user",
      content: text,
    };
    const assistantId = crypto.randomUUID();

    setMessages((prev) => [
      ...prev,
      userMsg,
      { id: assistantId, role: "assistant", content: "" },
    ]);

    setLoading(true);

    try {
      const resp = await fetch("http://127.0.0.1:8000/api/v1/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_id: userIdRef.current || "u_fallback",
          session_id: sessionIdRef.current || "s_fallback",
          message: text,
          page_context: collectPageContext(),
        }),
      });

      if (!resp.ok || !resp.body) {
        throw new Error("SSE request failed");
      }

      const reader = resp.body.getReader();
      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });
        const events = buffer.split("\n\n");
        buffer = events.pop() ?? "";

        for (const eventText of events) {
          const lines = eventText.split("\n");
          const dataLine = lines.find((line) => line.startsWith("data:"));
          if (!dataLine) continue;

          const raw = dataLine.replace(/^data:\s*/, "");

          try {
            const data = JSON.parse(raw);
            if (data.delta) {
              setMessages((prev) =>
                prev.map((m) =>
                  m.id === assistantId
                    ? { ...m, content: m.content + data.delta }
                    : m
                )
              );
            }
          } catch {
            // ignore non-json data
          }
        }
      }
    } catch {
      setMessages((prev) =>
        prev.map((m) =>
          m.id === assistantId
            ? { ...m, content: "请求失败，请检查后端 /api/v1/chat/stream 是否正常。" }
            : m
        )
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <aside
      className="relative h-screen shrink-0 overflow-visible border-l border-gray-300 bg-white"
      style={{ width: open ? `${width}px` : `${COLLAPSED_WIDTH}px` }}
    >
      {open ? (
        <div
          role="separator"
          aria-orientation="vertical"
          onPointerDown={handleResizePointerDown}
          title="拖拽调整宽度"
          style={{
            position: "absolute",
            top: 0,
            bottom: 0,
            left: -8,
            width: 16,
            zIndex: 2147483647,
            cursor: "col-resize",
            touchAction: "none",
          }}
        >
          <div
            style={{
              position: "absolute",
              left: 6,
              top: 0,
              width: 4,
              height: "100%",
              background: "#57575736",
            }}
          />
          <div
            style={{
              position: "absolute",
              left: 4,
              top: "50%",
              width: 8,
              height: 56,
              transform: "translateY(-50%)",
              borderRadius: 9999,
              background: "#00c3ff",
            }}
          />
        </div>
      ) : null}

      <div className="flex h-full min-h-0 flex-col overflow-hidden">
        <div
          className={`border-b py-3 ${
            open
              ? "flex items-center justify-between px-3"
              : "flex items-center justify-center px-1"
          }`}
        >
          {open ? (
            <div className="min-w-0">
              <h2 className="text-sm font-semibold">Agent Assistant</h2>
                <p
                  suppressHydrationWarning
                  className="mt-0.5 truncate font-mono text-[11px] text-gray-500"
                >
                  session ID: {displaySessionId || "loading..."}
                </p>
            </div>
          ) : null}

          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            className="rounded p-1 text-gray-600 hover:bg-gray-100"
            aria-label={open ? "Collapse sidebar" : "Expand sidebar"}
          >
            {open ? <PanelRightClose className="h-4 w-4" /> : <PanelRightOpen className="h-4 w-4" />}
          </button>
        </div>

        {open ? (
          <>
            <MessageList messages={messages} />
            <ChatInput onSend={handleSend} disabled={loading} />
          </>
        ) : (
          <div className="flex flex-1 items-center justify-center text-[11px] text-gray-500 [writing-mode:vertical-rl]">
            AGENT
          </div>
        )}
      </div>
    </aside>
  );
}
