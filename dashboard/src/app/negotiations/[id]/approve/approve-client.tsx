"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";

type Detail = {
  state: string;
  displayed_terms_hash: string | null;
  agreement: { terms: Record<string, unknown> } | null;
};

export function ApproveClient({ negotiationId }: { negotiationId: string }) {
  const [detail, setDetail] = useState<Detail | null>(null);
  const [decision, setDecision] = useState<"approve" | "reject">("approve");
  const [reason, setReason] = useState("");
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<Detail>(`/negotiations/${negotiationId}`).then(setDetail).catch((error) => setMessage(String(error)));
  }, [negotiationId]);

  async function submit() {
    if (!detail?.displayed_terms_hash) return;
    if (!reason) return;
    const path = decision === "approve" ? "approve" : "reject";
    try {
      await apiFetch(`/negotiations/${negotiationId}/${path}`, {
        method: "POST",
        body: JSON.stringify({ reason, displayed_terms_hash: detail.displayed_terms_hash })
      });
      location.href = `/negotiations/${negotiationId}`;
    } catch (error) {
      setMessage(String(error));
    }
  }

  return (
    <main className="space-y-5">
      <h1 className="font-display text-4xl">承認画面</h1>
      <section className="rounded-3xl border bg-white/75 p-5">
        <p>状態: {detail?.state ?? "loading"}</p>
        <pre className="mt-3 overflow-auto rounded-xl bg-wheat/30 p-3 text-sm">{JSON.stringify(detail?.agreement?.terms ?? {}, null, 2)}</pre>
      </section>
      <fieldset className="flex gap-4">
        <label><input type="radio" checked={decision === "approve"} onChange={() => setDecision("approve")} /> approve</label>
        <label><input type="radio" checked={decision === "reject"} onChange={() => setDecision("reject")} /> reject</label>
      </fieldset>
      <textarea className="w-full rounded-xl border p-3" placeholder="reason" value={reason} onChange={(event) => setReason(event.target.value)} />
      <Button onClick={submit} disabled={!detail || !reason || detail.state !== "pending_human_approval"}>送信</Button>
      {message ? <p>{message}</p> : null}
    </main>
  );
}
