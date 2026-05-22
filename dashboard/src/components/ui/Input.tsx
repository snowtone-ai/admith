import { forwardRef } from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  label?: string;
  error?: string;
}

export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, className, id, ...props }, ref) => {
    const inputId = id ?? label?.replace(/\s+/g, "-").toLowerCase();
    return (
      <div className={className}>
        {label ? (
          <label htmlFor={inputId} className="mb-1 block font-body text-[13px] font-medium text-ink-muted">
            {label}
          </label>
        ) : null}
        <input
          ref={ref}
          id={inputId}
          className={[
            "h-10 w-full rounded-md border bg-surface-1 px-3.5 py-2.5 font-body text-[15px] text-ink",
            "placeholder:text-ink-ghost",
            "transition-colors duration-150",
            error
              ? "border-negative focus:border-negative"
              : "border-hairline focus:border-accent",
          ].join(" ")}
          {...props}
        />
        {error ? <p className="mt-1 text-[13px] text-negative">{error}</p> : null}
      </div>
    );
  }
);

Input.displayName = "Input";
