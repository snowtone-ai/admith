"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/Badge";
import { Table } from "@/components/ui/Table";
import { AgentBadge } from "@/components/admith/AgentBadge";
import { ValueConversionIndicator } from "@/components/admith/ValueConversionIndicator";
import { NegotiationTimeline, type TimelineStep } from "@/components/admith/NegotiationTimeline";
import { apiFetch } from "@/lib/api";
import {
  auditEventTitle,
  formatKg,
  formatMaterial,
  formatRequiredUse,
  formatYen,
  formatYenPerKg,
  friendlyError,
  resourceStateLabel,
} from "@/lib/presentation";

type Resource = {
  resource_id: string;
  resource_type: string;
  state: string;
  attributes: {
    material?: string;
    quantity_kg?: number;
    disposal_cost_yen?: number;
    required_use?: string;
  };
};

type Negotiation = {
  negotiation_id: string;
  state: string;
  agreement: { terms: Record<string, unknown> } | null;
  audit_events: Array<{
    event_type: string;
    sequence_number: number;
    event_data: Record<string, unknown>;
  }>;
};

type RoundRow = {
  round: number;
  price: string;
  timestamp: string;
  agent: string;
};

const roundColumns = [
  { key: "round", header: "ラウンド", numeric: true },
  { key: "price", header: "提示価格", numeric: true },
  { key: "timestamp", header: "タイムスタンプ" },
  { key: "agent", header: "エージェントID" },
];

function buildRoundRows(events: Negotiation["audit_events"]): RoundRow[] {
  return events.map((e, i) => ({
    round: i + 1,
    price:
      typeof e.event_data.price_yen_per_kg === "number"
        ? formatYenPerKg(e.event_data.price_yen_per_kg)
        : "-",
    timestamp:
      typeof e.event_data.timestamp === "string"
        ? e.event_data.timestamp
        : `seq #${e.sequence_number}`,
    agent:
      typeof e.event_data.agent_id === "string"
        ? e.event_data.agent_id
        : "system",
  }));
}

export function ResourceDetailClient({ resourceId }: { resourceId: string }) {
  const [resource, setResource] = useState<Resource | null>(null);
  const [negotiation, setNegotiation] = useState<Negotiation | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<Resource>(`/resources/${resourceId}`)
      .then(async (res) => {
        setResource(res);
        if (res.state !== "available") {
          const negotiations = await apiFetch<Array<{ negotiation_id: string; resource_id: string }>>("/negotiations");
          const match = negotiations.find((n) => n.resource_id === resourceId);
          if (match) {
            const detail = await apiFetch<Negotiation>(`/negotiations/${match.negotiation_id}`);
            setNegotiation(detail);
          }
        }
      })
      .catch((error) => setMessage(String(error)));
  }, [resourceId]);

  const disposalCost = resource?.attributes.disposal_cost_yen ?? 0;
  const sellerDelta =
    typeof negotiation?.agreement?.terms?.seller_delta_yen === "number"
      ? (negotiation.agreement.terms.seller_delta_yen as number)
      : 0;
  const isSettled = resource?.state === "settled";

  const timelineSteps: TimelineStep[] = (negotiation?.audit_events ?? []).map((event, i, arr) => ({
    id: `${event.sequence_number}-${event.event_type}`,
    label: auditEventTitle(event.event_type),
    status: i === arr.length - 1 ? "active" : "completed",
    timestamp: undefined,
  }));

  const agents = Array.from(
    new Set(
      (negotiation?.audit_events ?? [])
        .map((e) => (typeof e.event_data.agent_id === "string" ? e.event_data.agent_id : null))
        .filter((a): a is string => a !== null)
    )
  );

  const roundRows = buildRoundRows(negotiation?.audit_events ?? []);

  return (
    <div className="space-y-6">
      <h1 className="font-display text-[32px] font-semibold tracking-tight" style={{ letterSpacing: "-0.8px" }}>
        リソース詳細
      </h1>

      {/* Hero: Resource overview */}
      <Card title={resource ? formatMaterial(resource.attributes.material ?? resource.resource_type) : "読み込み中"}>
        <div className="grid gap-6 md:grid-cols-2">
          <div className="space-y-3">
            <div className="flex items-center gap-2">
              <Badge
                variant={resource?.state === "available" ? "positive" : resource?.state === "settled" ? "info" : "warning"}
              >
                {resourceStateLabel(resource?.state)}
              </Badge>
            </div>
            <dl className="space-y-2 text-[13px]">
              <div className="flex gap-2">
                <dt className="text-ink-muted">数量:</dt>
                <dd className="font-mono tabular-nums" style={{ fontFeatureSettings: "'tnum', 'lnum'" }}>
                  {formatKg(resource?.attributes.quantity_kg)}
                </dd>
              </div>
              <div className="flex gap-2">
                <dt className="text-ink-muted">廃棄費:</dt>
                <dd className="font-mono tabular-nums text-negative" style={{ fontFeatureSettings: "'tnum', 'lnum'" }}>
                  {formatYen(resource?.attributes.disposal_cost_yen)}
                </dd>
              </div>
              <div className="flex gap-2">
                <dt className="text-ink-muted">用途:</dt>
                <dd>{formatRequiredUse(resource?.attributes.required_use)}</dd>
              </div>
            </dl>
          </div>
          <div className="flex flex-col items-center justify-center rounded-lg bg-surface-2 p-6">
            <span className="font-mono text-[11px] uppercase tracking-wider text-ink-subtle">価値転換</span>
            <div className="mt-3">
              <ValueConversionIndicator
                from={-disposalCost}
                to={sellerDelta}
                converting={isSettled}
                size="lg"
              />
            </div>
            <p className="mt-2 text-[13px] text-ink-muted" style={{ lineHeight: "1.7" }}>
              {isSettled ? "廃棄コストを価値に転換しました" : "転換前の廃棄コスト"}
            </p>
          </div>
        </div>
      </Card>

      {/* Negotiation timeline */}
      {timelineSteps.length > 0 ? (
        <Card title="交渉プロセス">
          <NegotiationTimeline steps={timelineSteps} />
        </Card>
      ) : null}

      {/* Participating agents */}
      {agents.length > 0 ? (
        <Card title="参加エージェント">
          <div className="flex flex-wrap gap-2">
            {agents.map((agent) => (
              <AgentBadge key={agent} state="idle" label={agent} />
            ))}
          </div>
        </Card>
      ) : null}

      {/* Detailed data table */}
      {roundRows.length > 0 ? (
        <Card title="交渉ラウンド詳細">
          <Table<RoundRow> columns={roundColumns} data={roundRows} keyField="round" />
        </Card>
      ) : null}

      {message ? <p className="text-[13px] text-negative">{friendlyError(message)}</p> : null}
    </div>
  );
}
