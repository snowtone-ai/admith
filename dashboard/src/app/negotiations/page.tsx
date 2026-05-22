"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/Badge";
import { apiFetch } from "@/lib/api";
import { friendlyError, negotiationStateLabel } from "@/lib/presentation";

type Negotiation = {
  negotiation_id: string;
  resource_id: string;
  state: string;
};

const stateBadgeVariant = (state: string) => {
  if (state === "settled") return "positive" as const;
  if (state === "failed" || state === "expired") return "negative" as const;
  if (state === "pending_human_approval") return "warning" as const;
  return "info" as const;
};

export default function NegotiationsPage() {
  const [rows, setRows] = useState<Negotiation[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<Negotiation[]>("/negotiations").then(setRows).catch((error) => setMessage(String(error)));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="font-display text-[32px] font-semibold tracking-tight" style={{ letterSpacing: "-0.8px" }}>
        交渉一覧
      </h1>

      <Card title="交渉">
        <div className="space-y-3">
          {rows.map((row) => (
            <Link
              key={row.negotiation_id}
              href={`/negotiations/${row.negotiation_id}`}
              className="block rounded-lg border border-hairline bg-canvas p-4 hoverable hover:bg-surface-1 hover:border-hairline-strong"
            >
              <div className="flex items-center gap-3">
                <Badge variant={stateBadgeVariant(row.state)}>
                  {negotiationStateLabel(row.state)}
                </Badge>
              </div>
              <div className="mt-2 flex flex-wrap gap-4 text-[13px] text-ink-muted">
                <span>取引番号: <span className="font-mono text-[11px]">{row.negotiation_id}</span></span>
                <span>食品残さ番号: <span className="font-mono text-[11px]">{row.resource_id}</span></span>
              </div>
            </Link>
          ))}
          {rows.length === 0 ? (
            <p className="text-[13px] text-ink-muted">取引はまだありません。食品残さ画面から開始してください。</p>
          ) : null}
        </div>
      </Card>

      {message ? <p className="text-[13px] text-negative">{friendlyError(message)}</p> : null}
    </div>
  );
}
