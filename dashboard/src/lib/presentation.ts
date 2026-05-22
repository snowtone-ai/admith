const numberFormat = new Intl.NumberFormat("ja-JP");

const negotiationStateLabels: Record<string, string> = {
  cfp_open: "買い手・運送条件を確認中",
  negotiating: "条件を調整中",
  draft_agreement: "合意案を作成済み",
  pending_human_approval: "決裁者の承認待ち",
  signing: "承認済み・手続き中",
  settled: "取引完了",
  failed: "取引不成立",
  expired: "期限切れ"
};

const resourceStateLabels: Record<string, string> = {
  available: "受付可能",
  locked: "交渉中",
  settled: "取引完了"
};

const materialLabels: Record<string, string> = {
  okara: "おから",
  food_waste: "食品残さ"
};

const requiredUseLabels: Record<string, string> = {
  feed: "飼料化",
  fertilizer: "肥料化",
  upcycle: "アップサイクル"
};

const auditEventLabels: Record<string, string> = {
  "action.CreateCFP": "交渉を開始しました",
  "action.RequestApproval": "決裁者への承認依頼を作成しました",
  "action.ApproveAgreement": "決裁者が承認しました",
  "action.RejectAgreement": "決裁者が却下しました",
  "action.SignAgreement": "契約手続きを進めました",
  "action.SettleDeal": "取引を完了しました",
  "circuit_breaker.price_anomaly": "価格が通常範囲を外れたため停止しました"
};

export function formatYen(value: unknown): string {
  const number = Number(value);
  if (!Number.isFinite(number)) return "-";
  return `${numberFormat.format(number)}円`;
}

export function formatKg(value: unknown): string {
  const number = Number(value);
  if (!Number.isFinite(number)) return "-";
  return `${numberFormat.format(number)}kg`;
}

export function formatYenPerKg(value: unknown): string {
  const number = Number(value);
  if (!Number.isFinite(number)) return "-";
  return `${numberFormat.format(number)}円/kg`;
}

export function formatMaterial(value: unknown): string {
  if (typeof value !== "string" || !value) return "食品残さ";
  return materialLabels[value] ?? value;
}

export function formatRequiredUse(value: unknown): string {
  if (typeof value !== "string" || !value) return "-";
  return requiredUseLabels[value] ?? value;
}

export function negotiationStateLabel(state: string | undefined): string {
  if (!state) return "読み込み中";
  return negotiationStateLabels[state] ?? "状態を確認中";
}

export function resourceStateLabel(state: string | undefined): string {
  if (!state) return "読み込み中";
  return resourceStateLabels[state] ?? "確認中";
}

export function approvalDisabledReason(state: string | undefined): string | null {
  if (!state) return "取引条件を読み込んでいます。";
  if (state !== "pending_human_approval") return "この取引は現在、承認操作の対象ではありません。";
  return null;
}

export function approvalTermsRows(terms: Record<string, unknown> | undefined): Array<{ label: string; value: string; emphasis?: boolean }> {
  if (!terms) return [];
  return [
    { label: "取引数量", value: formatKg(terms.quantity_kg) },
    { label: "受け渡し単価", value: formatYenPerKg(terms.transfer_price_yen_per_kg), emphasis: true },
    { label: "運送費", value: formatYen(terms.logistics_fee_yen) },
    { label: "サービス利用料", value: formatYen(terms.platform_fee_yen) },
    { label: "排出事業者の改善額", value: formatYen(terms.seller_delta_yen), emphasis: true },
    { label: "受け入れ事業者の改善額", value: formatYen(terms.buyer_delta_yen), emphasis: true },
    { label: "合計改善額", value: formatYen(terms.total_delta_yen), emphasis: true }
  ];
}

export function auditEventTitle(eventType: string): string {
  return auditEventLabels[eventType] ?? "取引記録を保存しました";
}

export function auditEventSummary(data: Record<string, unknown>): string {
  if (typeof data.state === "string") return `現在の状態: ${negotiationStateLabel(data.state)}`;
  if (typeof data.reason === "string") return `理由: ${data.reason}`;
  if (typeof data.decision === "string") return `判断: ${data.decision === "approve" ? "承認" : "却下"}`;
  return "詳細は監査用データとして保存されています。";
}

export function friendlyError(message: string): string {
  if (message.includes("API key is not set")) return "運用キーが未設定です。管理者に確認してください。";
  if (message.includes("401")) return "ログイン情報を確認してください。";
  if (message.includes("503")) return "運用キーが未設定です。管理者に確認してください。";
  if (message.includes("Failed to fetch")) return "サーバーに接続できません。起動状況を確認してください。";
  return "処理に失敗しました。入力内容または接続状況を確認してください。";
}
