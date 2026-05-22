import { ResourceDetailClient } from "./detail-client";

export default async function ResourceDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <ResourceDetailClient resourceId={id} />;
}
