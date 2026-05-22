"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/button";
import { NegotiationTimeline, type TimelineStep } from "@/components/admith/NegotiationTimeline";
import { apiFetch } from "@/lib/api";
import { approvalTermsRows, auditEventTitle, friendlyError, negotiationStateLabel } from "@/lib/presentation";

type Detail = {
  state: string;
  agreement: { terms: Record<string, unknown> } | null;
  audit_events: Array<{ event_type: string; sequence_number: number; event_data: Record<string, unknown> }>;
};

export function NegotiationDetailClient({ negotiationId }: { negotiationId: string }) {
  const [detail, setDetail] = useState<Detail | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<Detail>(`/negotiations/${negotiationId}`).then(setDetail).catch((error) => setMessage(String(error)));
  }, [negotiationId]);

  const timelineSteps: TimelineStep[] = (detail?.audit_events ?? []).map((event, i, arr) => ({
    id: `${event.sequence_number}-${event.event_type}`,
    label: auditEventTitle(event.event_type),
    status: i === arr.length - 1 ? "active" : "completed",
    timestamp: undefined,
  }));

  const termRows = approvalTermsRows(detail?.agreement?.terms);

  return (
    <div className="space-y-6">
      <h1 className="font-display text-[32px] font-semibold tracking-tight" style={{ letterSpacing: "-0.8px" }}>
        交渉詳細
      </h1>

      <Card title="状態">
        <div className="flex items-center gap-3">
          <Badge variant={detail?.state === "settled" ? "positive" : detail?.state === "pending_human_approval" ? "warning" : "info"}>
            {negotiationStateLabel(detail?.state)}
          </Badge>
          {detail?.state === "pending_human_approval" ? (
            <Link href={`/negotiations/${negotiationId}/approve`}>
              <Button size="sm">決裁内容を確認する</Button>
            </Link>
          ) : null}
        </div>
      </Card>

      <Card title="合意案">
        {termRows.length > 0 ? (
          <dl className="grid gap-3 md:grid-cols-2">
            {termRows.map((row) => (
              <div key={row.label} className="rounded-lg bg-surface-2 p-4">
                <dt className="text-[13px] text-ink-muted">{row.label}</dt>
                <dd className={[
                  "mt-1 font-mono tabular-nums",
                  row.emphasis ? "text-[20px] font-bold" : "text-[15px] font-semibold",
                ].join(" ")} style={{ fontFeatureSettings: "'tnum', 'lnum'" }}>
                  {row.value}
                </dd>
              </div>
            ))}
          </dl>
        ) : (
          <p className="text-[13px] text-ink-muted">合意案はまだ作成されていません。</p>
        )}
      </Card>

      <Card title="これまでの流れ">
        {timelineSteps.length > 0 ? (
          <NegotiationTimeline steps={timelineSteps} />
        ) : (
          <p className="text-[13px] text-ink-muted">タイムラインデータを読み込み中...</p>
        )}
      </Card>

      {message ? <p className="text-[13px] text-negative">{friendlyError(message)}</p> : null}
    </div>
  );
}
