import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useStore } from "@/store/useStore";
import { cn } from "@/lib/utils";
import { Terminal } from "lucide-react";

const LEVELS = ["beginner", "intermediate", "advanced"];

export default function LoginPage() {
  const [username, setUsername] = useState("");
  const [level, setLevel] = useState("beginner");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const { setUser } = useStore();

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!username.trim()) return;

    setIsLoading(true);
    try {
      const baseUrl = import.meta.env.VITE_API_URL || "http://localhost:8000";
      const res = await fetch(`${baseUrl}/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, level }),
      });
      
      if (res.ok) {
        const user = await res.json();
        setUser(user);
        navigate("/");
      }
    } catch (error) {
      console.error("Login failed", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-4 bg-[#050505] font-sans">
      <div className="scanline"></div>
      
      <motion.div 
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="w-full max-w-lg p-12 bg-[#080808] border border-[#1a1a1a] relative"
      >
        {/* Decorative elements */}
        <div className="absolute -top-1 -left-1 w-4 h-4 border-t-2 border-l-2 border-[#ff4d00]"></div>
        <div className="absolute -top-1 -right-1 w-4 h-4 border-t-2 border-r-2 border-[#ff4d00]"></div>
        <div className="absolute -bottom-1 -left-1 w-4 h-4 border-b-2 border-l-2 border-[#ff4d00]"></div>
        <div className="absolute -bottom-1 -right-1 w-4 h-4 border-b-2 border-r-2 border-[#ff4d00]"></div>

        <div className="mb-16">
          <div className="flex items-center gap-4 mb-4">
            <Terminal className="text-[#ff4d00] w-8 h-8" />
            <h1 className="text-4xl font-black text-white uppercase tracking-tighter">
              AI_TUTOR
            </h1>
          </div>
          <p className="tech-label">Universal_Learning_Interface</p>
        </div>

        <form onSubmit={handleLogin} className="space-y-12">
          <div className="space-y-3">
            <label className="tech-label">Access_Identifier</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="ENTER_USERNAME..."
              className="w-full px-6 py-5 bg-[#111111] border border-[#222222] focus:border-[#ff4d00] outline-none text-[12px] font-black uppercase tracking-[0.2em] text-white transition-all"
            />
          </div>

          <div className="space-y-4">
            <label className="tech-label">Knowledge_Level</label>
            <div className="grid grid-cols-3 gap-px bg-[#1a1a1a]">
              {LEVELS.map((l) => (
                <button
                  key={l}
                  type="button"
                  onClick={() => setLevel(l)}
                  className={cn(
                    "py-4 text-[10px] font-black uppercase tracking-widest transition-all",
                    level === l 
                      ? "bg-[#ff4d00] text-black" 
                      : "bg-[#080808] text-[#444444] hover:text-white"
                  )}
                >
                  {l}
                </button>
              ))}
            </div>
          </div>

          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-6 bg-white text-black font-black text-xs uppercase tracking-[0.3em] hover:bg-[#ff4d00] transition-all disabled:opacity-20 flex items-center justify-center gap-4 group"
          >
            {isLoading ? "SYNCHRONIZING..." : "ESTABLISH_CONNECTION"}
            <span className="group-hover:translate-x-2 transition-transform">→</span>
          </button>
        </form>
      </motion.div>

      <div className="mt-16 tech-label opacity-30 text-[8px]">
        [ SECURITY_CLEARANCE_REQUIRED // ENCRYPTION_ACTIVE ]
      </div>
    </main>
  );
}
