"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { apiFetch } from "@/lib/api";

type Metrics = {
  active_negotiations: number;
  pending_approvals: number;
  today_delta_yen: number;
};

export default function Page() {
  const [metrics, setMetrics] = useState<Metrics | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    apiFetch<Metrics>("/dashboard/metrics").then(setMetrics).catch((reason) => setError(String(reason)));
  }, []);

  return (
    <main className="grid gap-5 md:grid-cols-3">
      <Card title="アクティブ交渉数"><p className="text-4xl font-bold">{metrics?.active_negotiations ?? "-"}</p></Card>
      <Card title="承認待ち"><span className="rounded-full bg-red-100 px-3 py-1 text-red-700">{metrics?.pending_approvals ?? "-"}</span></Card>
      <Card title="本日Delta"><p className="text-4xl font-bold">JPY {metrics?.today_delta_yen ?? "-"}</p></Card>
      <section className="rounded-3xl bg-soil p-6 text-paper md:col-span-3">
        <h1 className="font-display text-4xl">Admith Operator Dashboard</h1>
        <p className="mt-3">食品廃棄物のB2B交渉、Human Approval、Settlementを監視します。</p>
        {error ? <p className="mt-3 text-wheat">API取得エラー: {error}</p> : null}
      </section>
    </main>
  );
}
