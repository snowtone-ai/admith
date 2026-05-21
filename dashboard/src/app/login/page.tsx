"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const [key, setKey] = useState("test-key");
  return <main className="max-w-md"><h1 className="font-display text-4xl">APIキー</h1><input className="mt-4 w-full rounded-xl border p-3" value={key} onChange={(event) => setKey(event.target.value)} /><Button className="mt-4" onClick={() => { localStorage.setItem("admith_api_key", key); document.cookie = `admith_api_key=${encodeURIComponent(key)}; path=/; max-age=86400; SameSite=Lax`; location.href = "/"; }}>ログイン</Button></main>;
}
