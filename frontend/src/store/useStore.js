import { create } from "zustand";
import { persist } from "zustand/middleware";

export const useStore = create()(
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
