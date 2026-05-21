export function Button(props: React.ButtonHTMLAttributes<HTMLButtonElement>) {
  return <button {...props} className={`rounded-full bg-leaf px-4 py-2 font-semibold text-white ${props.className ?? ""}`} />;
}
