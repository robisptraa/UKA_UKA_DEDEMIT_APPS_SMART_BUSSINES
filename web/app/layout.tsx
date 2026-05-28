import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Dedemit UMKM — AI Business OS untuk Semua UMKM Indonesia",
  description: "Platform manajemen bisnis berbasis AI untuk semua jenis UMKM Indonesia. Dari warung makan, toko fashion, salon kecantikan, laundry, hingga bengkel — kelola inventori, terima pembayaran QRIS otomatis, dan pantau omset dalam satu dashboard.",
  keywords: ["umkm", "bisnis indonesia", "manajemen toko", "ai business os", "midtrans payment", "qris", "telegram bot", "dedemit umkm", "warung makan", "toko fashion", "salon", "laundry"],
  authors: [{ name: "Dedemit UMKM Team" }],
  openGraph: {
    title: "Dedemit UMKM — AI Business OS untuk Semua UMKM Indonesia",
    description: "Platform AI terlengkap untuk semua jenis UMKM Indonesia: scan produk otomatis, terima pembayaran QRIS via Telegram Bot, dan analitik bisnis real-time.",
    type: "website",
    locale: "id_ID",
  }
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <head>
        <link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>👻</text></svg>" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet" />
      </head>
      <body className="antialiased min-h-screen bg-dark-950 text-dark-50 bg-streetwear-glow bg-no-repeat bg-cover font-sans">
        {children}
      </body>
    </html>
  );
}
