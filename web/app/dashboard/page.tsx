"use client";

import React, { useState } from "react";
import { 
  Sparkles, 
  TrendingUp, 
  Package, 
  ShoppingBag, 
  AlertTriangle,
  ArrowRight,
  Store,
  Wallet,
  Users,
  Clock,
  CheckCircle2,
  RefreshCw
} from "lucide-react";
import Link from "next/link";
import { 
  LineChart, 
  Line, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from "recharts";
import { toast } from "react-hot-toast";

export default function DashboardHome() {
  const [aiInsight, setAiInsight] = useState({
    title: "Minuman Dingin & Kopi Aren Melonjak 60% Siang Ini! ☕🍈",
    content: "Berdasarkan analitik transaksi pelanggan via Bot Telegram dan kasir, menu Kopi Aren Dingin mengalami peningkatan pesanan di jam 11:30 - 13:30. Pastikan stok es batu dan cup plastik 16oz aman sebelum jam makan siang dimulai!",
    time: "Diperbarui hari ini pukul 07:00 WIB"
  });
  
  const [isRefreshingInsight, setIsRefreshingInsight] = useState(false);

  // Mock data Recharts LineChart — Omset & Jumlah Order 7 hari terakhir (universal UMKM)
  const salesData = [
    { name: "Senin", omset: 1200000, orders: 12 },
    { name: "Selasa", omset: 1850000, orders: 19 },
    { name: "Rabu", omset: 1540000, orders: 15 },
    { name: "Kamis", omset: 2300000, orders: 24 },
    { name: "Jumat", omset: 2850000, orders: 30 },
    { name: "Sabtu", omset: 3600000, orders: 38 },
    { name: "Minggu", omset: 4100000, orders: 45 },
  ];

  // Summary Cards — 4 metrik sesuai spesifikasi
  const stats = [
    { name: "Order Hari Ini", value: "24 Order", change: "Rata-rata 99% sukses", icon: ShoppingBag, color: "text-brand", desc: "Dari Telegram & Kasir" },
    { name: "Pemasukan Hari Ini", value: "Rp 3,250,000", change: "+18% dari kemarin", icon: Wallet, color: "text-brand-ghost", desc: "E-Wallet & QRIS dominan" },
    { name: "Stok Menipis", value: "5 Item", change: "Perlu restock segera ⚠️", icon: AlertTriangle, color: "text-red-400", desc: "Klik untuk restock" },
    { name: "Pelanggan Baru", value: "12 Pelanggan", change: "+4 loyal member baru", icon: Users, color: "text-teal-400", desc: "Terdaftar minggu ini" },
  ];

  // Mock 5 order terbaru — campuran berbagai jenis UMKM
  const recentOrders = [
    { id: "ORD-901", buyer: "Sari Rahayu", item: "Kopi Aren Melted Latte x2", price: 44000, status: "paid", date: "3 menit lalu", type: "☕" },
    { id: "ORD-900", buyer: "Dian Kusuma", item: "T-Shirt Oversized Streetwear Noir", price: 185000, status: "paid", date: "22 menit lalu", type: "👕" },
    { id: "ORD-899", buyer: "Nurul Fadilah", item: "Hair Treatment + Creambath", price: 250000, status: "pending", date: "1 jam lalu", type: "💇‍♀️" },
    { id: "ORD-898", buyer: "Budi Santoso", item: "Layanan Cuci Kering Kilat 5kg", price: 45000, status: "paid", date: "2 jam lalu", type: "🧺" },
    { id: "ORD-897", buyer: "Ahmad Fauzi", item: "Oli Mesin Matic + Servis Ringan", price: 125000, status: "expired", date: "5 jam lalu", type: "🔧" },
  ];

  // Stok kritis — berbagai produk UMKM
  const criticalStock = [
    { name: "Biji Kopi House Blend 1kg", stock: 2, category: "Bahan Baku", color: "text-red-400" },
    { name: "Baju Kaos Streetwear Size L", stock: 1, category: "Fashion", color: "text-red-400" },
    { name: "Shampoo Salon Herbal 1L", stock: 2, category: "Kecantikan", color: "text-red-400" },
    { name: "Detergen Pewangi Laundry 5L", stock: 3, category: "Laundry", color: "text-yellow-500" },
    { name: "Cup Plastik 16oz (Pack)", stock: 3, category: "Kemasan", color: "text-yellow-500" },
  ];

  const formatRupiah = (val: number) => {
    if (val >= 1000000) return `${(val / 1000000).toFixed(1)}Jt`;
    if (val >= 1000) return `${(val / 1000).toFixed(0)}Rb`;
    return `${val}`;
  };

  const handleRefreshInsight = () => {
    setIsRefreshingInsight(true);
    toast.loading("Gemini AI sedang membaca arus kas harian...", { id: "refresh" });
    
    setTimeout(() => {
      const insights = [
        {
          title: "Promosi Bundling Naikkan Basket Size 35%! 🥐☕",
          content: "Analisis transaksi menunjukkan 42% pelanggan yang membeli Kopi juga ingin membeli Croissant jika ditawarkan sebagai paket bundling diskon 10%. Coba buat Menu Paket Sore di Bot Telegram!",
          time: "Diperbarui baru saja oleh Gemini 1.5 Flash"
        },
        {
          title: "Loyalty Program untuk Pelanggan Tidak Aktif! 😴👥",
          content: "Terdapat 18 pelanggan setia yang belum melakukan order ulang dalam 30 hari terakhir. Gunakan bot Telegram untuk mengirimkan kode kupon khusus diskon 15% sore ini!",
          time: "Diperbarui baru saja oleh Gemini 1.5 Flash"
        }
      ];
      
      const newInsight = insights[Math.floor(Math.random() * insights.length)];
      setAiInsight(newInsight);
      setIsRefreshingInsight(false);
      toast.dismiss("refresh");
      toast.success("Rekomendasi AI diperbarui! ✨", {
        style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
      });
    }, 1200);
  };

  return (
    <div className="space-y-8">
      {/* ALERT BANNER JIKA ADA STOK KRITIS */}
      {criticalStock.some(i => i.stock <= 2) && (
        <div className="p-4 bg-red-500/10 border border-red-500/30 rounded-2xl flex items-center justify-between text-xs font-mono">
          <div className="flex items-center gap-3 text-red-400">
            <AlertTriangle className="w-5 h-5 animate-pulse" />
            <div>
              <span className="font-bold uppercase block text-[10px]">Peringatan Stok Rendah! ⚠️</span>
              <span>Ada {criticalStock.filter(i => i.stock <= 2).length} item kritis dengan sisa stok &le; 2. Segera isi ulang untuk mencegah kehilangan pelanggan.</span>
            </div>
          </div>
          <Link href="/dashboard/inventory" className="bg-red-500 text-white font-bold px-3 py-1.5 rounded-lg hover:bg-red-600 transition-all">
            Restock Sekarang
          </Link>
        </div>
      )}

      {/* HEADER OVERVIEW */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
            Selamat Pagi, Bos Dedemit! 👋
          </h2>
          <p className="text-xs text-zinc-500">Toko <strong className="text-brand">Dedemit Coffee & Goods</strong> hari ini:</p>
        </div>
        <Link 
          href="/dashboard/inventory"
          className="flex items-center gap-2 px-4 py-2.5 bg-brand text-white rounded-xl text-xs font-bold hover:bg-brand-dark transition-all shadow-lg hover:shadow-brand/20"
        >
          <Package className="w-4 h-4" />
          + Tambah Item Baru
        </Link>
      </header>

      {/* ================= SUMMARY CARDS ================= */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <div key={i} className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 flex justify-between items-start group hover:border-zinc-700 transition-all duration-300">
              <div className="space-y-1">
                <span className="text-xs font-semibold text-zinc-400 block uppercase tracking-wider">{stat.name}</span>
                <h3 className="text-2xl font-extrabold text-white">{stat.value}</h3>
                <div className="flex flex-col font-mono text-[9px] text-zinc-500">
                  <span className="text-brand-ghost font-bold">{stat.change}</span>
                  <span>{stat.desc}</span>
                </div>
              </div>
              <div className={`p-3 rounded-xl bg-zinc-950 border border-zinc-800 ${stat.color} group-hover:scale-110 transition-transform`}>
                <Icon className="w-5 h-5" />
              </div>
            </div>
          );
        })}
      </section>

      {/* ================= RECHARTS LINECHART + STOK KRITIS ================= */}
      <section className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Recharts Line Chart */}
        <div className="lg:col-span-2 p-6 rounded-3xl bg-zinc-900 border border-zinc-800 flex flex-col justify-between">
          <div className="flex justify-between items-start mb-6">
            <div>
              <span className="text-[10px] font-bold text-brand-ghost tracking-widest uppercase block mb-1 font-mono">Real-time Analytics</span>
              <h3 className="text-lg font-bold text-white">Tren Omset & Transaksi (7 Hari Terakhir)</h3>
            </div>
            <div className="flex gap-4 text-[10px] font-mono">
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-brand" /> Omset</span>
              <span className="flex items-center gap-1.5"><span className="w-2.5 h-2.5 rounded-full bg-brand-ghost" /> Transaksi</span>
            </div>
          </div>
          
          <div className="w-full h-64 font-mono text-[10px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={salesData} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1f1f23" vertical={false} />
                <XAxis dataKey="name" stroke="#52525b" tickLine={false} tick={{ fontSize: 10 }} />
                <YAxis 
                  yAxisId="left"
                  stroke="#52525b" 
                  tickLine={false} 
                  tickFormatter={formatRupiah}
                  tick={{ fontSize: 10 }}
                  width={40}
                />
                <YAxis 
                  yAxisId="right"
                  orientation="right"
                  stroke="#52525b" 
                  tickLine={false} 
                  tick={{ fontSize: 10 }}
                  width={20}
                />
                <Tooltip 
                  contentStyle={{ backgroundColor: "#18181b", borderColor: "#27272a", borderRadius: "12px", color: "#fff", fontSize: "11px" }}
                  itemStyle={{ color: "#34D399" }}
                  formatter={(value: any, name: any) => {
                    if (name === "omset") return [`Rp ${Number(value).toLocaleString("id-ID")}`, "Omset"];
                    return [`${value} Transaksi`, "Order Count"];
                  }}
                />
                <Line 
                  yAxisId="left"
                  type="monotone" 
                  dataKey="omset" 
                  name="omset"
                  stroke="#10B981" 
                  strokeWidth={3} 
                  dot={{ r: 4, strokeWidth: 2, fill: "#18181b", stroke: "#10B981" }} 
                  activeDot={{ r: 6, fill: "#F59E0B" }} 
                />
                <Line 
                  yAxisId="right"
                  type="monotone" 
                  dataKey="orders" 
                  name="orders"
                  stroke="#F59E0B" 
                  strokeWidth={2} 
                  dot={{ r: 3, strokeWidth: 1.5, fill: "#18181b", stroke: "#F59E0B" }} 
                  activeDot={{ r: 5, fill: "#10B981" }} 
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* ALERT STOK KRITIS */}
        <div className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 flex flex-col justify-between gap-4">
          <div>
            <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-red-400" /> Stok Hampir Habis
            </h3>
            <p className="text-[10px] text-zinc-500 mb-4 font-mono">AI mendeteksi 3 bahan baku kritis yang harus diorder ulang.</p>

            <div className="space-y-3 font-mono">
              {criticalStock.slice(0, 4).map((item, index) => (
                <div key={index} className="p-3 rounded-xl bg-zinc-950 border border-zinc-800 flex items-center justify-between">
                  <div className="space-y-0.5">
                    <h4 className="text-[11px] font-bold text-white">{item.name}</h4>
                    <span className="text-[9px] text-zinc-500">{item.category}</span>
                  </div>
                  <span className={`px-2 py-0.5 rounded text-[9px] font-extrabold uppercase ${
                    item.stock <= 2 ? "bg-red-500/10 text-red-400 border border-red-500/20 animate-pulse" : "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20"
                  }`}>
                    {item.stock} sisa
                  </span>
                </div>
              ))}
            </div>
          </div>

          <Link href="/dashboard/inventory" className="w-full bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 text-white text-center py-2.5 rounded-xl text-[10px] font-bold transition-all flex items-center justify-center gap-1.5 font-mono">
            Kelola Inventori <ArrowRight className="w-4 h-4" />
          </Link>
        </div>
      </section>

      {/* ================= GEMINI AI INSIGHTS CARD ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-brand/20 relative overflow-hidden">
        <div className="absolute top-0 right-0 p-8 opacity-5">
          <Sparkles className="w-36 h-36 text-brand" />
        </div>

        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <div className="bg-brand/10 p-2 rounded-xl text-brand border border-brand/20">
              <Sparkles className="w-4 h-4 animate-pulse" />
            </div>
            <span className="text-[10px] font-extrabold tracking-widest text-brand uppercase font-mono">Gemini AI OS Insight</span>
          </div>

          <button 
            onClick={handleRefreshInsight}
            disabled={isRefreshingInsight}
            className="flex items-center gap-1.5 text-[9px] font-mono text-zinc-400 hover:text-white transition-colors bg-zinc-950 px-2.5 py-1.5 rounded-lg border border-zinc-800"
          >
            <RefreshCw className={`w-3 h-3 ${isRefreshingInsight ? "animate-spin" : ""}`} /> Refresh
          </button>
        </div>

        <h3 className="text-base font-extrabold text-white mb-1.5">{aiInsight.title}</h3>
        <p className="text-xs text-zinc-300 leading-relaxed mb-3 max-w-4xl">{aiInsight.content}</p>
        <span className="text-[8px] text-zinc-500 font-mono block">{aiInsight.time}</span>
      </section>

      {/* ================= 5 ORDER TERBARU ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-bold text-white">Transaksi Terbaru</h3>
            <p className="text-xs text-zinc-500">5 order terakhir dari berbagai channel penjualan Anda.</p>
          </div>
          <Link href="/dashboard/orders" className="text-xs font-bold text-brand hover:text-brand-light transition-colors flex items-center gap-1 font-mono">
            Lihat Semua <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-xs font-mono text-left">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase tracking-wider">
                <th className="py-4">Order ID</th>
                <th className="py-4">Pelanggan</th>
                <th className="py-4">Produk/Jasa</th>
                <th className="py-4 text-right">Total</th>
                <th className="py-4">Waktu</th>
                <th className="py-4">Status</th>
              </tr>
            </thead>
            <tbody>
              {recentOrders.map((order) => (
                <tr key={order.id} className="border-b border-zinc-800/50 hover:bg-zinc-950/40 transition-colors">
                  <td className="py-4 text-white font-bold">{order.id}</td>
                  <td className="py-4 text-zinc-300">{order.buyer}</td>
                  <td className="py-4 text-zinc-300 max-w-[200px]">
                    <span className="mr-1">{order.type}</span>
                    <span className="truncate">{order.item}</span>
                  </td>
                  <td className="py-4 text-right text-brand-ghost font-bold">Rp {order.price.toLocaleString("id-ID")}</td>
                  <td className="py-4 text-zinc-500">{order.date}</td>
                  <td className="py-4">
                    <span className={`px-2.5 py-0.5 rounded text-[9px] font-extrabold uppercase ${
                      order.status === "paid" 
                        ? "bg-brand/10 text-brand border border-brand/20" 
                        : order.status === "pending"
                        ? "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20"
                        : "bg-red-500/10 text-red-400 border border-red-500/20"
                    }`}>
                      {order.status === "paid" ? "✓ Lunas" : order.status === "pending" ? "⏳ Pending" : "✕ Expired"}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ================= QUICK SECTOR METRICS ================= */}
      <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { emoji: "☕", label: "Warung/Kuliner", orders: 12, color: "border-yellow-500/20 bg-yellow-500/5" },
          { emoji: "👕", label: "Fashion/Toko", orders: 6, color: "border-purple-500/20 bg-purple-500/5" },
          { emoji: "💇‍♀️", label: "Salon/Beauty", orders: 3, color: "border-pink-500/20 bg-pink-500/5" },
          { emoji: "🧺", label: "Laundry/Jasa", orders: 3, color: "border-sky-500/20 bg-sky-500/5" },
        ].map((cat, i) => (
          <div key={i} className={`p-4 rounded-2xl border ${cat.color} flex items-center gap-3`}>
            <span className="text-2xl">{cat.emoji}</span>
            <div className="font-mono">
              <p className="text-[10px] text-zinc-500">{cat.label}</p>
              <p className="text-xs font-bold text-white">{cat.orders} order hari ini</p>
            </div>
          </div>
        ))}
      </section>
    </div>
  );
}
