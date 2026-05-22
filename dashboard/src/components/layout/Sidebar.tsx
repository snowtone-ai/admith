"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

interface SidebarProps {
  open?: boolean;
  onClose?: () => void;
}

const navItems = [
  { href: "/", label: "概要", icon: "M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-4 0a1 1 0 01-1-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 01-1 1" },
  { href: "/negotiations", label: "取引", icon: "M8 7h12m0 0l-4-4m4 4l-4 4m0 5H4m0 0l4 4m-4-4l4-4" },
  { href: "/resources", label: "食品残さ", icon: "M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" },
  { href: "/audit", label: "監査記録", icon: "M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" },
];

export function Sidebar({ open, onClose }: SidebarProps) {
  const pathname = usePathname();

  const sidebar = (
    <nav className="flex h-full w-60 flex-col gap-1 border-r border-hairline bg-surface-1 p-3 pt-16">
      {navItems.map((item) => {
        const active = pathname === item.href || (item.href !== "/" && pathname.startsWith(item.href));
        return (
          <Link
            key={item.href}
            href={item.href}
            onClick={onClose}
            className={[
              "flex items-center gap-3 rounded-md px-3 py-2 text-[13px] font-medium",
              "transition-colors duration-150",
              active
                ? "border-l-2 border-l-accent bg-surface-2 text-ink"
                : "text-ink-muted hover:bg-surface-2 hover:text-ink",
            ].join(" ")}
          >
            <svg className="h-4 w-4 shrink-0" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <path d={item.icon} />
            </svg>
            {item.label}
          </Link>
        );
      })}
    </nav>
  );

  return (
    <>
      {/* Desktop sidebar */}
      <aside className="hidden md:block fixed left-0 top-0 h-full z-30">
        {sidebar}
      </aside>

      {/* Mobile drawer */}
      {open ? (
        <div className="fixed inset-0 z-50 md:hidden">
          <div
            className="absolute inset-0 bg-[var(--color-overlay)] backdrop-blur-sm"
            onClick={onClose}
          />
          <aside className="relative h-full w-full max-w-[300px]">
            {sidebar}
          </aside>
        </div>
      ) : null}
    </>
  );
}
