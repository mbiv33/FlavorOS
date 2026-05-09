import type { Metadata } from "next";
import "@/styles/globals.css";
import { Header } from "@/components/shell/Header";
import { LeftNav } from "@/components/shell/LeftNav";
import { RightRail } from "@/components/shell/RightRail";

export const metadata: Metadata = {
  title: "FlavorOS",
  description: "Calm by default. Voice-first.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://rsms.me/" />
        <link rel="stylesheet" href="https://rsms.me/inter/inter.css" />
      </head>
      <body>
        <Header />
        <div
          className="grid gap-5 mx-auto max-w-[1620px] px-7 pt-5 pb-[60px]"
          style={{ gridTemplateColumns: "260px minmax(0,1fr) 380px" }}
        >
          <LeftNav />
          <main className="min-w-0">{children}</main>
          <RightRail />
        </div>
      </body>
    </html>
  );
}
