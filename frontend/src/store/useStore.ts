import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id: number;
  username: string;
  level: string;
}

interface AppState {
  user: User | null;
  sessionId: number | null;
  subject: string;
  mode: "normal" | "socratic";
  messages: any[];
  
  setUser: (user: User | null) => void;
  setSessionId: (id: number | null) => void;
  setSubject: (subject: string) => void;
  setMode: (mode: "normal" | "socratic") => void;
  setMessages: (messages: any[]) => void;
  addMessage: (message: any) => void;
  clearSession: () => void;
  setHydrated: (h: boolean) => void;
  _hydrated: boolean;
}

export const useStore = create<AppState>()(
  persist(
    (set) => ({
      user: null,
      sessionId: null,
      subject: "Physics",
      mode: "normal",
      messages: [],

      setUser: (user) => set({ user }),
      setSessionId: (sessionId) => set({ sessionId }),
      setSubject: (subject) => set({ subject }),
      setMode: (mode) => set({ mode }),
      setMessages: (messages) => set({ messages }),
      addMessage: (message) => set((state) => ({ 
        messages: [...state.messages, message] 
      })),
      clearSession: () => set({ sessionId: null, messages: [] }),
      _hydrated: false,
      setHydrated: (h) => set({ _hydrated: h }),
    }),
    {
      name: "ai-tutor-storage",
      onRehydrateStorage: () => (state) => {
        state?.setHydrated(true);
      },
    }
  )
);
