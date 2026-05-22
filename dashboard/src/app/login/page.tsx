"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/Input";

export default function LoginPage() {
  const [key, setKey] = useState("");
  return (
    <div className="flex min-h-[60vh] items-center justify-center">
      <div className="w-full max-w-md rounded-lg border border-hairline bg-surface-1 p-8">
        <h1 className="font-display text-[24px] font-semibold tracking-tight" style={{ letterSpacing: "-0.4px" }}>
          運用画面ログイン
        </h1>
        <div className="mt-6">
          <Input
            label="運用キー"
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="管理者から共有された運用キー"
            type="password"
          />
        </div>
        <Button
          className="mt-6 w-full"
          disabled={!key}
          onClick={() => {
            document.cookie = `admith_api_key=${encodeURIComponent(key)}; path=/; max-age=43200; SameSite=Strict`;
            location.href = "/";
          }}
        >
          ログイン
        </Button>
      </div>
    </div>
  );
}
