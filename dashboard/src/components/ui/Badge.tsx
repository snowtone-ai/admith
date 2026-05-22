type BadgeVariant = "default" | "positive" | "negative" | "warning" | "info";

interface BadgeProps {
  variant?: BadgeVariant;
  children: React.ReactNode;
  className?: string;
}

const variantStyles: Record<BadgeVariant, string> = {
  default:  "bg-surface-3 text-ink-muted",
  positive: "bg-positive-subtle text-positive",
  negative: "bg-negative-subtle text-negative",
  warning:  "bg-warning-subtle text-warning",
  info:     "bg-info-subtle text-info",
};

export function Badge({ variant = "default", children, className }: BadgeProps) {
  return (
    <span
      className={[
        "inline-flex items-center rounded-full px-2 py-0.5 font-mono text-[11px] leading-tight",
        "font-[500]",
        variantStyles[variant],
        className ?? "",
      ].join(" ")}
    >
      {children}
    </span>
  );
}
