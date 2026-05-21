export default async function NegotiationDetail({ params }: { params: Promise<{ id: string }> }) {
  const { id } = await params;
  return <main><h1 className="font-display text-4xl">交渉詳細</h1><p>Timeline, Agreement, Approval: {id}</p></main>;
}
