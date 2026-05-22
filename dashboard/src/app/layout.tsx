import "./globals.css";
import { DashboardLayout } from "@/components/layout/DashboardLayout";

export const metadata = {
  title: "Admith Flow",
  description: "食品残さの価値転換プラットフォーム",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ja">
      <body>
        <DashboardLayout>{children}</DashboardLayout>
      </body>
    </html>
  );
}
