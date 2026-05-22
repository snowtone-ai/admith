interface CardProps {
  title?: string;
  variant?: "default" | "elevated" | "interactive";
  selected?: boolean;
  children: React.ReactNode;
  className?: string;
}

export function Card({ title, variant = "default", selected, children, className }: CardProps) {
  const base = "rounded-lg border border-hairline p-6";
  const variants: Record<string, string> = {
    default: "bg-surface-1",
    elevated: "bg-surface-2",
    interactive: [
      "bg-surface-1 hoverable cursor-pointer",
      "hover:bg-surface-2 hover:border-hairline-strong",
      selected ? "border-l-2 border-l-accent" : "",
    ].join(" "),
  };

  return (
    <section className={[base, variants[variant], className ?? ""].join(" ")}>
      {title ? (
        <h2 className="font-display text-base font-semibold tracking-tight text-ink">{title}</h2>
      ) : null}
      <div className={title ? "mt-3" : ""}>{children}</div>
    </section>
  );
}
