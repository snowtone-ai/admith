interface StatCardProps {
  label: string;
  value: string | number;
  delta?: number;
  variant?: "default" | "positive" | "negative";
  className?: string;
  live?: boolean;
}

export function StatCard({ label, value, delta, variant = "default", className, live }: StatCardProps) {
  const bgStyles: Record<string, string> = {
    default: "bg-surface-1",
    positive: "bg-positive-subtle",
    negative: "bg-negative-subtle",
  };

  const deltaColor = delta !== undefined && delta >= 0 ? "text-positive" : "text-negative";
  const deltaBg = delta !== undefined && delta >= 0 ? "bg-positive-subtle" : "bg-negative-subtle";
  const deltaPrefix = delta !== undefined && delta >= 0 ? "+" : "";

  return (
    <div
      className={[
        "rounded-lg border border-hairline p-6",
        bgStyles[variant],
        live ? "data-live" : "",
        className ?? "",
      ].join(" ")}
    >
      <p className="font-mono text-[11px] font-medium uppercase tracking-[0.08em] text-ink-subtle">
        {label}
      </p>
      <p className="mt-2 font-mono text-[28px] font-semibold leading-tight tracking-tight text-ink" style={{ fontFeatureSettings: "'tnum', 'lnum'" }}>
        {value}
      </p>
      {delta !== undefined ? (
        <span className={["mt-1 inline-block rounded-full px-2 py-0.5 font-mono text-[11px]", deltaColor, deltaBg].join(" ")}>
          {deltaPrefix}{delta.toFixed(1)}%
        </span>
      ) : null}
    </div>
  );
}
