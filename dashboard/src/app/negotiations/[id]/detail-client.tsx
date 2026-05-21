"use client";

import Link from "next/link";
import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { apiFetch } from "@/lib/api";

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
        <p>{detail?.state ?? "loading"}</p>
        {detail?.state === "pending_human_approval" ? <Link className="mt-3 inline-block font-semibold text-leaf" href={`/negotiations/${negotiationId}/approve`}>承認画面へ</Link> : null}
      </Card>
      <Card title="Agreement Terms">
        <pre className="overflow-auto rounded-xl bg-wheat/30 p-3 text-sm">{JSON.stringify(detail?.agreement?.terms ?? {}, null, 2)}</pre>
      </Card>
      <Card title="Timeline">
        <div className="space-y-2">
          {detail?.audit_events.map((event) => (
            <div key={`${event.sequence_number}-${event.event_type}`} className="rounded-xl border bg-white p-3">
              <p className="font-semibold">#{event.sequence_number} {event.event_type}</p>
              <pre className="mt-2 overflow-auto text-xs">{JSON.stringify(event.event_data, null, 2)}</pre>
            </div>
          ))}
        </div>
      </Card>
      {message ? <p className="text-red-700">{message}</p> : null}
    </main>
  );
}
