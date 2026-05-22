"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";

export default function LoginPage() {
  const [key, setKey] = useState("");
  return (
    <main className="max-w-md">
      <h1 className="font-display text-4xl">運用画面ログイン</h1>
      <input className="mt-4 w-full rounded-xl border p-3" value={key} onChange={(event) => setKey(event.target.value)} placeholder="管理者から共有された運用キー" />
      <Button className="mt-4" disabled={!key} onClick={() => { document.cookie = `admith_api_key=${encodeURIComponent(key)}; path=/; max-age=43200; SameSite=Strict`; location.href = "/"; }}>ログイン</Button>
    </main>
  );
}
