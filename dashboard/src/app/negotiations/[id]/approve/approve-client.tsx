"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { apiFetch } from "@/lib/api";
import { approvalDisabledReason, approvalTermsRows, friendlyError, negotiationStateLabel } from "@/lib/presentation";

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
      <h1 className="font-display text-4xl">決裁確認</h1>
      <section className="rounded-3xl border bg-white/75 p-5">
        <p>現在の状況: {negotiationStateLabel(detail?.state)}</p>
        <dl className="mt-3 grid gap-3 md:grid-cols-2">
          {approvalTermsRows(detail?.agreement?.terms).map((row) => (
            <div key={row.label} className="rounded-xl bg-wheat/30 p-3">
              <dt className="text-sm text-soil/70">{row.label}</dt>
              <dd className={row.emphasis ? "text-2xl font-bold" : "font-semibold"}>{row.value}</dd>
            </div>
          ))}
        </dl>
      </section>
      <fieldset className="flex gap-4">
        <label><input type="radio" checked={decision === "approve"} onChange={() => setDecision("approve")} /> この条件で承認する</label>
        <label><input type="radio" checked={decision === "reject"} onChange={() => setDecision("reject")} /> 差し戻す</label>
      </fieldset>
      <textarea className="w-full rounded-xl border p-3" placeholder="判断理由を入力してください" value={reason} onChange={(event) => setReason(event.target.value)} />
      {approvalDisabledReason(detail?.state) ? <p className="text-sm text-soil/70">{approvalDisabledReason(detail?.state)}</p> : null}
      <Button onClick={submit} disabled={!detail || !reason || detail.state !== "pending_human_approval"}>判断を記録する</Button>
      {message ? <p>{friendlyError(message)}</p> : null}
    </main>
  );
}
