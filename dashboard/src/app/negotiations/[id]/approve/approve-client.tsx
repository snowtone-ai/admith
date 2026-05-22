"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/Badge";
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

  const termRows = approvalTermsRows(detail?.agreement?.terms);
  const disabledReason = approvalDisabledReason(detail?.state);

  return (
    <div className="space-y-6">
      <h1 className="font-display text-[32px] font-semibold tracking-tight" style={{ letterSpacing: "-0.8px" }}>
        決裁確認
      </h1>

      <Card title="取引条件">
        <div className="mb-4 flex items-center gap-2">
          <span className="text-[13px] text-ink-muted">現在の状況:</span>
          <Badge variant={detail?.state === "pending_human_approval" ? "warning" : "info"}>
            {negotiationStateLabel(detail?.state)}
          </Badge>
        </div>
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
        ) : null}
      </Card>

      <Card title="判断">
        <fieldset className="flex gap-6">
          <label className="flex items-center gap-2 text-[14px] text-ink cursor-pointer">
            <input
              type="radio"
              checked={decision === "approve"}
              onChange={() => setDecision("approve")}
              className="accent-accent"
            />
            この条件で承認する
          </label>
          <label className="flex items-center gap-2 text-[14px] text-ink cursor-pointer">
            <input
              type="radio"
              checked={decision === "reject"}
              onChange={() => setDecision("reject")}
              className="accent-negative"
            />
            差し戻す
          </label>
        </fieldset>

        <textarea
          className="mt-4 w-full rounded-md border border-hairline bg-surface-1 p-3.5 text-[15px] text-ink placeholder:text-ink-ghost focus:border-accent"
          placeholder="判断理由を入力してください"
          rows={3}
          value={reason}
          onChange={(e) => setReason(e.target.value)}
        />

        {disabledReason ? (
          <p className="mt-2 text-[13px] text-ink-muted">{disabledReason}</p>
        ) : null}

        <div className="mt-4">
          <Button
            variant={decision === "reject" ? "danger" : "accent"}
            onClick={submit}
            disabled={!detail || !reason || detail.state !== "pending_human_approval"}
          >
            判断を記録する
          </Button>
        </div>
      </Card>

      {message ? <p className="text-[13px] text-negative">{friendlyError(message)}</p> : null}
    </div>
  );
}
