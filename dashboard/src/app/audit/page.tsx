"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { apiFetch } from "@/lib/api";

type AuditEvent = {
  audit_id: string;
  negotiation_id: string | null;
  sequence_number: number;
  event_type: string;
  event_data: Record<string, unknown>;
};

export default function AuditPage() {
  const [rows, setRows] = useState<AuditEvent[]>([]);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<AuditEvent[]>("/audit-events").then(setRows).catch((error) => setMessage(String(error)));
  }, []);

  return (
    <main className="space-y-5">
      <h1 className="font-display text-4xl">監査ログ</h1>
      <Card title="Append-only Events">
        <div className="space-y-3">
          {rows.map((row) => (
            <div key={row.audit_id} className="rounded-2xl border bg-white p-4">
              <p className="font-semibold">#{row.sequence_number} {row.event_type}</p>
              <p className="break-all text-sm">Negotiation: {row.negotiation_id ?? "-"}</p>
              <pre className="mt-2 overflow-auto text-xs">{JSON.stringify(row.event_data, null, 2)}</pre>
            </div>
          ))}
          {rows.length === 0 ? <p>監査イベントはまだありません。</p> : null}
        </div>
      </Card>
      {message ? <p className="text-red-700">{message}</p> : null}
    </main>
  );
}
