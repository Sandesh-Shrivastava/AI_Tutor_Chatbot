"use client";

import { useStore } from "@/store/useStore";
import { ChevronRight, LogOut, PlusSquare, Terminal } from "lucide-react";
import { cn } from "@/lib/utils";

const SUBJECTS = [
  "Physics", 
  "Chemistry", 
  "Biology", 
  "Mathematics", 
  "Computer_Science", 
  "Social_Science",
  "General_Knowledge"
];

export function Sidebar() {
  const { user, subject, mode, setSubject, setMode, setUser, clearSession } = useStore();

  const handleLogout = () => {
    setUser(null);
    clearSession();
    window.location.href = "/login";
  };

  return (
    <aside className="w-72 h-full flex flex-col bg-[#080808] border-r border-[#1a1a1a]">
      <div className="p-8">
        <div className="flex items-center gap-4 mb-12 border-b border-[#1a1a1a] pb-8">
          <div className="w-12 h-12 bg-[#ff4d00] flex items-center justify-center">
            <Terminal className="text-black w-6 h-6" strokeWidth={3} />
          </div>
          <div>
            <h2 className="font-black text-xl tracking-tighter text-white uppercase">{user?.username}</h2>
            <p className="tech-label text-[#ff4d00]">{user?.level}</p>
          </div>
        </div>

        <div className="space-y-10">
          <div>
            <label className="tech-label mb-4 block">Core_Modules</label>
            <div className="space-y-1">
              {SUBJECTS.map((s) => (
                <button
                  key={s}
                  onClick={() => setSubject(s)}
                  className={cn(
                    "w-full text-left px-4 py-3 text-[11px] font-black uppercase tracking-widest transition-all border-l-2",
                    subject === s 
                      ? "border-[#ff4d00] bg-[#ff4d00]/5 text-[#ff4d00]" 
                      : "border-transparent text-[#444444] hover:text-white hover:bg-white/5"
                  )}
                >
                  <span className="mr-2">{subject === s ? ">" : " "}</span>
                  {s.replace("_", " ")}
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="tech-label mb-4 block">Logic_Mode</label>
            <div className="flex gap-px bg-[#1a1a1a] p-px">
              <button
                onClick={() => setMode("normal")}
                className={cn(
                  "flex-1 py-3 text-[10px] font-black uppercase tracking-widest transition-all",
                  mode === "normal" ? "bg-[#ff4d00] text-black" : "bg-[#080808] text-[#444444]"
                )}
              >
                Normal
              </button>
              <button
                onClick={() => setMode("socratic")}
                className={cn(
                  "flex-1 py-3 text-[10px] font-black uppercase tracking-widest transition-all",
                  mode === "socratic" ? "bg-[#ff4d00] text-black" : "bg-[#080808] text-[#444444]"
                )}
              >
                Socratic
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-auto p-8 border-t border-[#1a1a1a] space-y-4">
        <button 
          onClick={clearSession}
          className="w-full flex items-center justify-between px-4 py-4 bg-white text-black text-[10px] font-black uppercase tracking-widest hover:bg-[#ff4d00] transition-all"
        >
          New_Session <PlusSquare size={16} />
        </button>
        <button 
          onClick={handleLogout}
          className="w-full flex items-center justify-between px-4 py-2 text-[#444444] text-[10px] font-black uppercase tracking-widest hover:text-white transition-all"
        >
          Disconnect <LogOut size={16} />
        </button>
      </div>
    </aside>
  );
}
