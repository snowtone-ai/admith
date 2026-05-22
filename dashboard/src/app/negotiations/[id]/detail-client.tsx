"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { apiFetch } from "@/lib/api";
import { approvalTermsRows, auditEventSummary, auditEventTitle, friendlyError, negotiationStateLabel } from "@/lib/presentation";

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

  return (
    <main className="space-y-5">
      <h1 className="font-display text-4xl">交渉詳細</h1>
      <Card title="状態">
        <p>{negotiationStateLabel(detail?.state)}</p>
        {detail?.state === "pending_human_approval" ? <Link className="mt-3 inline-block font-semibold text-leaf" href={`/negotiations/${negotiationId}/approve`}>決裁内容を確認する</Link> : null}
      </Card>
      <Card title="合意案">
        <dl className="grid gap-3 md:grid-cols-2">
          {approvalTermsRows(detail?.agreement?.terms).map((row) => (
            <div key={row.label} className="rounded-xl bg-wheat/30 p-3">
              <dt className="text-sm text-soil/70">{row.label}</dt>
              <dd className={row.emphasis ? "text-2xl font-bold" : "font-semibold"}>{row.value}</dd>
            </div>
          ))}
        </dl>
        {!detail?.agreement ? <p>合意案はまだ作成されていません。</p> : null}
      </Card>
      <Card title="これまでの流れ">
        <div className="space-y-2">
          {detail?.audit_events.map((event) => (
            <div key={`${event.sequence_number}-${event.event_type}`} className="rounded-xl border bg-white p-3">
              <p className="font-semibold">{event.sequence_number}. {auditEventTitle(event.event_type)}</p>
              <p className="mt-1 text-sm text-soil/75">{auditEventSummary(event.event_data)}</p>
            </div>
          ))}
        </div>
      </Card>
      {message ? <p className="text-red-700">{friendlyError(message)}</p> : null}
    </main>
  );
}
