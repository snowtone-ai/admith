import { forwardRef } from "react";

interface SelectProps extends React.SelectHTMLAttributes<HTMLSelectElement> {
  label?: string;
  error?: string;
}

export const Select = forwardRef<HTMLSelectElement, SelectProps>(
  ({ label, error, className, id, children, ...props }, ref) => {
    const selectId = id ?? label?.replace(/\s+/g, "-").toLowerCase();
    return (
      <div className={className}>
        {label ? (
          <label htmlFor={selectId} className="mb-1 block font-body text-[13px] font-medium text-ink-muted">
            {label}
          </label>
        ) : null}
        <select
          ref={ref}
          id={selectId}
          className={[
            "h-10 w-full rounded-md border bg-surface-1 px-3.5 py-2.5 font-body text-[15px] text-ink",
            "transition-colors duration-150",
            error
              ? "border-negative focus:border-negative"
              : "border-hairline focus:border-accent",
          ].join(" ")}
          {...props}
        >
          {children}
        </select>
        {error ? <p className="mt-1 text-[13px] text-negative">{error}</p> : null}
      </div>
    );
  }
);

Select.displayName = "Select";
