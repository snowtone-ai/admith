import "./globals.css";
import Link from "next/link";

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <div className="mx-auto max-w-6xl px-5 py-6">
          <nav className="mb-8 flex gap-4 font-semibold text-leaf">
            <Link href="/">概要</Link>
            <Link href="/negotiations">取引</Link>
            <Link href="/resources">食品残さ</Link>
            <Link href="/audit">監査記録</Link>
          </nav>
          {children}
        </div>
      </body>
    </html>
  );
}
