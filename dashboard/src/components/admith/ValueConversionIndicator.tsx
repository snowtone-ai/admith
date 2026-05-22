"use client";

import { useEffect, useRef, useState } from "react";

interface ValueConversionProps {
  from: number;
  to: number;
  converting?: boolean;
  size?: "sm" | "lg";
}

const fmt = new Intl.NumberFormat("ja-JP");

function useCountUp(target: number, duration: number, active: boolean): number {
  const [current, setCurrent] = useState(target);
  const startRef = useRef<number | null>(null);
  const fromRef = useRef(target);

  useEffect(() => {
    if (!active) {
      setCurrent(target);
      return;
    }
    fromRef.current = current;
    startRef.current = null;
    let raf: number;
    function tick(ts: number) {
      if (startRef.current === null) startRef.current = ts;
      const elapsed = ts - startRef.current;
      const progress = Math.min(elapsed / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);
      setCurrent(Math.round(fromRef.current + (target - fromRef.current) * eased));
      if (progress < 1) raf = requestAnimationFrame(tick);
    }
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [target, active, duration]);

  return current;
}

export function ValueConversionIndicator({ from, to, converting = false, size = "sm" }: ValueConversionProps) {
  const [done, setDone] = useState(false);
  const displayValue = useCountUp(converting ? to : from, 1000, converting);

  useEffect(() => {
    if (!converting) { setDone(false); return; }
    const timer = setTimeout(() => setDone(true), 800);
    return () => clearTimeout(timer);
  }, [converting]);

  const sizeClass = size === "lg"
    ? "font-mono text-[28px] font-semibold"
    : "font-mono text-[16px] font-medium";

  const prefix = displayValue >= 0 ? "+" : "\u2212";

  return (
    <span
      className={[
        sizeClass,
        converting && !done ? "value-converting" : "",
        done ? "text-positive glow-positive" : !converting ? "text-negative" : "",
      ].join(" ")}
      style={{ fontFeatureSettings: "'tnum', 'lnum'" }}
    >
      {prefix}{fmt.format(Math.abs(displayValue))}
    </span>
  );
}
