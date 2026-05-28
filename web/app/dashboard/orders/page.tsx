"use client";

import React, { useState } from "react";
import { 
  CreditCard, 
  Search, 
  Download, 
  Eye, 
  Check, 
  X, 
  User, 
  Phone, 
  MapPin, 
  FileText,
  Clock,
  Plus,
  Calendar,
  AlertCircle,
  TrendingUp,
  ShoppingBag,
  ChevronDown
} from "lucide-react";
import { toast } from "react-hot-toast";

interface Order {
  id: string;
  buyerName: string;
  buyerPhone: string;
  buyerAddress: string;
  itemName: string;
  price: number;
  status: "paid" | "pending" | "processing" | "done" | "cancelled";
  date: string;
  paymentType: string;
  referenceNumber: string;
}

export default function OrdersPage() {
  // Mock data transaksi pesanan — berbagai jenis UMKM
  const [orders, setOrders] = useState<Order[]>([
    { id: "ORD-901", buyerName: "Sari Rahayu", buyerPhone: "081299998888", buyerAddress: "Jl. Mampang Prapatan No. 5, Jakarta Selatan", itemName: "Kopi Aren Melted Latte x2 + Croissant Almond", price: 69000, status: "paid", date: "2026-05-28", paymentType: "QRIS", referenceNumber: "REF90112345" },
    { id: "ORD-900", buyerName: "Dian Kusuma", buyerPhone: "08987654321", buyerAddress: "Pasar Atom Blok B No. 34, Surabaya", itemName: "T-Shirt Oversized Streetwear Noir", price: 185000, status: "paid", date: "2026-05-28", paymentType: "GoPay", referenceNumber: "REF90019283" },
    { id: "ORD-899", buyerName: "Nurul Fadilah", buyerPhone: "087711112222", buyerAddress: "Jl. Setia Budi No. 12, Medan", itemName: "Hair Treatment + Creambath Herbal", price: 250000, status: "pending", date: "2026-05-28", paymentType: "BCA Transfer", referenceNumber: "REF89920194" },
    { id: "ORD-898", buyerName: "Budi Santoso", buyerPhone: "081322223333", buyerAddress: "Jl. Sudirman No. 45, Semarang", itemName: "Layanan Cuci Kering Kilat 5kg", price: 45000, status: "processing", date: "2026-05-27", paymentType: "OVO", referenceNumber: "REF89838491" },
    { id: "ORD-897", buyerName: "Ahmad Fauzi", buyerPhone: "085699990000", buyerAddress: "Jl. Ahmad Yani No. 20, Yogyakarta", itemName: "Oli Mesin Matic + Servis Ringan", price: 125000, status: "cancelled", date: "2026-05-27", paymentType: "Mandiri Transfer", referenceNumber: "REF89728492" },
    { id: "ORD-896", buyerName: "Rina Marlina", buyerPhone: "081988887777", buyerAddress: "Jl. Gatot Subroto No. 7, Bandung", itemName: "Kue Tart Ulang Tahun Custom", price: 280000, status: "done", date: "2026-05-26", paymentType: "ShopeePay", referenceNumber: "REF89691038" },
  ]);

  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState("all");
  const [dateRange, setDateRange] = useState("all"); // all, today, yesterday, this-week

  // Selected Order for Detail Modal (Drawer)
  const [selectedOrder, setSelectedOrder] = useState<Order | null>(null);

  // Quick Create Order Modal State
  const [isQuickCreateOpen, setIsQuickCreateOpen] = useState(false);
  const [newName, setNewName] = useState("");
  const [newPhone, setNewPhone] = useState("");
  const [newAddress, setNewAddress] = useState("");
  const [newItemName, setNewItemName] = useState("Kopi Aren Melted Latte");
  const [newItemPrice, setNewItemPrice] = useState("22000");
  const [newPayMethod, setNewPayMethod] = useState("QRIS");

  const filteredOrders = orders.filter(o => {
    const matchesSearch = o.buyerName.toLowerCase().includes(searchQuery.toLowerCase()) || 
                          o.id.toLowerCase().includes(searchQuery.toLowerCase());
    
    const matchesStatus = filterStatus === "all" || o.status === filterStatus;
    
    let matchesDate = true;
    if (dateRange === "today") {
      matchesDate = o.date === "2026-05-28";
    } else if (dateRange === "yesterday") {
      matchesDate = o.date === "2026-05-27";
    } else if (dateRange === "this-week") {
      matchesDate = o.date >= "2026-05-22";
    }
    
    return matchesSearch && matchesStatus && matchesDate;
  });

  // Manual Payment Validation
  const handleUpdateStatus = (id: string, newStatus: Order["status"]) => {
    setOrders(prev => 
      prev.map(o => o.id === id ? { ...o, status: newStatus } : o)
    );
    
    if (selectedOrder && selectedOrder.id === id) {
      setSelectedOrder(prev => prev ? { ...prev, status: newStatus } : null);
    }

    let msg = `Order ${id} berhasil diperbarui menjadi ${newStatus}!`;
    if (newStatus === "paid") msg = `Pembayaran order ${id} dikonfirmasi LUNAS! 💸`;
    else if (newStatus === "cancelled") msg = `Order ${id} dibatalkan! ✕`;

    toast.success(msg, {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  // Excel Export Simulation
  const handleExportExcel = () => {
    toast.loading("Mengekspor laporan penjualan ke Excel...", { id: "export" });
    
    setTimeout(() => {
      toast.dismiss("export");
      toast.success("Sukses mengunduh dedemit_umkm_orders_report.xlsx! 📊", {
        style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
      });
    }, 1200);
  };

  // Save new order from Cashier terminal
  const handleSaveQuickOrder = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName || !newItemPrice) {
      toast.error("Nama pelanggan dan total harga wajib diisi!");
      return;
    }

    const priceNum = parseFloat(newItemPrice) || 0;
    const newOrder: Order = {
      id: `ORD-${902 + orders.length}`,
      buyerName: newName,
      buyerPhone: newPhone || "0812XXXXXXXX",
      buyerAddress: newAddress || "Beli Langsung di Toko",
      itemName: newItemName,
      price: priceNum,
      status: "paid",
      date: "2026-05-28",
      paymentType: newPayMethod,
      referenceNumber: `REF${Date.now().toString().slice(-8)}`
    };

    setOrders([newOrder, ...orders]);
    setIsQuickCreateOpen(false);
    
    // Reset Form
    setNewName("");
    setNewPhone("");
    setNewAddress("");
    setNewItemPrice("22000");

    toast.success("Transaksi kasir lunas berhasil dicatat! ☕🎉", {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  return (
    <div className="space-y-8 font-mono text-xs">
      
      {/* HEADER ORDERS */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2 font-sans">
            Pelacak Transaksi Pesanan <span className="animate-pulse">💸</span>
          </h2>
          <p className="text-[10px] text-zinc-500">Otomatis konfirmasi via Midtrans Webhook atau lakukan validasi manual lunas beserta ekspor Excel sheet.</p>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={handleExportExcel}
            className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-950 text-zinc-400 hover:text-white transition-all font-bold"
          >
            <Download className="w-3.5 h-3.5" /> Export ke Excel
          </button>

          <button 
            onClick={() => setIsQuickCreateOpen(true)}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-brand hover:bg-brand-dark text-white shadow-lg hover:shadow-brand/20 transition-all font-bold font-sans text-xs"
          >
            <Plus className="w-4 h-4" /> Quick Order
          </button>
        </div>
      </header>

      {/* ================= CONTROLS & FILTER SECTION ================= */}
      <section className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Search Bar */}
        <div className="lg:col-span-2 relative">
          <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-500">
            <Search className="w-4 h-4" />
          </span>
          <input 
            type="text" 
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Cari order ID atau nama pembeli..."
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-3 pl-10 pr-4 text-zinc-200 focus:outline-none focus:border-brand-light transition-all"
          />
        </div>

        {/* Date Range Picker Simulator */}
        <div className="relative">
          <span className="absolute inset-y-0 left-0 pl-3.5 flex items-center pointer-events-none text-zinc-500">
            <Calendar className="w-4 h-4" />
          </span>
          <select 
            value={dateRange}
            onChange={(e) => setDateRange(e.target.value)}
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-3 pl-10 pr-10 text-zinc-300 focus:outline-none focus:border-brand-light transition-all appearance-none"
          >
            <option value="all">Semua Tanggal</option>
            <option value="today">Hari Ini (28 Mei)</option>
            <option value="yesterday">Kemarin (27 Mei)</option>
            <option value="this-week">Seminggu Terakhir</option>
          </select>
          <span className="absolute inset-y-0 right-3.5 flex items-center pointer-events-none text-zinc-500">
            <ChevronDown className="w-4 h-4" />
          </span>
        </div>

        {/* Filter Status */}
        <div className="relative">
          <select 
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-3 px-3 text-zinc-300 focus:outline-none focus:border-brand-light transition-all appearance-none"
          >
            <option value="all">Semua Status</option>
            <option value="paid">Lunas (Paid)</option>
            <option value="pending">Tertunda (Pending)</option>
            <option value="processing">Diproses (Processing)</option>
            <option value="done">Selesai (Done)</option>
            <option value="cancelled">Batal (Cancelled)</option>
          </select>
          <span className="absolute inset-y-0 right-3.5 flex items-center pointer-events-none text-zinc-500">
            <ChevronDown className="w-4 h-4" />
          </span>
        </div>
      </section>

      {/* ================= ORDERS DATATABLE ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase tracking-wider">
                <th className="py-4">ORDER ID</th>
                <th className="py-4">PEMBELI</th>
                <th className="py-4">PRODUK/JASA</th>
                <th className="py-4 text-right">TOTAL</th>
                <th className="py-4 pl-4">METODE</th>
                <th className="py-4">TANGGAL</th>
                <th className="py-4">STATUS</th>
                <th className="py-4 text-center">AKSI</th>
              </tr>
            </thead>
            <tbody>
              {filteredOrders.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-zinc-500">Tidak ada pesanan ditemukan.</td>
                </tr>
              ) : (
                filteredOrders.map((o) => (
                  <tr key={o.id} className="border-b border-zinc-800/50 hover:bg-zinc-950/40 transition-colors">
                    <td className="py-4 text-white font-bold">{o.id}</td>
                    <td className="py-4 text-zinc-300 font-bold">{o.buyerName}</td>
                    <td className="py-4 text-zinc-400 truncate max-w-[150px]">{o.itemName}</td>
                    <td className="py-4 text-right text-brand-ghost font-bold">Rp {o.price.toLocaleString("id-ID")}</td>
                    <td className="py-4 pl-4 text-zinc-500 uppercase">{o.paymentType}</td>
                    <td className="py-4 text-zinc-500">{o.date}</td>
                    <td className="py-4">
                      <span className={`px-2.5 py-0.5 rounded text-[8px] font-extrabold uppercase ${
                        o.status === "paid" || o.status === "done"
                          ? "bg-brand/10 text-brand border border-brand/20" 
                          : o.status === "pending" || o.status === "processing"
                          ? "bg-yellow-500/10 text-yellow-400 border border-yellow-500/20"
                          : "bg-red-500/10 text-red-400 border border-red-500/20"
                      }`}>
                        {o.status === "paid" ? "✓ Lunas" : o.status === "done" ? "✓ Selesai" : o.status === "processing" ? "⏳ Diproses" : o.status === "pending" ? "⏳ Pending" : "✕ Batal"}
                      </span>
                    </td>
                    <td className="py-4 text-center">
                      <button 
                        onClick={() => setSelectedOrder(o)}
                        className="px-2 py-1 bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 rounded-lg text-brand-ghost transition-colors inline-flex items-center gap-1 font-bold"
                      >
                        <Eye className="w-3 h-3" /> Detail
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* ================= MODAL DETAIL / DRAWER OVERLAY ================= */}
      {selectedOrder && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in">
          <div className="fixed inset-0 bg-black/75 backdrop-blur-sm" onClick={() => setSelectedOrder(null)} />
          
          <div className="w-full max-w-2xl bg-zinc-900 border border-zinc-800 rounded-3xl p-6 relative z-50 text-xs font-mono grid grid-cols-1 md:grid-cols-5 gap-6">
            
            {/* Left side: Order Info */}
            <div className="md:col-span-3 space-y-4 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-center pb-3 border-b border-zinc-800 mb-4">
                  <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-1.5 font-sans">
                    <FileText className="w-4 h-4 text-brand-ghost" /> Detail Transaksi {selectedOrder.id}
                  </h3>
                  <button 
                    onClick={() => setSelectedOrder(null)}
                    className="p-1 rounded-lg text-zinc-500 hover:text-white"
                  >
                    <X className="w-4 h-4" />
                  </button>
                </div>

                <div className="space-y-2.5 text-zinc-300">
                  <div className="flex items-center gap-2">
                    <User className="w-3.5 h-3.5 text-zinc-500" />
                    <span>Pembeli: <span className="text-white font-bold">{selectedOrder.buyerName}</span></span>
                  </div>
                  <div className="flex items-center gap-2">
                    <Phone className="w-3.5 h-3.5 text-zinc-500" />
                    <span>Telepon: <span className="text-zinc-450">{selectedOrder.buyerPhone}</span></span>
                  </div>
                  <div className="flex items-start gap-2">
                    <MapPin className="w-3.5 h-3.5 text-zinc-500 mt-0.5" />
                    <span className="leading-normal">Alamat: <span className="text-zinc-400">{selectedOrder.buyerAddress}</span></span>
                  </div>
                  
                  <div className="border-t border-zinc-800/65 my-2.5 pt-2.5 space-y-1.5">
                    <div>Keranjang: <span className="text-white font-bold">{selectedOrder.itemName}</span></div>
                    <div>Metode: <span className="text-white uppercase font-bold">{selectedOrder.paymentType}</span></div>
                    <div>Ref No: <span className="text-zinc-400 font-mono font-bold">{selectedOrder.referenceNumber}</span></div>
                    <div>Subtotal Tagihan: <span className="text-brand-ghost font-bold text-sm">Rp {selectedOrder.price.toLocaleString("id-ID")}</span></div>
                  </div>
                </div>
              </div>

              {/* Status Update Actions */}
              <div className="space-y-2 pt-3 border-t border-zinc-800">
                <span className="text-[9px] text-zinc-500 block uppercase font-bold">Modifikasi Status Transaksi:</span>
                <div className="flex flex-wrap gap-2">
                  {selectedOrder.status !== "paid" && selectedOrder.status !== "done" && (
                    <button 
                      onClick={() => handleUpdateStatus(selectedOrder.id, "paid")}
                      className="px-3 py-2 bg-brand text-white rounded-xl hover:bg-brand-dark transition-all flex-1 font-bold text-center"
                    >
                      Konfirmasi Lunas
                    </button>
                  )}
                  {selectedOrder.status === "paid" && (
                    <button 
                      onClick={() => handleUpdateStatus(selectedOrder.id, "processing")}
                      className="px-3 py-2 bg-yellow-500 text-zinc-950 rounded-xl hover:bg-yellow-650 transition-all flex-1 font-bold text-center"
                    >
                      Mulai Proses
                    </button>
                  )}
                  {selectedOrder.status === "processing" && (
                    <button 
                      onClick={() => handleUpdateStatus(selectedOrder.id, "done")}
                      className="px-3 py-2 bg-brand text-white rounded-xl hover:bg-brand-dark transition-all flex-1 font-bold text-center"
                    >
                      Selesaikan Order
                    </button>
                  )}
                  {selectedOrder.status !== "cancelled" && selectedOrder.status !== "done" && (
                    <button 
                      onClick={() => handleUpdateStatus(selectedOrder.id, "cancelled")}
                      className="px-3 py-2 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-xl transition-all font-bold"
                    >
                      Batalkan
                    </button>
                  )}
                </div>
              </div>
            </div>

            {/* Right side: Visual Receipt OCR Simulator */}
            <div className="md:col-span-2 bg-zinc-950 rounded-2xl border border-zinc-800 p-4 flex flex-col justify-between gap-4">
              <div>
                <span className="text-[10px] text-zinc-500 block mb-2 font-bold uppercase tracking-wider">Simulasi Bukti Transfer (OCR)</span>
                
                {/* Visual receipt template */}
                <div className="bg-white text-zinc-900 p-4 rounded-xl shadow-inner relative overflow-hidden font-mono text-[9px] leading-relaxed">
                  {/* Decorative stamp/watermark based on status */}
                  {selectedOrder.status === "paid" || selectedOrder.status === "done" ? (
                    <div className="absolute top-[30%] left-[10%] border-4 border-emerald-600/40 text-emerald-600/40 rounded px-2 py-0.5 text-xs font-bold uppercase rotate-12 pointer-events-none">
                      PAID ✓
                    </div>
                  ) : selectedOrder.status === "cancelled" ? (
                    <div className="absolute top-[30%] left-[10%] border-4 border-red-650/40 text-red-655/40 rounded px-2 py-0.5 text-xs font-bold uppercase rotate-12 pointer-events-none">
                      VOID ✕
                    </div>
                  ) : (
                    <div className="absolute top-[30%] left-[10%] border-4 border-yellow-600/30 text-yellow-600/30 rounded px-2 py-0.5 text-xs font-bold uppercase rotate-12 pointer-events-none">
                      UNPAID ⏳
                    </div>
                  )}

                  <div className="text-center font-bold text-xs border-b border-dashed border-zinc-300 pb-2 mb-2 uppercase">
                    MOBILE BANKING SLIP
                  </div>
                  
                  <div className="space-y-1 select-none">
                    <div>TIMESTAMP : {selectedOrder.date} 12:45</div>
                    <div>SENDER : {selectedOrder.buyerName.toUpperCase()}</div>
                    <div>GATEWAY : {selectedOrder.paymentType.split(" ")[0].toUpperCase()}</div>
                    <div>BENEFICIARY : DEDEMIT UMKM</div>
                    <div className="border-t border-dashed border-zinc-300 pt-1 mt-1 font-bold text-zinc-950">
                      NOMINAL : RP {selectedOrder.price.toLocaleString()}
                    </div>
                    <div>REFERENCE : {selectedOrder.referenceNumber}</div>
                  </div>
                </div>
              </div>

              {/* OCR Information summary */}
              <div className="p-3 bg-zinc-900 border border-zinc-800/80 rounded-xl space-y-1 font-mono text-[10px]">
                <div className="text-zinc-500 font-bold">GEMINI OCR SCANNER:</div>
                <div>Metode Bayar: <span className="text-white uppercase font-bold">{selectedOrder.paymentType}</span></div>
                <div>Status OCR: {selectedOrder.status === "paid" || selectedOrder.status === "done" ? (
                  <span className="text-brand font-bold">MATCHED (100% Pas) ✅</span>
                ) : (
                  <span className="text-yellow-400 font-bold">WAITING CONFIRMATION ⏳</span>
                )}</div>
              </div>
            </div>

          </div>
        </div>
      )}

      {/* ================= MODAL QUICK CREATE ORDER ================= */}
      {isQuickCreateOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="fixed inset-0 bg-black/75 backdrop-blur-sm" onClick={() => setIsQuickCreateOpen(false)} />
          
          <div className="w-full max-w-lg bg-zinc-900 border border-zinc-800 rounded-3xl p-6 relative z-50 text-xs font-mono">
            <div className="flex justify-between items-center pb-4 border-b border-zinc-800 mb-5">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-1.5 font-sans">
                <ShoppingBag className="w-4 h-4 text-brand-ghost" /> + Buat Quick Order (Kasir Langsung)
              </h3>
              <button 
                onClick={() => setIsQuickCreateOpen(false)}
                className="p-1 rounded-lg text-zinc-500 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveQuickOrder} className="space-y-4">
              <div>
                <label className="text-zinc-500 block mb-1">NAMA PELANGGAN *</label>
                <input 
                  type="text" 
                  required
                  placeholder="Contoh: Rian Hidayat"
                  value={newName}
                  onChange={(e) => setNewName(e.target.value)}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none focus:border-brand-light"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-zinc-500 block mb-1">NO HP PELANGGAN</label>
                  <input 
                    type="text" 
                    placeholder="08123456789"
                    value={newPhone}
                    onChange={(e) => setNewPhone(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-200 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-zinc-500 block mb-1">METODE BAYAR</label>
                  <select 
                    value={newPayMethod}
                    onChange={(e) => setNewPayMethod(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
                  >
                    <option value="QRIS">QRIS Tagihan</option>
                    <option value="Cash / Tunai">Cash / Tunai</option>
                    <option value="GoPay">GoPay</option>
                    <option value="BCA Transfer">BCA Transfer</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="text-zinc-500 block mb-1">PRODUK YANG DIBELI</label>
                <input 
                  type="text" 
                  value={newItemName}
                  onChange={(e) => setNewItemName(e.target.value)}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-250 focus:outline-none"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-zinc-500 block mb-1">HARGA TOTAL (RP) *</label>
                  <input 
                    type="number" 
                    required
                    value={newItemPrice}
                    onChange={(e) => setNewItemPrice(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none"
                  />
                </div>
                <div>
                  <label className="text-zinc-500 block mb-1">LOKASI / ALAMAT</label>
                  <input 
                    type="text" 
                    placeholder="Beli Langsung di Toko"
                    value={newAddress}
                    onChange={(e) => setNewAddress(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none"
                  />
                </div>
              </div>

              <div className="pt-2 flex gap-3">
                <button 
                  type="button"
                  onClick={() => setIsQuickCreateOpen(false)}
                  className="w-1/2 border border-zinc-800 text-zinc-400 py-3 rounded-xl hover:bg-zinc-850 hover:text-white transition-colors font-bold"
                >
                  Batal
                </button>
                <button 
                  type="submit"
                  className="w-1/2 bg-brand text-white py-3 rounded-xl hover:bg-brand-dark shadow-lg transition-colors font-bold"
                >
                  Catat & Lunasi
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
