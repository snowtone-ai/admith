"use client";

import { useEffect, useState } from "react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Input } from "@/components/ui/Input";
import { Badge } from "@/components/ui/Badge";
import { apiFetch } from "@/lib/api";
import { formatKg, formatMaterial, formatRequiredUse, formatYen, friendlyError, resourceStateLabel } from "@/lib/presentation";

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
    <div className="space-y-6">
      <h1 className="font-display text-[32px] font-semibold tracking-tight" style={{ letterSpacing: "-0.8px" }}>
        食品残さ管理
      </h1>

      <Card title="新しい食品残さを登録">
        <div className="grid gap-4 md:grid-cols-4">
          <Input
            label="食品残さの種類"
            value={material}
            onChange={(e) => setMaterial(e.target.value)}
          />
          <Input
            label="数量 (kg)"
            type="number"
            value={quantity}
            onChange={(e) => setQuantity(Number(e.target.value))}
          />
          <Input
            label="現在の廃棄費 (円)"
            type="number"
            value={disposalCost}
            onChange={(e) => setDisposalCost(Number(e.target.value))}
          />
          <div className="flex items-end">
            <Button onClick={createResource} className="w-full">登録</Button>
          </div>
        </div>
      </Card>

      <Card title="登録済みの食品残さ">
        <div className="space-y-3">
          {resources.map((resource) => (
            <div
              key={resource.resource_id}
              className="grid gap-4 rounded-lg border border-hairline bg-canvas p-4 hoverable hover:bg-surface-1 md:grid-cols-[1fr_auto]"
            >
              <div>
                <p className="font-display text-[16px] font-semibold tracking-tight">
                  {formatMaterial(resource.attributes.material ?? resource.resource_type)}
                </p>
                <div className="mt-2 flex flex-wrap items-center gap-2 text-[13px] text-ink-muted">
                  <Badge variant={resource.state === "available" ? "positive" : resource.state === "settled" ? "info" : "warning"}>
                    {resourceStateLabel(resource.state)}
                  </Badge>
                  <span>数量: <span className="font-mono tabular-nums">{formatKg(resource.attributes.quantity_kg)}</span></span>
                  <span>廃棄費: <span className="font-mono tabular-nums text-negative">{formatYen(resource.attributes.disposal_cost_yen)}</span></span>
                  <span>用途: {formatRequiredUse(resource.attributes.required_use)}</span>
                </div>
              </div>
              <div className="flex items-center">
                <Button
                  onClick={() => startNegotiation(resource.resource_id)}
                  disabled={resource.state !== "available"}
                  size="sm"
                >
                  交渉開始
                </Button>
              </div>
            </div>
          ))}
          {resources.length === 0 ? (
            <p className="text-[13px] text-ink-muted">食品残さはまだ登録されていません。</p>
          ) : null}
        </div>
      </Card>

      {message ? <p className="text-[13px] text-negative">{friendlyError(message)}</p> : null}
    </div>
  );
}
