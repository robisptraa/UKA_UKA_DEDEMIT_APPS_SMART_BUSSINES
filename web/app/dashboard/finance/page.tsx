"use client";

import React, { useState } from "react";
import { 
  Wallet, 
  Plus, 
  Search, 
  Download, 
  X, 
  ArrowUpRight, 
  ArrowDownRight,
  Sparkles,
  Camera,
  Trash2,
  Check,
  FileText
} from "lucide-react";
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer,
  Legend
} from "recharts";
import { toast } from "react-hot-toast";

interface Expense {
  id: string;
  merchant: string;
  category: string;
  date: string;
  total: number;
  notes: string;
  scanned: boolean;
}

export default function FinancePage() {
  // Summary Metrics
  const revenue = 32450000;
  const [expenses, setExpenses] = useState<Expense[]>([
    { id: "EXP-01", merchant: "Kopi Mulya Supplier", category: "Bahan Baku", date: "2026-05-28", total: 1200000, notes: "Pembelian 10kg biji kopi house blend", scanned: false },
    { id: "EXP-02", merchant: "PLN Kantor Mampang", category: "Listrik & Air", date: "2026-05-25", total: 450000, notes: "Tagihan listrik toko bulan Mei", scanned: true },
    { id: "EXP-03", merchant: "Pabrik Cup Plastik Jaya", category: "Kemasan", date: "2026-05-22", total: 320000, notes: "Cup plastik sablon logo 500 pcs", scanned: false },
    { id: "EXP-04", merchant: "Facebook Ads Inc", category: "Pemasaran", date: "2026-05-18", total: 500000, notes: "Iklan media sosial promosi bot Telegram", scanned: true },
    { id: "EXP-05", merchant: "Indogrosir Sembako", category: "Operasional", date: "2026-05-10", total: 180000, notes: "Pembelian detergen laundry & sabun cuci", scanned: false },
  ]);

  const totalExpense = expenses.reduce((acc, curr) => acc + curr.total, 0);
  const netProfit = revenue - totalExpense;

  // Mock 30 days cashflow (sampled weekly for cleaner representation)
  const cashflowData = [
    { name: "Minggu 1", Pemasukan: 6800000, Pengeluaran: 1200000 },
    { name: "Minggu 2", Pemasukan: 8200000, Pengeluaran: 1800000 },
    { name: "Minggu 3", Pemasukan: 7900000, Pengeluaran: 950000 },
    { name: "Minggu 4", Pemasukan: 9550000, Pengeluaran: 2650000 },
  ];

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [merchant, setMerchant] = useState("");
  const [category, setCategory] = useState("Bahan Baku");
  const [date, setDate] = useState("2026-05-28");
  const [total, setTotal] = useState("");
  const [notes, setNotes] = useState("");
  const [scanned, setScanned] = useState(false);

  const formatRupiah = (val: number) => {
    return `Rp ${val.toLocaleString("id-ID")}`;
  };

  const formatChartRupiah = (val: number) => {
    if (val >= 1000000) return `${(val / 1000000).toFixed(1)}Jt`;
    return `${val}`;
  };

  // Add manual expense
  const handleSaveExpense = (e: React.FormEvent) => {
    e.preventDefault();
    if (!merchant || !total) {
      toast.error("Nama merchant dan nominal pengeluaran wajib diisi!");
      return;
    }

    const newExpense: Expense = {
      id: `EXP-0${expenses.length + 1}`,
      merchant,
      category,
      date,
      total: parseFloat(total) || 0,
      notes,
      scanned
    };

    setExpenses([newExpense, ...expenses]);
    setIsModalOpen(false);
    resetForm();

    toast.success("Catatan pengeluaran kas keluar berhasil disimpan! 💸", {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  // OCR Scan Receipt Simulation
  const handleScanReceipt = () => {
    toast.loading("Gemini AI sedang membaca struktur struk nota belanja...", { id: "ocr" });
    
    setTimeout(() => {
      setMerchant("Pertamina Gas Mampang");
      setCategory("Operasional");
      setTotal("150000");
      setNotes("Hasil Scan AI: Pembelian Tabung Gas Melon 3x");
      setScanned(true);
      
      toast.dismiss("ocr");
      toast.success("OCR Berhasil! Data pengeluaran terisi otomatis. 🤖📸", {
        style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
      });
    }, 1500);
  };

  const resetForm = () => {
    setMerchant("");
    setCategory("Bahan Baku");
    setDate("2026-05-28");
    setTotal("");
    setNotes("");
    setScanned(false);
  };

  // Delete Expense
  const handleDeleteExpense = (id: string) => {
    setExpenses(prev => prev.filter(e => e.id !== id));
    toast.error("Catatan pengeluaran dihapus! 🗑️", {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  // PDF Export trigger
  const handleExportPDF = () => {
    toast.loading("Menyusun laporan laba-rugi formal...", { id: "pdf" });
    
    setTimeout(() => {
      toast.dismiss("pdf");
      window.print(); // Invokes formal premium print preview
      toast.success("Laporan Keuangan Dedemit UMKM siap dicetak! 📂", {
        style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
      });
    }, 1200);
  };

  return (
    <div className="space-y-8 font-mono text-xs print:bg-white print:text-zinc-950">
      
      {/* HEADER FINANCE */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 print:hidden">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2 font-sans">
            Laporan Keuangan & Kas Keluar <span className="animate-pulse">💰</span>
          </h2>
          <p className="text-[10px] text-zinc-500">Pantau perbandingan arus kas pemasukan vs pengeluaran operasional serta unduh slip laba rugi PDF.</p>
        </div>

        <div className="flex items-center gap-3">
          <button 
            onClick={handleExportPDF}
            className="flex items-center gap-1.5 px-3.5 py-2.5 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-950 text-zinc-400 hover:text-white transition-all font-bold"
          >
            <Download className="w-3.5 h-3.5" /> Cetak Laporan PDF
          </button>
          
          <button 
            onClick={() => { resetForm(); setIsModalOpen(true); }}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl bg-brand hover:bg-brand-dark text-white shadow-lg hover:shadow-brand/20 transition-all font-bold font-sans text-xs"
          >
            <Plus className="w-4 h-4" /> Catat Kas Keluar
          </button>
        </div>
      </header>

      {/* ================= PRINT FORMAT ONLY (HIDDEN IN SCREEN) ================= */}
      <div className="hidden print:block font-sans space-y-6 text-zinc-900">
        <div className="text-center pb-4 border-b-2 border-zinc-900">
          <h1 className="text-2xl font-black">LAPORAN LABA RUGI UMKM</h1>
          <p className="text-xs uppercase tracking-widest text-zinc-500 font-mono">DEDEMIT COFFEE & GOODS · MEI 2026</p>
        </div>
        <div className="grid grid-cols-3 gap-6 font-mono text-xs">
          <div>TOTAL PEMASUKAN:<br /><strong className="text-lg text-emerald-700">{formatRupiah(revenue)}</strong></div>
          <div>TOTAL PENGELUARAN:<br /><strong className="text-lg text-red-700">{formatRupiah(totalExpense)}</strong></div>
          <div>LABA BERSIH:<br /><strong className="text-lg text-blue-700">{formatRupiah(netProfit)}</strong></div>
        </div>
      </div>

      {/* ================= SUMMARY METRICS CARD ================= */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6 print:hidden">
        {/* Pemasukan Card */}
        <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 flex justify-between items-center relative overflow-hidden">
          <div className="space-y-1">
            <span className="text-[10px] text-zinc-400 block font-bold uppercase">Pemasukan Bulan Ini</span>
            <h3 className="text-2xl font-extrabold text-white">{formatRupiah(revenue)}</h3>
            <span className="text-[9px] text-brand flex items-center font-bold gap-0.5"><ArrowUpRight className="w-3.5 h-3.5" /> +18% peningkatan</span>
          </div>
          <div className="p-3 bg-brand/10 border border-brand/20 rounded-xl text-brand">
            <Wallet className="w-6 h-6" />
          </div>
        </div>

        {/* Pengeluaran Card */}
        <div className="p-6 rounded-2xl bg-zinc-900 border border-zinc-800 flex justify-between items-center relative overflow-hidden">
          <div className="space-y-1">
            <span className="text-[10px] text-zinc-400 block font-bold uppercase">Pengeluaran Bulan Ini</span>
            <h3 className="text-2xl font-extrabold text-white">{formatRupiah(totalExpense)}</h3>
            <span className="text-[9px] text-red-400 flex items-center font-bold gap-0.5"><ArrowDownRight className="w-3.5 h-3.5" /> Catatan operasional UMKM</span>
          </div>
          <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-xl text-red-400">
            <ArrowDownRight className="w-6 h-6" />
          </div>
        </div>

        {/* Laba Bersih Card */}
        <div className="p-6 rounded-2xl bg-zinc-900 border border-brand-ghost/25 flex justify-between items-center relative overflow-hidden shadow-lg hover:shadow-brand-ghost/5">
          <div className="space-y-1">
            <span className="text-[10px] text-zinc-400 block font-bold uppercase">Estimasi Laba Bersih</span>
            <h3 className="text-2xl font-extrabold text-brand-ghost">{formatRupiah(netProfit)}</h3>
            <span className="text-[9px] text-teal-400 flex items-center font-bold gap-0.5">✓ Sehat & Profitable</span>
          </div>
          <div className="p-3 bg-brand-ghost/10 border border-brand-ghost/20 rounded-xl text-brand-ghost">
            <Sparkles className="w-6 h-6" />
          </div>
        </div>
      </section>

      {/* ================= RECHARTS BAR CHART CASHFLOW ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 print:hidden">
        <div className="mb-6">
          <span className="text-[10px] font-bold text-brand-ghost tracking-widest uppercase block mb-1">CASHFLOW MONITOR</span>
          <h3 className="text-sm font-bold text-white font-sans">Perbandingan Cashflow Mingguan (30 Hari)</h3>
        </div>

        <div className="w-full h-64 font-mono text-[9px]">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={cashflowData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1f1f23" vertical={false} />
              <XAxis dataKey="name" stroke="#52525b" tickLine={false} />
              <YAxis stroke="#52525b" tickLine={false} tickFormatter={formatChartRupiah} />
              <Tooltip 
                contentStyle={{ backgroundColor: "#18181b", borderColor: "#27272a", borderRadius: "12px", color: "#fff" }}
                formatter={(value: any) => [formatRupiah(Number(value)), ""]}
              />
              <Legend verticalAlign="top" height={36} wrapperStyle={{ fontSize: "10px" }} />
              <Bar dataKey="Pemasukan" fill="#10B981" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Pengeluaran" fill="#F43F5E" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </section>

      {/* ================= EXPENSE TABLE ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 overflow-hidden print:w-full print:border-none print:p-0">
        <div className="flex justify-between items-center mb-6 print:hidden">
          <div>
            <h3 className="text-sm font-bold text-white font-sans">Buku Catatan Pengeluaran Kas</h3>
            <p className="text-[10px] text-zinc-500">Daftar pengeluaran operasional toko, kulakan bahan baku, dan iklan marketing.</p>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase tracking-wider print:text-zinc-900 print:border-zinc-900">
                <th className="py-4">ID</th>
                <th className="py-4">MERCHANT / PENERIMA</th>
                <th className="py-4">KATEGORI</th>
                <th className="py-4">TANGGAL</th>
                <th className="py-4">KETERANGAN</th>
                <th className="py-4 text-right">TOTAL KAS KELUAR</th>
                <th className="py-4 text-center print:hidden">AKSI</th>
              </tr>
            </thead>
            <tbody>
              {expenses.map((exp) => (
                <tr key={exp.id} className="border-b border-zinc-800/50 hover:bg-zinc-950/40 transition-colors print:text-zinc-800 print:border-zinc-300">
                  <td className="py-4 text-zinc-500 font-bold">{exp.id}</td>
                  <td className="py-4 text-white font-bold print:text-zinc-950 flex items-center gap-1.5">
                    {exp.merchant}
                    {exp.scanned && (
                      <span className="px-1.5 py-0.5 rounded text-[8px] bg-brand/10 text-brand border border-brand/20 font-mono font-extrabold uppercase print:hidden">AI Scan</span>
                    )}
                  </td>
                  <td className="py-4 text-zinc-400 print:text-zinc-700">{exp.category}</td>
                  <td className="py-4 text-zinc-550 print:text-zinc-600">{exp.date}</td>
                  <td className="py-4 text-zinc-450 print:text-zinc-650 max-w-[200px] truncate">{exp.notes}</td>
                  <td className="py-4 text-right text-red-400 print:text-red-700 font-extrabold pr-2">{formatRupiah(exp.total)}</td>
                  <td className="py-4 text-center print:hidden">
                    <button 
                      onClick={() => handleDeleteExpense(exp.id)}
                      className="p-1.5 bg-red-500/10 hover:bg-red-500/20 text-red-400 rounded-lg transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      {/* ================= MODAL ADD EXPENSE OVERLAY ================= */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <div className="fixed inset-0 bg-black/75 backdrop-blur-sm" onClick={() => setIsModalOpen(false)} />
          
          <div className="w-full max-w-lg bg-zinc-900 border border-zinc-800 rounded-3xl p-6 relative z-50 text-xs font-mono">
            <div className="flex justify-between items-center pb-4 border-b border-zinc-800 mb-5">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-1.5 font-sans">
                <Wallet className="w-4 h-4 text-brand-ghost" /> + Catat Pengeluaran Baru
              </h3>
              <button 
                onClick={() => setIsModalOpen(false)}
                className="p-1 rounded-lg text-zinc-500 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* AI Struk Scanner Simulator Button */}
            <div className="mb-5 p-4 rounded-xl bg-brand/5 border border-brand/20 flex items-center justify-between">
              <div className="space-y-0.5">
                <span className="text-brand font-bold uppercase block text-[9px]">Pintasan Scan AI Struk 🤖📸</span>
                <span className="text-[10px] text-zinc-400">Punya foto struk belanja? Simulasikan scan struk dengan Gemini AI.</span>
              </div>
              
              <button
                type="button"
                onClick={handleScanReceipt}
                className="flex items-center gap-1 bg-brand text-white font-bold px-3 py-2 rounded-lg hover:bg-brand-dark transition-all text-[10px] font-sans"
              >
                <Camera className="w-3.5 h-3.5" /> Scan Struk Nota
              </button>
            </div>

            <form onSubmit={handleSaveExpense} className="space-y-4">
              <div>
                <label className="text-zinc-500 block mb-1">MERCHANT / TOKO PENERIMA *</label>
                <input 
                  type="text" 
                  required
                  placeholder="Contoh: Kopi Mulya Supplier, Toko Sembako Makmur..."
                  value={merchant}
                  onChange={(e) => setMerchant(e.target.value)}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none focus:border-brand-light"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                 <div>
                   <label className="text-zinc-500 block mb-1">KATEGORI OPERASIONAL</label>
                   <select 
                     value={category}
                     onChange={(e) => setCategory(e.target.value)}
                     className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-350 focus:outline-none"
                   >
                     <option value="Bahan Baku">Bahan Baku (Restock)</option>
                     <option value="Listrik & Air">Listrik & Air</option>
                     <option value="Kemasan">Kemasan</option>
                     <option value="Pemasaran">Pemasaran (Ads)</option>
                     <option value="Operasional">Operasional Lainnya</option>
                   </select>
                 </div>
                 <div>
                   <label className="text-zinc-500 block mb-1">TANGGAL TRANSAKSI</label>
                   <input 
                     type="date" 
                     value={date}
                     onChange={(e) => setDate(e.target.value)}
                     className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-300 focus:outline-none text-center"
                   />
                 </div>
              </div>

              <div className="grid grid-cols-1 gap-4">
                <div>
                  <label className="text-zinc-500 block mb-1">NOMINAL CASH KELUAR (RP) *</label>
                  <input 
                    type="number" 
                    required
                    placeholder="120000"
                    value={total}
                    onChange={(e) => setTotal(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 text-zinc-200 focus:outline-none"
                  />
                </div>
              </div>

              <div>
                <label className="text-zinc-500 block mb-1">KETERANGAN / NOTES</label>
                <textarea 
                  placeholder="Contoh: Kulakan biji kopi arabika 5kg & robusta 5kg"
                  value={notes}
                  onChange={(e) => setNotes(e.target.value)}
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3.5 h-20 text-zinc-200 focus:outline-none"
                />
              </div>

              <div className="pt-2 flex gap-3">
                <button 
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="w-1/2 border border-zinc-800 text-zinc-400 py-3 rounded-xl hover:bg-zinc-850 hover:text-white transition-colors font-bold"
                >
                  Batal
                </button>
                <button 
                  type="submit"
                  className="w-1/2 bg-brand text-white py-3 rounded-xl hover:bg-brand-dark shadow-lg transition-colors font-bold"
                >
                  Simpan Catatan
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
