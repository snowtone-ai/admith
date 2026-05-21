import { NegotiationDetailClient } from "./detail-client";

export default async function NegotiationDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <NegotiationDetailClient negotiationId={id} />;
}
