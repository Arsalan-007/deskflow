import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "DeskFlow",
  description: "Agentic arXiv research tracker",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0 }}>{children}</body>
    </html>
  );
}
