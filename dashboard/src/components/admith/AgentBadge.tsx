export type AgentState = "idle" | "active" | "negotiating";

interface AgentBadgeProps {
  state: AgentState;
  label?: string;
  className?: string;
}

const stateStyles: Record<AgentState, string> = {
  idle: "bg-surface-2 text-ink-muted",
  active: "bg-[rgba(124,58,237,0.20)] text-accent agent-active",
  negotiating: "bg-warning-subtle text-warning data-live",
};

const stateLabels: Record<AgentState, string> = {
  idle: "待機中",
  active: "稼働中",
  negotiating: "交渉中",
};

export function AgentBadge({ state, label, className }: AgentBadgeProps) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-2.5 py-1 font-mono text-[11px] font-medium",
        stateStyles[state],
        className ?? "",
      ].join(" ")}
    >
      {label ?? stateLabels[state]}
    </span>
  );
}
