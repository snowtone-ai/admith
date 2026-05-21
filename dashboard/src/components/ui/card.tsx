export function Card({ title, children }: { title: string; children: React.ReactNode }) {
  return <section className="rounded-3xl border border-wheat/70 bg-white/75 p-5 shadow-sm"><h2 className="font-display text-xl">{title}</h2><div className="mt-3">{children}</div></section>;
}
