import { Badge } from "@/components/ui/Badge";
import { AgentBadge, type AgentState } from "./AgentBadge";

interface ResourceCardProps {
  name: string;
  category: string;
  value: number;
  deadline?: Date;
  agentState: AgentState;
  className?: string;
  onClick?: () => void;
}

function deadlineLabel(deadline: Date): { text: string; urgent: boolean } {
  const ms = deadline.getTime() - Date.now();
  if (ms <= 0) return { text: "期限切れ", urgent: true };
  const minutes = Math.floor(ms / 60000);
  if (minutes < 60) return { text: `あと ${minutes}分`, urgent: minutes < 30 };
  const hours = Math.floor(minutes / 60);
  if (hours < 24) return { text: `あと ${hours}時間`, urgent: true };
  const days = Math.floor(hours / 24);
  return { text: `あと ${days}日`, urgent: false };
}

export function ResourceCard({ name, category, value, deadline, agentState, className, onClick }: ResourceCardProps) {
  const valueColor = value >= 0 ? "text-positive" : "text-negative";
  const valuePrefix = value >= 0 ? "+" : "\u2212";
  const absValue = Math.abs(value);

  const dl = deadline ? deadlineLabel(deadline) : null;

  return (
    <div
      className={[
        "rounded-lg border border-hairline bg-surface-1 p-5 hoverable",
        "hover:bg-surface-2 hover:border-hairline-strong",
        onClick ? "cursor-pointer" : "",
        className ?? "",
      ].join(" ")}
      onClick={onClick}
      role={onClick ? "button" : undefined}
      tabIndex={onClick ? 0 : undefined}
      onKeyDown={onClick ? (e) => { if (e.key === "Enter" || e.key === " ") onClick(); } : undefined}
    >
      <div className="flex items-start justify-between">
        <h3 className="font-display text-[16px] font-semibold tracking-tight">{name}</h3>
        <Badge>{category}</Badge>
      </div>
      <p
        className={["mt-3 font-mono text-[16px] font-medium", valueColor].join(" ")}
        style={{ fontFeatureSettings: "'tnum', 'lnum'" }}
      >
        {valuePrefix}{new Intl.NumberFormat("ja-JP").format(absValue)}
      </p>
      <div className="mt-3 flex items-center gap-3">
        {dl ? (
          <span className={["flex items-center gap-1 text-[13px]", dl.urgent ? "text-warning" : "text-ink-muted"].join(" ")}>
            {dl.urgent ? (
              <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M12 9v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            ) : null}
            {dl.text}
          </span>
        ) : null}
        <AgentBadge state={agentState} />
      </div>
    </div>
  );
}
