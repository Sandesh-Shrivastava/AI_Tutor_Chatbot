import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Cpu, User, Activity } from "lucide-react";
import ReactMarkdown from "react-markdown";
import { useStore } from "@/store/useStore";
import { cn } from "@/lib/utils";

export function Chat() {
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const { user, sessionId, subject, mode, messages, setSessionId, addMessage } = useStore();
  const scrollRef = useRef(null);

  // Auto-scroll
  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages, isTyping]);

  // Init session if needed
  useEffect(() => {
    if (!sessionId && user) {
      const initSession = async () => {
        try {
          const baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
          const res = await fetch(`${baseUrl}/sessions/start`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
              user_id: user.id,
              subject,
              level: user.level,
              mode
            })
          });
          const data = await res.json();
          setSessionId(data.session_id);
        } catch (e) {
          console.error("Failed to start session", e);
        }
      };
      initSession();
    }
  }, [sessionId, user, subject, mode, setSessionId]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!input.trim() || !sessionId || !user) return;

    const question = input.trim();
    setInput("");
    addMessage({ role: "user", content: question });
    setIsTyping(true);

    try {
      const baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await fetch(`${baseUrl}/chat/ask`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          session_id: sessionId,
          user_id: user.id,
          question,
          subject,
          level: user.level,
          mode
        })
      });

      if (res.ok) {
        const data = await res.json();
        addMessage({ 
          role: "assistant", 
          content: data.answer, 
          sources: data.sources 
        });
      }
    } catch (e) {
      console.error("Chat error", e);
      addMessage({ 
        role: "assistant", 
        content: "CRITICAL_ERROR: UPLINK_FAILURE" 
      });
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col h-full overflow-hidden bg-[#050505]">
      {/* Header */}
      <header className="p-8 border-b border-[#1a1a1a] flex items-center justify-between">
        <div className="flex items-center gap-6">
          <Activity className="text-[#ff4d00] w-5 h-5" />
          <div>
            <h1 className="text-sm font-black text-white uppercase tracking-[0.2em]">
              AI_Tutor_Terminal [Live]
            </h1>
            <p className="text-[9px] text-[#444444] font-black uppercase tracking-[0.4em] mt-1">
              Active_Link: {subject} // {mode}_Mode
            </p>
          </div>
        </div>
      </header>

      {/* Messages */}
      <div 
        ref={scrollRef}
        className="flex-1 overflow-y-auto p-12 space-y-12 scroll-smooth"
      >
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              className={cn(
                "flex gap-8 max-w-5xl",
                msg.role === "user" ? "flex-row-reverse ml-auto" : ""
              )}
            >
              <div className={cn(
                "w-12 h-12 flex items-center justify-center shrink-0 border-2",
                msg.role === "user" 
                  ? "border-white text-white" 
                  : "border-[#ff4d00] text-[#ff4d00] bg-[#ff4d00]/5 shadow-[0_0_15px_rgba(255,77,0,0.2)]"
              )}>
                {msg.role === "user" ? <User size={22} /> : <Cpu size={22} />}
              </div>
              
              <div className="space-y-4">
                <div className={cn(
                  "p-6 text-[13px] font-medium leading-relaxed tracking-wide",
                  msg.role === "user" 
                    ? "bg-[#111111] text-white border border-[#222222]" 
                    : "bg-white text-black font-bold"
                )}>
                  <div className="prose prose-sm max-w-none">
                    <ReactMarkdown>
                      {msg.content}
                    </ReactMarkdown>
                  </div>
                </div>
                
                {msg.sources && msg.sources.length > 0 && (
                  <div className="flex flex-wrap gap-3">
                    {msg.sources.map((src, j) => (
                      <span key={j} className="px-3 py-1 bg-[#111111] border border-[#222222] text-[9px] text-[#444444] font-black uppercase tracking-widest">
                        {src}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </motion.div>
          ))}
        </AnimatePresence>

        {isTyping && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-8">
            <div className="w-12 h-12 border-2 border-[#ff4d00] flex items-center justify-center shrink-0 bg-[#ff4d00]/5">
              <Cpu size={22} className="text-[#ff4d00]" />
            </div>
            <div className="p-6 bg-white text-black flex gap-2 items-center">
              <span className="w-1.5 h-1.5 bg-black animate-pulse" />
              <span className="w-1.5 h-1.5 bg-black animate-pulse [animation-delay:0.2s]" />
              <span className="w-1.5 h-1.5 bg-black animate-pulse [animation-delay:0.4s]" />
              <span className="ml-2 text-[9px] font-black uppercase tracking-widest">Processing...</span>
            </div>
          </motion.div>
        )}
      </div>

      {/* Input Area */}
      <div className="p-8 bg-[#080808] border-t border-[#1a1a1a]">
        <form onSubmit={handleSend} className="relative max-w-5xl mx-auto flex gap-4">
          <div className="relative flex-1">
            <div className="absolute left-4 top-1/2 -translate-y-1/2 text-[#ff4d00] font-black text-xs">{">"}</div>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder={`COMMAND_INPUT: ${subject}...`}
              className="w-full pl-10 pr-6 py-5 bg-[#111111] border border-[#222222] focus:border-[#ff4d00] outline-none text-[11px] font-black uppercase tracking-widest text-white transition-all"
            />
          </div>
          <button
            type="submit"
            disabled={!input.trim() || isTyping}
            className="w-20 bg-[#ff4d00] text-black flex items-center justify-center hover:bg-white transition-all disabled:opacity-20"
          >
            <Send size={20} strokeWidth={3} />
          </button>
        </form>
        <p className="text-[9px] text-center text-[#222222] mt-6 font-black uppercase tracking-[0.5em]">
          Industrial Grade Intelligence // Site_V1.0
        </p>
      </div>
    </div>
  );
}
