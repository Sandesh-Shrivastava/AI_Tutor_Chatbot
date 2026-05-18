import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useStore } from "@/store/useStore";
import { Sidebar } from "@/components/Sidebar";
import { Chat } from "@/components/Chat";

export default function Home() {
  const { user, _hydrated } = useStore();
  const navigate = useNavigate();

  useEffect(() => {
    if (_hydrated && !user) {
      navigate("/login");
    }
  }, [_hydrated, user, navigate]);

  if (!_hydrated) return null;
  if (!user) return null;

  return (
    <main className="flex h-screen w-screen overflow-hidden">
      <Sidebar />
      <Chat />
    </main>
  );
}
