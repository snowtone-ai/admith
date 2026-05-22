"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { apiFetch } from "@/lib/api";
import { friendlyError, negotiationStateLabel } from "@/lib/presentation";

type Negotiation = {
  negotiation_id: string;
  resource_id: string;
  state: string;
};

export default function NegotiationsPage() {
  const [rows, setRows] = useState<Negotiation[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<Negotiation[]>("/negotiations").then(setRows).catch((error) => setMessage(String(error)));
  }, []);

  return (
    <main className="space-y-5">
      <h1 className="font-display text-4xl">交渉一覧</h1>
      <Card title="交渉">
        <div className="space-y-3">
          {rows.map((row) => (
            <Link key={row.negotiation_id} href={`/negotiations/${row.negotiation_id}`} className="block rounded-2xl border bg-white p-4 hover:border-leaf">
              <p className="font-semibold">{negotiationStateLabel(row.state)}</p>
              <p className="break-all text-sm">取引番号: {row.negotiation_id}</p>
              <p className="break-all text-sm">食品残さ番号: {row.resource_id}</p>
            </Link>
          ))}
          {rows.length === 0 ? <p>取引はまだありません。食品残さ画面から開始してください。</p> : null}
        </div>
      </Card>
      {message ? <p className="text-red-700">{friendlyError(message)}</p> : null}
    </main>
  );
}
