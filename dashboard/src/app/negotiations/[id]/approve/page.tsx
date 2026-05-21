import { ApproveClient } from "./approve-client";

export default async function ApprovePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <ApproveClient negotiationId={id} />;
}
