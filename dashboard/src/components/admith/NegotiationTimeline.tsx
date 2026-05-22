import { AgentBadge, type AgentState } from "./AgentBadge";

export interface TimelineStep {
  id: string;
  label: string;
  status: "pending" | "active" | "completed";
  timestamp?: string;
  agent?: string;
}

interface NegotiationTimelineProps {
  steps: TimelineStep[];
}

const dotStyles: Record<string, string> = {
  pending: "bg-ink-ghost",
  active: "bg-accent agent-active",
  completed: "bg-positive",
};

const textStyles: Record<string, string> = {
  pending: "text-ink-ghost",
  active: "text-accent",
  completed: "text-ink-muted",
};

const rowBg: Record<string, string> = {
  pending: "",
  active: "bg-[var(--color-accent-glow)] rounded-md",
  completed: "",
};

function agentStateFromStepStatus(status: string): AgentState {
  if (status === "active") return "active";
  if (status === "completed") return "idle";
  return "idle";
}

export function NegotiationTimeline({ steps }: NegotiationTimelineProps) {
  return (
    <div className="space-y-0">
      {steps.map((step, i) => (
        <div key={step.id} className={["flex gap-4 p-3", rowBg[step.status]].join(" ")}>
          {/* Dot + line */}
          <div className="flex flex-col items-center">
            <div className={["h-3 w-3 shrink-0 rounded-full", dotStyles[step.status]].join(" ")}>
              {step.status === "completed" ? (
                <svg className="h-3 w-3 text-white" viewBox="0 0 12 12" fill="none">
                  <path d="M2.5 6l2.5 2.5 4.5-5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
                </svg>
              ) : null}
            </div>
            {i < steps.length - 1 ? (
              <div className="w-px flex-1 border-l border-hairline" />
            ) : null}
          </div>
          {/* Content */}
          <div className="flex-1 pb-4">
            <p className={["text-[13px] font-medium leading-relaxed", textStyles[step.status]].join(" ")}>
              {step.label}
            </p>
            <div className="mt-1 flex flex-wrap items-center gap-2">
              {step.timestamp ? (
                <span className="font-mono text-[11px] text-ink-subtle">{step.timestamp}</span>
              ) : null}
              {step.agent ? (
                <AgentBadge state={agentStateFromStepStatus(step.status)} label={step.agent} />
              ) : null}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
