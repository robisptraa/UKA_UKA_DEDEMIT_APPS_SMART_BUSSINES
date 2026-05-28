"use client";

import React, { useState } from "react";
import { 
  TrendingUp, 
  Sparkles, 
  AlertTriangle,
  ArrowRight,
  Clock,
  Zap,
  CheckCircle2,
  Calendar,
  Layers,
  Search,
  UserCheck
} from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  LineChart,
  Line,
  Legend,
  Cell
} from "recharts";
import { toast } from "react-hot-toast";

export default function AnalyticsPage() {
  const [reportMonth, setReportMonth] = useState("Mei 2026");

  // 1. Data Best Selling Products / Services (Bar Chart)
  const bestSellers = [
    { name: "Kopi Aren Latte", sales: 145, revenue: 3190000, color: "#10B981" },
    { name: "Kaos Streetwear", sales: 88, revenue: 16280000, color: "#F59E0B" },
    { name: "Cuci Kering Laundry", sales: 74, revenue: 3330000, color: "#2DD4BF" },
    { name: "Creambath Salon", sales: 52, revenue: 13000000, color: "#8B5CF6" },
    { name: "Servis Motor Matic", sales: 38, revenue: 3610000, color: "#38BDF8" },
  ];

  // 2. Data Pelanggan Baru vs Repeat Order (Line Chart)
  const customerTrends = [
    { name: "Minggu 1", "Baru": 24, "Lama": 45 },
    { name: "Minggu 2", "Baru": 38, "Lama": 62 },
    { name: "Minggu 3", "Baru": 29, "Lama": 78 },
    { name: "Minggu 4", "Baru": 42, "Lama": 95 },
  ];

  // 3. Data Prediksi Stok Habis (Tabel Risk)
  const stockPredictions = [
    { id: "ITEM-105", name: "Beras Premium Pandan Wangi 5kg", stock: 2, avgSalesWeekly: 4.5, daysRemaining: 3, alertStatus: "critical" },
    { id: "ITEM-107", name: "Biji Kopi House Blend Arabica 1kg", stock: 4, avgSalesWeekly: 2.8, daysRemaining: 10, alertStatus: "warning" },
    { id: "ITEM-102", name: "T-Shirt Oversized Noir Size L", stock: 1, avgSalesWeekly: 0.5, daysRemaining: 14, alertStatus: "warning" },
    { id: "ITEM-108", name: "Croissant Almond Premium", stock: 24, avgSalesWeekly: 14.0, daysRemaining: 12, alertStatus: "normal" },
  ];

  // 4. Heatmap Jam Tersibuk (7 Hari x 24 Jam)
  // Simplified for display: showing 7 days x 8 major time slots to keep layout compact and responsive
  const days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"];
  const timeSlots = ["08:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00", "22:00"];
  
  // Color intensity scale: values from 0 (quiet) to 10 (peak busy)
  const heatmapData: { [key: string]: number[] } = {
    "Senin":    [2, 3, 7, 4, 3, 6, 8, 4],
    "Selasa":   [1, 4, 8, 5, 2, 5, 7, 3],
    "Rabu":     [3, 3, 6, 4, 4, 7, 8, 5],
    "Kamis":    [2, 5, 9, 6, 3, 6, 8, 4],
    "Jumat":    [4, 6, 8, 7, 6, 9, 10, 7],
    "Sabtu":    [6, 8, 10, 8, 7, 10, 9, 8],
    "Minggu":   [5, 9, 9, 7, 8, 8, 7, 5],
  };

  const getHeatmapColor = (value: number) => {
    if (value >= 9) return "bg-brand font-bold text-white border-brand"; // Peak Busy
    if (value >= 7) return "bg-emerald-700/80 text-zinc-150 border-emerald-800"; // Busy
    if (value >= 4) return "bg-emerald-900/50 text-zinc-300 border-emerald-950"; // Moderate
    return "bg-zinc-950 text-zinc-650 border-zinc-900"; // Quiet
  };

  return (
    <div className="space-y-8 font-mono text-xs">
      
      {/* HEADER ANALYTICS */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2 font-sans">
            AI Analytics & Deep Reports <span className="animate-pulse">✨</span>
          </h2>
          <p className="text-[10px] text-zinc-500">Menganalisis performa produk terlaris harian, tren retensi pelanggan, heatmap kesibukan kasir, dan proyeksi stok.</p>
        </div>
      </header>

      {/* ================= SECTION 1: BEST SELLERS & RETENTION RETRIEVAL ================= */}
      <section className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        
        {/* Bar Chart: Produk Terlaris */}
        <div className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold text-brand-ghost tracking-widest uppercase block mb-1">TOP SELLERS</span>
            <h3 className="text-sm font-bold text-white mb-6 font-sans">Produk & Jasa Terlaris (Pcs Terjual)</h3>
          </div>
          
          <div className="w-full h-64 font-mono text-[9px]">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={bestSellers} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f1f23" vertical={false} />
                <XAxis dataKey="name" stroke="#52525b" tickLine={false} />
                <YAxis stroke="#52525b" tickLine={false} />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#18181b", borderColor: "#27272a", borderRadius: "12px", color: "#fff" }}
                  cursor={{ fill: "rgba(16, 185, 129, 0.05)" }}
                />
                <Bar dataKey="sales" fill="#10B981" radius={[4, 4, 0, 0]}>
                  {bestSellers.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Line Chart: Pelanggan Baru vs Repeat */}
        <div className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 flex flex-col justify-between">
          <div>
            <span className="text-[10px] font-bold text-brand tracking-widest uppercase block mb-1">CUSTOMER RETENTION</span>
            <h3 className="text-sm font-bold text-white mb-6 font-sans">Tren Pelanggan Baru vs Pembeli Berulang</h3>
          </div>

          <div className="w-full h-64 font-mono text-[9px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={customerTrends} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f1f23" vertical={false} />
                <XAxis dataKey="name" stroke="#52525b" tickLine={false} />
                <YAxis stroke="#52525b" tickLine={false} />
                <Tooltip contentStyle={{ backgroundColor: "#18181b", borderColor: "#27272a", borderRadius: "12px", color: "#fff" }} />
                <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: "10px" }} />
                <Line type="monotone" dataKey="Baru" name="Pelanggan Baru" stroke="#38BDF8" strokeWidth={3} dot={{ r: 3 }} />
                <Line type="monotone" dataKey="Lama" name="Repeat Order (Lama)" stroke="#F59E0B" strokeWidth={3} dot={{ r: 3 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </section>

      {/* ================= SECTION 2: HEATMAP JAM SIBUK 7x24 ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800">
        <div>
          <span className="text-[10px] font-bold text-teal-400 tracking-widest uppercase block mb-1">STORE TRAFFIC ANALYSIS</span>
          <h3 className="text-sm font-bold text-white mb-2 font-sans">Heatmap Jam Tersibuk Toko (Mingguan)</h3>
          <p className="text-xs text-zinc-500 mb-6 font-sans">Peta intensitas transaksi kasir dan chat Telegram bot. Membantu pengaturan jam kerja staf operasional toko.</p>
        </div>

        <div className="overflow-x-auto">
          <div className="min-w-[650px] border border-zinc-800 rounded-2xl p-4 bg-zinc-950/40">
            {/* Hour headers */}
            <div className="grid grid-cols-9 gap-1.5 mb-1.5 text-center text-zinc-500 font-bold uppercase">
              <div className="text-left pl-2">HARI</div>
              {timeSlots.map(t => (
                <div key={t} className="text-[10px]">{t}</div>
              ))}
            </div>

            {/* Grid Rows */}
            <div className="space-y-1.5">
              {days.map(day => (
                <div key={day} className="grid grid-cols-9 gap-1.5 items-center">
                  <div className="text-left font-bold text-zinc-400 pl-2">{day}</div>
                  {heatmapData[day].map((val, idx) => (
                    <div 
                      key={idx}
                      title={`${day} jam ${timeSlots[idx]} - Level Kesibukan: ${val}/10`}
                      className={`py-3 rounded-lg text-center border text-[9px] cursor-help transition-all hover:scale-105 hover:z-10 ${getHeatmapColor(val)}`}
                    >
                      {val}
                    </div>
                  ))}
                </div>
              ))}
            </div>

            {/* Legend scale */}
            <div className="mt-4 pt-3 border-t border-zinc-900 flex justify-end items-center gap-3 text-[9px] text-zinc-500">
              <span>SENGGANG</span>
              <span className="w-4 h-4 rounded bg-zinc-950 border border-zinc-900" />
              <span className="w-4 h-4 rounded bg-emerald-900/50 border border-emerald-950" />
              <span className="w-4 h-4 rounded bg-emerald-700/80 border border-emerald-800" />
              <span className="w-4 h-4 rounded bg-brand border border-brand" />
              <span>SIBUK (PEAK)</span>
            </div>
          </div>
        </div>
      </section>

      {/* ================= SECTION 3: STOCK RISK FORECAST TABLE ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800">
        <div>
          <span className="text-[10px] font-bold text-red-400 tracking-widest uppercase block mb-1">INVENTORY RISK FORECASTING</span>
          <h3 className="text-sm font-bold text-white mb-2 font-sans">Proyeksi & Estimasi Kehabisan Stok</h3>
          <p className="text-xs text-zinc-500 mb-6 font-sans">AI membandingkan kecepatan penjualan harian dengan sisa stok aktif untuk memberikan peringatan aman kulakan.</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase tracking-wider">
                <th className="py-4">ID</th>
                <th className="py-4">NAMA PRODUK</th>
                <th className="py-4 text-right">SISA STOK</th>
                <th className="py-4 text-right">RATA-RATA HARIAN</th>
                <th className="py-4 text-right">PREDIKSI HARI HABIS</th>
                <th className="py-4 pl-8">STATUS RISIKO</th>
              </tr>
            </thead>
            <tbody>
              {stockPredictions.map((pred) => (
                <tr key={pred.id} className="border-b border-zinc-800/50 hover:bg-zinc-950/40 transition-colors">
                  <td className="py-4 text-zinc-500 font-bold">{pred.id}</td>
                  <td className="py-4 text-white font-bold max-w-[200px] truncate">{pred.name}</td>
                  <td className="py-4 text-right text-zinc-300 font-bold pr-2">{pred.stock} Unit</td>
                  <td className="py-4 text-right text-zinc-400 pr-4">{pred.avgSalesWeekly} Pcs</td>
                  <td className={`py-4 text-right font-extrabold pr-4 ${pred.alertStatus === "critical" ? "text-red-450 text-sm font-black" : "text-white"}`}>
                    {pred.daysRemaining} Hari Lagi
                  </td>
                  <td className="py-4 pl-8">
                    <span className={`px-2.5 py-0.5 rounded text-[8px] font-extrabold uppercase ${
                      pred.alertStatus === "critical" 
                        ? "bg-red-500/10 text-red-400 border border-red-500/20 animate-pulse font-bold" 
                        : pred.alertStatus === "warning"
                        ? "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20"
                        : "bg-zinc-800 text-zinc-450"
                    }`}>
                      {pred.alertStatus === "critical" ? "BAHAYA KRITIS 🚨" : pred.alertStatus === "warning" ? "Peringatan Waspada" : "Aman Sedia"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ================= SECTION 4: AI BUSINESS NARRATIVE REPORT ================= */}
      <section className="p-8 rounded-3xl bg-zinc-900 border border-brand/20 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5">
          <Sparkles className="w-36 h-36 text-brand" />
        </div>

        <div className="flex items-center gap-2 mb-6">
          <div className="bg-brand/10 p-2 rounded-xl text-brand border border-brand/20">
            <Sparkles className="w-5 h-5 animate-pulse" />
          </div>
          <span className="text-[10px] font-extrabold tracking-widest text-brand uppercase font-sans">Monthly AI Strategic Business Report</span>
        </div>

        <h3 className="text-xl font-extrabold text-white mb-2 font-sans">Laporan Eksekutif Narasi Gemini AI</h3>
        <p className="text-xs text-zinc-500 mb-8 max-w-2xl font-sans">
          Analisis intelijen AI terhadap total laba kotor, frekuensi checkout order bot Telegram, retensi pelanggan, dan efektivitas jam sibuk bulan berjalan.
        </p>

        <div className="p-6 bg-zinc-950/80 border border-zinc-800 rounded-2xl space-y-5 font-sans leading-relaxed text-zinc-300">
          <div className="space-y-2">
            <h4 className="text-white font-bold text-xs font-mono">1. RINGKASAN PERTUMBUHAN KELAS BISNIS 📈</h4>
            <p className="text-xs">
              Pada bulan berjalan ({reportMonth}), bisnis Anda mencatat **Pemasukan Rp 32.450.000** dengan profitabilitas rata-rata **Laba Bersih ~85%**. Kontribusi transaksi terbesar berasal dari **kategori Fashion (Kaos Streetwear)** senilai Rp 16.280.000 disusul **kategori Kuliner (Kopi Aren Latte)**. Chatbot Telegram melayani 72% dari total checkout pelanggan, membuktikan otomatisasi bot sangat disukai.
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="text-white font-bold text-xs font-mono">2. REKOMENDASI PEAK-HOURS & MANPOWER ALLOCATION ⏰</h4>
            <p className="text-xs">
              Heatmap menunjukkan transaksi mengalami **Peak tertinggi pada hari Jumat-Sabtu pukul 12:00-14:00 (jam makan siang)** dan **18:00-20:00 (malam hari)** dengan level kesibukan mencapai 10/10. Rekomendasi AI: alokasikan minimal 2 staf kasir aktif di rentang waktu tersebut untuk meminimalkan antrean kasir digital.
            </p>
          </div>

          <div className="space-y-2">
            <h4 className="text-white font-bold text-xs font-mono">3. TINDAKAN PENCEGAHAN RESIKO INVENTORI 🚨</h4>
            <p className="text-xs">
              AI mendeteksi item **Beras Premium Pandan Wangi** dalam status bahaya kritis (sisa 2 kantong, diprediksi habis dalam 3 hari). Segera hubungi distributor penyuplai utama untuk restock malam ini demi menghindari kekosongan menu utama warung Anda.
            </p>
          </div>
        </div>
      </section>

    </div>
  );
}
