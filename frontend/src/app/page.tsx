"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { useStore } from "@/store/useStore";
import { Sidebar } from "@/components/Sidebar";
import { Chat } from "@/components/Chat";

export default function Home() {
  const { user, _hydrated } = useStore();
  const router = useRouter();

  useEffect(() => {
    if (_hydrated && !user) {
      router.push("/login");
    }
  }, [_hydrated, user, router]);

  if (!_hydrated) return null;
  if (!user) return null;

  return (
    <main className="flex h-screen w-screen overflow-hidden">
      <Sidebar />
      <Chat />
    </main>
  );
}
