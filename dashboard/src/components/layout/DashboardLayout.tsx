"use client";

import { useState } from "react";
import { TopNav } from "./TopNav";
import { Sidebar } from "./Sidebar";

interface DashboardLayoutProps {
  children: React.ReactNode;
}

export function DashboardLayout({ children }: DashboardLayoutProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  return (
    <div className="min-h-screen bg-canvas">
      <TopNav onMenuToggle={() => setSidebarOpen((v) => !v)} />
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} />
      <main className="pt-14 md:pl-60">
        <div className="mx-auto max-w-[1440px] p-6">
          {children}
        </div>
      </main>
    </div>
  );
}
