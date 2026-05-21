"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { apiFetch } from "@/lib/api";

type Resource = {
  resource_id: string;
  resource_type: string;
  state: string;
  attributes: {
    material?: string;
    quantity_kg?: number;
    disposal_cost_yen?: number;
    required_use?: string;
  };
};

export default function ResourcesPage() {
  const [resources, setResources] = useState<Resource[]>([]);
  const [material, setMaterial] = useState("okara");
  const [quantity, setQuantity] = useState(1000);
  const [disposalCost, setDisposalCost] = useState(25000);
  const [message, setMessage] = useState<string | null>(null);

  async function load() {
    setResources(await apiFetch<Resource[]>("/resources"));
  }

  useEffect(() => {
    load().catch((error) => setMessage(String(error)));
  }, []);

  async function createResource() {
    setMessage(null);
    await apiFetch<Resource>("/resources", {
      method: "POST",
      body: JSON.stringify({ material, quantity_kg: quantity, disposal_cost_yen: disposalCost, required_use: "feed" })
    });
    await load();
  }

  async function startNegotiation(resourceId: string) {
    const negotiation = await apiFetch<{ negotiation_id: string }>(
      "/negotiations",
      { method: "POST", body: JSON.stringify({ resource_id: resourceId, buyer_max_price_yen_per_kg: 18 }) }
    );
    location.href = `/negotiations/${negotiation.negotiation_id}/approve`;
  }

  return (
    <main className="space-y-5">
      <h1 className="font-display text-4xl">リソース管理</h1>
      <Card title="新規リソース">
        <div className="grid gap-3 md:grid-cols-4">
          <input className="rounded-xl border p-3" value={material} onChange={(event) => setMaterial(event.target.value)} aria-label="material" />
          <input className="rounded-xl border p-3" type="number" value={quantity} onChange={(event) => setQuantity(Number(event.target.value))} aria-label="quantity kg" />
          <input className="rounded-xl border p-3" type="number" value={disposalCost} onChange={(event) => setDisposalCost(Number(event.target.value))} aria-label="disposal cost yen" />
          <Button onClick={createResource}>登録</Button>
        </div>
      </Card>
      <Card title="登録済みリソース">
        <div className="space-y-3">
          {resources.map((resource) => (
            <div key={resource.resource_id} className="grid gap-3 rounded-2xl border bg-white p-4 md:grid-cols-[1fr_auto]">
              <div>
                <p className="font-semibold">{resource.attributes.material ?? resource.resource_type}</p>
                <p className="text-sm">状態: {resource.state} / 数量: {resource.attributes.quantity_kg}kg / 廃棄費: JPY {resource.attributes.disposal_cost_yen}</p>
              </div>
              <Button onClick={() => startNegotiation(resource.resource_id)} disabled={resource.state !== "available"}>交渉開始</Button>
            </div>
          ))}
          {resources.length === 0 ? <p>リソースはまだありません。</p> : null}
        </div>
      </Card>
      {message ? <p className="text-red-700">{message}</p> : null}
    </main>
  );
}
