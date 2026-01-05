import { useEffect, useRef, useState } from "react";

type Source = {
  source_type: string;
  source_id: string;
  chunk_id: string;
  score: number;
};

type StageEvent = {
  event_id: number;
  stage: string;
  ts_ms: number;
  duration_ms: number;
  input: Record<string, any>;
  output: Record<string, any>;
  skipped: boolean;
  error: boolean;
};

type FinalPayload = {
  mode: "chat";
  conversation_id?: string | null;
  answer: string;
  confidence: number;
  sources: Source[];
  classification?: string | null;
  refusal_code?: string | null;
  needs_human?: boolean;
};

type ChatMessage = {
  id: string;
  role: "user" | "assistant";
  content: string;
  ts: number;

  // show only the latest pipeline stage (like "your" UI)
  status?: StageEvent | null;

  meta?: {
    sources?: Source[];
    confidence?: number;
    classification?: string | null;
    refusal_code?: string | null;
    needs_human?: boolean;
    conversation_id?: string | null;
  };
};

function uid() {
  return Math.random().toString(36).slice(2) + "-" + Date.now().toString(36);
}

function safeJsonParse(line: string) {
  try {
    return JSON.parse(line);
  } catch {
    return null;
  }
}

function formatStageLabel(stage: string) {
  const map: Record<string, string> = {
    persist_user_message: "Saving message",
    rewrite: "Rewriting query",
    retrieve: "Retrieving context",
    rerank: "Reranking",
    build_context: "Building context",
    llm_answer: "Generating answer",
    validate_citations: "Validating citations",
    persist_assistant_message: "Saving answer",
    update_summary: "Updating summary",
    classify_response: "Classifying response",
    fallback_no_docs: "No relevant docs",
    final: "Finalizing",
  };
  return map[stage] ?? stage;
}

type DrawerAiProps = {
  baseUrl?: string;
  apiKey?: string;
};

export const DrawerAi = ({
  baseUrl = "http://localhost:8001",
  apiKey = "super-secret-internal-key",
}: DrawerAiProps) => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);

  const abortRef = useRef<AbortController | null>(null);
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight, behavior: "smooth" });
  }, [messages.length]);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        if (loading) {
          abortRef.current?.abort();
          setLoading(false);
        } else {
          setOpen(false);
        }
      }
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [loading]);

  const stop = () => {
    abortRef.current?.abort();
    abortRef.current = null;
    setLoading(false);
  };

  const clear = () => {
    stop();
    setMessages([]);
    setConversationId(null);
    setInput("");
  };

  const setAssistantStatus = (assistantId: string, ev: StageEvent) => {
    setMessages((prev) =>
      prev.map((m) => (m.id === assistantId ? { ...m, status: ev } : m))
    );
  };

  const setFinalOnAssistant = (assistantId: string, fp: FinalPayload) => {
    setMessages((prev) =>
      prev.map((m) => {
        if (m.id !== assistantId) return m;
        return {
          ...m,
          content: fp.answer || "(empty)",
          meta: {
            sources: fp.sources,
            confidence: fp.confidence,
            classification: fp.classification ?? null,
            refusal_code: fp.refusal_code ?? null,
            needs_human: fp.needs_human,
            conversation_id: fp.conversation_id ?? null,
          },
          status: { ...(m.status ?? ({} as any)), stage: "final", event_id: (m.status?.event_id ?? 0) + 1 } as any,
        };
      })
    );
  };

  const setErrorOnAssistant = (assistantId: string, msg: string) => {
    setMessages((prev) =>
      prev.map((m) => (m.id === assistantId ? { ...m, content: `Error: ${msg}` } : m))
    );
  };

  const send = async () => {
    const text = input.trim();
    if (!text || loading) return;

    setInput("");
    setLoading(true);

    const userMsg: ChatMessage = { id: uid(), role: "user", content: text, ts: Date.now() };
    const assistantId = uid();
    const assistantMsg: ChatMessage = {
      id: assistantId,
      role: "assistant",
      content: "",
      ts: Date.now(),
      status: null,
    };

    setMessages((m) => [...m, userMsg, assistantMsg]);

    const controller = new AbortController();
    abortRef.current = controller;

    const url = `${baseUrl.replace(/\/$/, "")}/rag/chat`;
    const companyId = sessionStorage.getItem("company_id");
    if (!companyId) {
      setErrorOnAssistant(assistantId, "Missing company_id in session. Please re-login.");
      setLoading(false);
      return;
    }

    const body = {
      conversation_id: conversationId || undefined,
      message: text,
      company_id: Number(companyId),
    };

    try {
      const res = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "X-RAG-API-KEY": apiKey,
          Accept: "*/*",
        },
        body: JSON.stringify(body),
        signal: controller.signal,
      });

      if (!res.ok) {
        const errText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errText}`);
      }

      const reader = res.body?.getReader();
      if (!reader) throw new Error("No response body (stream not supported).");

      const decoder = new TextDecoder("utf-8");
      let buffer = "";

      let currentEvent = "message";
      let dataLines: string[] = [];

      const flushEvent = () => {
        if (!dataLines.length) return;
        const dataStr = dataLines.join("\n").trim();
        dataLines = [];

        const payload = safeJsonParse(dataStr);
        if (!payload) return;

        if (currentEvent === "stage") {
          setAssistantStatus(assistantId, payload as StageEvent);
          return;
        }

        if (currentEvent === "final") {
          const fp = (payload as any).payload as FinalPayload;
          setConversationId(fp.conversation_id ?? null);
          setFinalOnAssistant(assistantId, fp);
          return;
        }

        if (currentEvent === "error") {
          const message = (payload as any)?.message || "Unknown error";
          setErrorOnAssistant(assistantId, message);
        }
      };

      while (true) {
        const { value, done } = await reader.read();
        if (done) break;

        buffer += decoder.decode(value, { stream: true });

        let idx;
        while ((idx = buffer.indexOf("\n")) !== -1) {
          const line = buffer.slice(0, idx);
          buffer = buffer.slice(idx + 1);

          const trimmed = line.replace(/\r$/, "");

          if (trimmed.startsWith(":")) continue;

          if (trimmed.startsWith("event:")) {
            currentEvent = trimmed.slice("event:".length).trim();
            continue;
          }

          if (trimmed.startsWith("data:")) {
            dataLines.push(trimmed.slice("data:".length).trim());
            continue;
          }

          if (trimmed === "") {
            flushEvent();
            currentEvent = "message";
          }
        }
      }

      flushEvent();
    } catch (e: any) {
      const msg = e?.name === "AbortError" ? "Request aborted." : (e?.message ?? "Request failed.");
      setErrorOnAssistant(assistantId, msg);
    } finally {
      setLoading(false);
      abortRef.current = null;
    }
  };

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="fixed bottom-5 right-5 z-40 inline-flex items-center gap-2 rounded-full bg-zinc-900 px-4 py-3 text-sm font-semibold text-white shadow-lg shadow-black/20 hover:bg-zinc-800 focus:outline-none focus:ring-2 focus:ring-zinc-400"
      >
        <span className="inline-block h-2 w-2 rounded-full bg-emerald-400" />
        Ask AI
      </button>

      {open && (
        <div className="fixed inset-0 z-50">
          <button
            aria-label="Close"
            onClick={() => (loading ? stop() : setOpen(false))}
            className="absolute inset-0 bg-black/40"
          />

          <div className="absolute bottom-0 right-0 m-4 w-[min(420px,calc(100%-2rem))] overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-2xl">
            <div className="flex items-center justify-between border-b border-zinc-200 px-4 py-3">
              <div className="flex flex-col">
                <div className="text-sm font-semibold text-zinc-900">Ask AI</div>
                <div className="text-xs text-zinc-500">
                  {conversationId ? `Conversation: ${conversationId.slice(0, 8)}…` : "New conversation"}
                </div>
              </div>

              <div className="flex items-center gap-2">
                <button
                  type="button"
                  onClick={clear}
                  className="rounded-lg border border-zinc-200 bg-white px-2 py-1 text-xs font-medium text-zinc-700 hover:bg-zinc-50"
                >
                  Clear
                </button>

                <button
                  type="button"
                  onClick={() => (loading ? stop() : setOpen(false))}
                  className="rounded-lg bg-zinc-900 px-2 py-1 text-xs font-semibold text-white hover:bg-zinc-800"
                >
                  {loading ? "Stop" : "Close"}
                </button>
              </div>
            </div>

            <div className="flex h-[520px] flex-col">
              <div ref={scrollRef} className="flex-1 space-y-3 overflow-auto px-4 py-3">
                {messages.length === 0 ? (
                  <div className="rounded-xl border border-dashed border-zinc-200 bg-white p-4 text-sm text-zinc-600">
                    Type a question and press Enter.
                  </div>
                ) : (
                  messages.map((m) => (
                    <div key={m.id} className={`flex ${m.role === "user" ? "justify-end" : "justify-start"}`}>
                      <div
                        className={`max-w-[85%] rounded-2xl px-3 py-2 text-sm shadow-sm ${
                          m.role === "user" ? "bg-zinc-900 text-white" : "bg-zinc-100 text-zinc-900"
                        }`}
                      >
                        {/* Latest stage only (like your UI) */}
                        {m.role === "assistant" && m.status && (
                          <div className="mb-2 inline-flex w-full items-center justify-between gap-2 rounded-xl border border-zinc-200 bg-white/70 px-2 py-1">
                            <div className="min-w-0 truncate text-[11px] font-semibold text-zinc-800">
                               {formatStageLabel(m.status.stage)}
                              {m.status.skipped ? (
                                <span className="ml-2 rounded bg-zinc-100 px-1 py-0.5 text-[10px] font-medium text-zinc-600">
                                  skipped
                                </span>
                              ) : null}
                              {m.status.error ? (
                                <span className="ml-2 rounded bg-red-100 px-1 py-0.5 text-[10px] font-medium text-red-700">
                                  error
                                </span>
                              ) : null}
                            </div>
                            <div className="shrink-0 text-[11px] text-zinc-500">{m.status.duration_ms}ms</div>
                          </div>
                        )}

                        <div className="whitespace-pre-wrap">
                          {m.content || (m.role === "assistant" && loading ? "…" : "")}
                        </div>

                        {m.role === "assistant" && m.meta?.sources?.length ? (
                          <div className="mt-2 rounded-xl bg-white/70 px-2 py-1 text-[11px] text-zinc-700">
                            <div className="flex flex-wrap items-center gap-2">
                              <span className="font-semibold">Sources:</span>
                              <span className="text-zinc-600">
                                {m.meta.sources.slice(0, 3).map((s, i) => (
                                  <span key={`${s.source_type}-${s.source_id}-${s.chunk_id}`}>
                                    [{s.source_type}:{s.source_id}#{s.chunk_id}]
                                    {i < Math.min(2, m.meta.sources.length - 1) ? " " : ""}
                                  </span>
                                ))}
                                {m.meta.sources.length > 3 ? " …" : ""}
                              </span>
                            </div>
                            <div className="mt-1 flex flex-wrap items-center gap-2 text-zinc-600">
                              {typeof m.meta.confidence === "number" ? (
                                <span>Confidence: {m.meta.confidence.toFixed(2)}</span>
                              ) : null}
                              {m.meta.classification ? <span>· {m.meta.classification}</span> : null}
                              {m.meta.refusal_code ? <span>· {m.meta.refusal_code}</span> : null}
                              {m.meta.needs_human ? <span>· needs_human</span> : null}
                            </div>
                          </div>
                        ) : null}
                      </div>
                    </div>
                  ))
                )}
              </div>

              <div className="border-t border-zinc-200 bg-white p-3">
                <form
                  onSubmit={(e) => {
                    e.preventDefault();
                    send();
                  }}
                  className="flex items-end gap-2"
                >
                  <div className="flex-1">
                    <textarea
                      value={input}
                      onChange={(e) => setInput(e.target.value)}
                      placeholder="Ask something…"
                      rows={2}
                      className="w-full resize-none rounded-xl border border-zinc-200 bg-white px-3 py-2 text-sm text-zinc-900 outline-none focus:border-zinc-400"
                      onKeyDown={(e) => {
                        if (e.key === "Enter" && !e.shiftKey) {
                          e.preventDefault();
                          send();
                        }
                      }}
                    />
                    <div className="mt-1 text-[11px] text-zinc-500">Enter to send · Shift+Enter for new line</div>
                  </div>

                  <button
                    type="submit"
                    disabled={loading || input.trim().length === 0}
                    className="inline-flex h-10 items-center justify-center rounded-xl bg-zinc-900 px-4 text-sm font-semibold text-white shadow-sm hover:bg-zinc-800 disabled:cursor-not-allowed disabled:opacity-50"
                  >
                    {loading ? "Sending…" : "Send"}
                  </button>
                </form>
              </div>
            </div>

          </div>
        </div>
      )}
    </>
  );
};
