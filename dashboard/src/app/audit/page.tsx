"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/Badge";
import { apiFetch } from "@/lib/api";
import { auditEventSummary, auditEventTitle, friendlyError } from "@/lib/presentation";

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
    <div className="space-y-6">
      <h1 className="font-display text-[32px] font-semibold tracking-tight" style={{ letterSpacing: "-0.8px" }}>
        監査ログ
      </h1>

      <Card title="改ざん防止の取引記録">
        <div className="space-y-3">
          {rows.map((row) => (
            <div
              key={row.audit_id}
              className="rounded-lg border border-hairline bg-canvas p-4 hoverable hover:bg-surface-1"
            >
              <div className="flex items-center gap-3">
                <span className="font-mono text-[11px] tabular-nums text-ink-subtle" style={{ fontFeatureSettings: "'tnum', 'lnum'" }}>
                  {row.sequence_number}
                </span>
                <p className="text-[14px] font-medium text-ink">{auditEventTitle(row.event_type)}</p>
              </div>
              <div className="mt-2 flex flex-wrap items-center gap-2">
                <Badge>{row.negotiation_id ? `取引 ${row.negotiation_id.slice(0, 8)}` : "システム"}</Badge>
                <span className="text-[13px] text-ink-muted">{auditEventSummary(row.event_data)}</span>
              </div>
            </div>
          ))}
          {rows.length === 0 ? (
            <p className="text-[13px] text-ink-muted">監査イベントはまだありません。</p>
          ) : null}
        </div>
      </Card>

      {message ? <p className="text-[13px] text-negative">{friendlyError(message)}</p> : null}
    </div>
  );
}
