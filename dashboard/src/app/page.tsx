"use client";

import { useEffect, useState } from "react";
import { Card } from "@/components/ui/card";
import { apiFetch } from "@/lib/api";
import { formatYen, friendlyError } from "@/lib/presentation";

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
      <Card title="進行中の取引"><p className="text-4xl font-bold">{metrics?.active_negotiations ?? "-"}</p></Card>
      <Card title="決裁待ち"><span className="rounded-full bg-red-100 px-3 py-1 text-red-700">{metrics?.pending_approvals ?? "-"}</span></Card>
      <Card title="本日の改善額"><p className="text-4xl font-bold">{metrics ? formatYen(metrics.today_delta_yen) : "-"}</p></Card>
      <section className="rounded-3xl bg-soil p-6 text-paper md:col-span-3">
        <h1 className="font-display text-4xl">Admith Flow</h1>
        <p className="mt-3">食品残さの引き取り条件、決裁待ち、取引完了までの流れを確認します。</p>
        {error ? <p className="mt-3 text-wheat">{friendlyError(error)}</p> : null}
      </section>
    </main>
  );
}
