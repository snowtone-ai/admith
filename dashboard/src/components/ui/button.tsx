import { forwardRef } from "react";

type ButtonVariant = "accent" | "surface" | "ghost" | "danger";
type ButtonSize = "sm" | "md" | "lg";

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  size?: ButtonSize;
  loading?: boolean;
}

const variantStyles: Record<ButtonVariant, string> = {
  accent:  "bg-accent text-white hover:bg-accent-hover active:bg-accent-pressed",
  surface: "bg-surface-2 text-ink hover:bg-surface-3",
  ghost:   "bg-transparent text-ink-muted hover:bg-surface-1 hover:text-ink",
  danger:  "bg-negative text-white hover:brightness-110",
};

const sizeStyles: Record<ButtonSize, string> = {
  sm: "h-8 px-3 text-[13px]",
  md: "h-10 px-5 text-[14px]",
  lg: "h-12 px-6 text-[14px]",
};

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(
  ({ variant = "accent", size = "md", loading, children, className, disabled, ...props }, ref) => {
    return (
      <button
        ref={ref}
        disabled={disabled || loading}
        className={[
          "inline-flex items-center justify-center rounded-md font-body font-medium",
          "transition-colors duration-150",
          variantStyles[variant],
          sizeStyles[size],
          (disabled || loading) ? "opacity-40 cursor-not-allowed" : "",
          className ?? "",
        ].join(" ")}
        {...props}
      >
        {loading ? (
          <svg className="h-4 w-4 animate-spin" viewBox="0 0 24 24" fill="none">
            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z" />
          </svg>
        ) : children}
      </button>
    );
  }
);

Button.displayName = "Button";
