"use client";

import Link from "next/link";
import { Button } from "@/components/ui/button";

interface TopNavProps {
  onMenuToggle?: () => void;
}

export function TopNav({ onMenuToggle }: TopNavProps) {
  return (
    <header className="fixed inset-x-0 top-0 z-40 flex h-14 items-center border-b border-hairline bg-canvas px-4">
      {/* Hamburger (mobile) */}
      <Button variant="ghost" size="sm" className="mr-2 md:hidden" onClick={onMenuToggle} aria-label="メニュー">
        <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
          <path d="M4 6h16M4 12h16M4 18h16" />
        </svg>
      </Button>

      {/* Logo */}
      <Link href="/" className="flex items-baseline gap-0.5">
        <span className="font-display text-lg font-bold text-ink">Admith</span>
        <span className="font-display text-lg font-normal text-ink-muted">Flow</span>
      </Link>

      <div className="flex-1" />

      {/* Right side */}
      <div className="flex items-center gap-2">
        <Button variant="ghost" size="sm" aria-label="通知">
          <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M18 8A6 6 0 006 8c0 7-3 9-3 9h18s-3-2-3-9M13.73 21a2 2 0 01-3.46 0" />
          </svg>
        </Button>
        <div className="h-8 w-8 rounded-full bg-surface-3" />
      </div>
    </header>
  );
}
