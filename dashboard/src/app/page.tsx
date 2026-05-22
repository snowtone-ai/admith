"use client";

import { useEffect, useState } from "react";
import { apiFetch } from "@/lib/api";
import { formatYen, friendlyError } from "@/lib/presentation";
import { StatCard } from "@/components/admith/StatCard";
import { ResourceCard } from "@/components/admith/ResourceCard";
import { NegotiationTimeline, type TimelineStep } from "@/components/admith/NegotiationTimeline";
import { ValueConversionIndicator } from "@/components/admith/ValueConversionIndicator";

type Metrics = {
  active_negotiations: number;
  pending_approvals: number;
  today_delta_yen: number;
};

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

type AuditEvent = {
  audit_id: string;
  negotiation_id: string | null;
  sequence_number: number;
  event_type: string;
  event_data: Record<string, unknown>;
};

const auditToStep = (event: AuditEvent, index: number, total: number): TimelineStep => ({
  id: event.audit_id,
  label: event.event_type.replace("action.", "").replace("circuit_breaker.", ""),
  status: index === total - 1 ? "active" : "completed",
  timestamp: undefined,
  agent: event.event_data.agent_id ? String(event.event_data.agent_id) : undefined,
});

const agentState = (state: string) => {
  if (state === "locked") return "negotiating" as const;
  if (state === "settled") return "idle" as const;
  return "active" as const;
};

export default function Page() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [resources, setResources] = useState<Resource[]>([]);
  const [events, setEvents] = useState<AuditEvent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [converting, setConverting] = useState(false);

  useEffect(() => {
    Promise.all([
      apiFetch<Metrics>("/dashboard/metrics").then(setMetrics),
      apiFetch<Resource[]>("/resources").then(setResources),
      apiFetch<AuditEvent[]>("/audit-events").then(setEvents),
    ]).catch((reason) => setError(String(reason)));
  }, []);

  useEffect(() => {
    if (metrics && metrics.today_delta_yen > 0) {
      const timer = setTimeout(() => setConverting(true), 500);
      return () => clearTimeout(timer);
    }
  }, [metrics]);

  const totalDelta = metrics?.today_delta_yen ?? 0;
  const timelineSteps = events.slice(-10).map((e, i, arr) => auditToStep(e, i, arr.length));

  return (
    <div className="space-y-8">
      {/* Section 1 -- KPI */}
      <section className="grid gap-4 md:grid-cols-3">
        <StatCard
          label="本日の取引件数"
          value={metrics?.active_negotiations ?? "-"}
          live
        />
        <StatCard
          label="総転換額"
          value={metrics ? formatYen(totalDelta) : "-"}
          variant={totalDelta > 0 ? "positive" : "default"}
        />
        <StatCard
          label="稼働エージェント数"
          value={metrics?.pending_approvals ?? "-"}
          live
        />
      </section>

      {/* Section 2 -- Active Resources */}
      <section className="mt-8">
        <p className="font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-ink-subtle">
          アクティブリソース
        </p>
        <div className="mt-4 grid gap-4" style={{ gridTemplateColumns: "repeat(auto-fill, minmax(320px, 1fr))" }}>
          {resources.map((r) => (
            <ResourceCard
              key={r.resource_id}
              name={r.attributes.material ?? r.resource_type}
              category={r.attributes.required_use ?? "食品残さ"}
              value={-(r.attributes.disposal_cost_yen ?? 0)}
              agentState={agentState(r.state)}
              onClick={() => { location.href = `/resources`; }}
            />
          ))}
          {resources.length === 0 && !error ? (
            <p className="text-[13px] text-ink-muted">リソースはまだ登録されていません。</p>
          ) : null}
        </div>
      </section>

      {/* Section 3 -- Negotiation Timeline */}
      {timelineSteps.length > 0 ? (
        <section className="mt-8">
          <p className="font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-ink-subtle">
            交渉タイムライン
          </p>
          <div className="mt-4 rounded-lg border border-hairline bg-surface-1 p-4">
            <NegotiationTimeline steps={timelineSteps} />
          </div>
        </section>
      ) : null}

      {/* Section 4 -- Conversion Summary */}
      <section className="mt-8 rounded-lg border border-hairline bg-surface-1 p-8 text-center">
        <ValueConversionIndicator
          from={totalDelta > 0 ? -totalDelta : 0}
          to={totalDelta}
          converting={converting}
          size="lg"
        />
        <p className="mt-4 text-[15px] leading-relaxed text-ink-muted" style={{ lineHeight: 1.7 }}>
          {totalDelta > 0
            ? `本日 ${events.filter((e) => e.event_type === "action.SettleDeal").length}件の廃棄を価値に転換しました`
            : "本日の転換データはまだありません"}
        </p>
      </section>

      {error ? (
        <p className="text-[13px] text-negative">{friendlyError(error)}</p>
      ) : null}
    </div>
  );
}
