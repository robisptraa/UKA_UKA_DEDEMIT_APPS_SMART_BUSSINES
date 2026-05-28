"use client";

import React, { useState } from "react";
import { 
  Users, 
  Search, 
  Download, 
  Eye, 
  Check, 
  X, 
  Phone, 
  MapPin, 
  Calendar,
  DollarSign,
  ShoppingBag,
  Clock,
  Sparkles
} from "lucide-react";
import { toast } from "react-hot-toast";

interface Customer {
  id: string;
  name: string;
  phone: string;
  email: string;
  address: string;
  totalOrders: number;
  totalSpend: number;
  lastOrderDate: string;
  notes: string;
}

export default function CustomersPage() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCustomer, setSelectedCustomer] = useState<Customer | null>(null);

  // Mock CRM data — berbagai pelanggan UMKM
  const [customers] = useState<Customer[]>([
    { id: "CUST-001", name: "Sari Rahayu", phone: "081299998888", email: "sari.rahayu@gmail.com", address: "Jl. Mampang Prapatan No. 5, Jakarta", totalOrders: 14, totalSpend: 540000, lastOrderDate: "2026-05-28", notes: "Pelanggan setia warung nasi & kopi aren. Suka kopi manis." },
    { id: "CUST-002", name: "Dian Kusuma", phone: "089876543210", email: "dian.k@gmail.com", address: "Pasar Atom Blok B No. 34, Surabaya", totalOrders: 6, totalSpend: 1110000, lastOrderDate: "2026-05-28", notes: "Sering beli kaos oversized & batik fashion." },
    { id: "CUST-003", name: "Nurul Fadilah", phone: "087711112222", email: "nurul.beauty@yahoo.com", address: "Jl. Setia Budi No. 12, Medan", totalOrders: 4, totalSpend: 950000, lastOrderDate: "2026-05-15", notes: "Pelanggan salon kecantikan, suka creambath herbal." },
    { id: "CUST-004", name: "Budi Santoso", phone: "081322223333", email: "budi.s@outlook.com", address: "Jl. Sudirman No. 45, Semarang", totalOrders: 1, totalSpend: 45000, lastOrderDate: "2026-05-27", notes: "Baru terdaftar dari layanan laundry dry-cleaning." },
    { id: "CUST-005", name: "Ahmad Fauzi", phone: "085699990000", email: "ahmad.bengkel@gmail.com", address: "Jl. Ahmad Yani No. 20, Yogyakarta", totalOrders: 3, totalSpend: 375000, lastOrderDate: "2026-04-12", notes: "Pelanggan bengkel motor, ganti oli rutin." },
    { id: "CUST-006", name: "Hendra Wijaya", phone: "081988887777", email: "hendra.w@gmail.com", address: "Jl. Gatot Subroto No. 7, Bandung", totalOrders: 8, totalSpend: 2240000, lastOrderDate: "2026-03-10", notes: "Pelanggan loyal grosir sembako, pasif akhir-akhir ini." },
  ]);

  const filteredCustomers = customers.filter(c => 
    c.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
    c.phone.includes(searchQuery)
  );

  // CRM Segment Tag Generator
  const getCustomerTag = (c: Customer) => {
    // Loyal: orders > 5
    // Pasif / Tidak Aktif: last order > 30 days ago (relative to today 28 Mei 2026)
    // Baru: orders <= 1
    const lastDate = new Date(c.lastOrderDate);
    const today = new Date("2026-05-28");
    const diffDays = Math.ceil((today.getTime() - lastDate.getTime()) / (1000 * 60 * 60 * 24));
    
    if (c.totalOrders > 5 && diffDays <= 30) {
      return { label: "🔥 Loyal", color: "bg-brand/10 text-brand border border-brand/20" };
    } else if (diffDays > 30) {
      return { label: "😴 Tidak Aktif", color: "bg-red-500/10 text-red-400 border border-red-500/20" };
    } else if (c.totalOrders <= 1) {
      return { label: "🆕 Baru", color: "bg-teal-500/10 text-teal-400 border border-teal-500/20" };
    } else {
      return { label: "👍 Reguler", color: "bg-zinc-800 text-zinc-400" };
    }
  };

  const handleExportCSV = () => {
    toast.loading("Mengekspor data kontak CRM ke CSV...", { id: "export" });
    setTimeout(() => {
      toast.dismiss("export");
      toast.success("Sukses mengunduh dedemit_crm_contacts.csv! 👥📄", {
        style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
      });
    }, 1200);
  };

  return (
    <div className="space-y-8 font-mono text-xs">
      {/* HEADER CRM */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2 font-sans">
            CRM & Manajemen Pelanggan <span className="animate-pulse">👥</span>
          </h2>
          <p className="text-[10px] text-zinc-500">Kenali pelanggan setia Anda secara instan. Bot Telegram otomatis mendata pembeli baru ke basis data ini.</p>
        </div>

        <div>
          <button 
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 px-4 py-2.5 rounded-xl border border-zinc-800 hover:border-zinc-700 bg-zinc-900 text-zinc-300 hover:text-white transition-all font-bold"
          >
            <Download className="w-3.5 h-3.5" /> Export Kontak CSV
          </button>
        </div>
      </header>

      {/* ================= SEARCH & CONTROLS ================= */}
      <section className="max-w-md relative">
        <span className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-zinc-500">
          <Search className="w-3.5 h-3.5" />
        </span>
        <input 
          type="text" 
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Cari nama atau nomor HP pelanggan..."
          className="w-full bg-zinc-900 border border-zinc-800 rounded-xl py-2.5 pl-9 pr-3 text-zinc-200 focus:outline-none focus:border-brand-light transition-all"
        />
      </section>

      {/* ================= DATATABLE ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="border-b border-zinc-800 text-zinc-500 uppercase tracking-wider">
                <th className="py-4">ID PELANGGAN</th>
                <th className="py-4">NAMA LENGKAP</th>
                <th className="py-4">KONTAK HP</th>
                <th className="py-4 text-right">TOTAL ORDER</th>
                <th className="py-4 text-right">TOTAL BELANJA</th>
                <th className="py-4">ORDER TERAKHIR</th>
                <th className="py-4 pl-4">SEGMENTASI</th>
                <th className="py-4 text-center">AKSI</th>
              </tr>
            </thead>
            <tbody>
              {filteredCustomers.length === 0 ? (
                <tr>
                  <td colSpan={8} className="py-8 text-center text-zinc-500">Tidak ada data pelanggan ditemukan.</td>
                </tr>
              ) : (
                filteredCustomers.map((c) => {
                  const tag = getCustomerTag(c);
                  return (
                    <tr key={c.id} className="border-b border-zinc-800/50 hover:bg-zinc-950/40 transition-colors">
                      <td className="py-4 text-zinc-500 font-bold">{c.id}</td>
                      <td className="py-4 text-white font-bold">{c.name}</td>
                      <td className="py-4 text-zinc-400 font-bold">{c.phone}</td>
                      <td className="py-4 text-right text-zinc-350 pr-4">{c.totalOrders} Transaksi</td>
                      <td className="py-4 text-right text-brand-ghost font-bold pr-2">Rp {c.totalSpend.toLocaleString("id-ID")}</td>
                      <td className="py-4 text-zinc-450">{c.lastOrderDate}</td>
                      <td className="py-4 pl-4">
                        <span className={`px-2 py-0.5 rounded text-[8px] font-extrabold uppercase ${tag.color}`}>
                          {tag.label}
                        </span>
                      </td>
                      <td className="py-4 text-center">
                        <button 
                          onClick={() => setSelectedCustomer(c)}
                          className="px-2 py-1 bg-zinc-950 hover:bg-zinc-800 border border-zinc-800 rounded-lg text-brand-ghost transition-colors inline-flex items-center gap-1 font-bold animate-fade-in"
                        >
                          <Eye className="w-3 h-3" /> Detail
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* ================= MODAL DETAIL CRM OVERLAY ================= */}
      {selectedCustomer && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 animate-fade-in">
          <div className="fixed inset-0 bg-black/75 backdrop-blur-sm" onClick={() => setSelectedCustomer(null)} />
          
          <div className="w-full max-w-xl bg-zinc-900 border border-zinc-800 rounded-3xl p-6 relative z-50 text-xs font-mono">
            <div className="flex justify-between items-center pb-4 border-b border-zinc-800 mb-5">
              <h3 className="text-sm font-bold text-white uppercase tracking-wider flex items-center gap-1.5 font-sans">
                <Users className="w-4 h-4 text-brand-ghost" /> Profil Pelanggan {selectedCustomer.id}
              </h3>
              <button 
                onClick={() => setSelectedCustomer(null)}
                className="p-1 rounded-lg text-zinc-500 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Left side: Profile Info */}
              <div className="space-y-4">
                <div className="space-y-1">
                  <span className="text-[9px] text-zinc-500 block uppercase font-bold">Nama Lengkap</span>
                  <div className="text-white font-bold text-sm font-sans">{selectedCustomer.name}</div>
                </div>

                <div className="space-y-1">
                  <span className="text-[9px] text-zinc-500 block uppercase font-bold">Hubungi Kontak</span>
                  <div className="text-zinc-300 font-bold flex items-center gap-1">
                    <Phone className="w-3.5 h-3.5 text-zinc-500" /> {selectedCustomer.phone}
                  </div>
                </div>

                <div className="space-y-1">
                  <span className="text-[9px] text-zinc-500 block uppercase font-bold">Email</span>
                  <div className="text-zinc-300">{selectedCustomer.email}</div>
                </div>

                <div className="space-y-1">
                  <span className="text-[9px] text-zinc-500 block uppercase font-bold">Alamat Pengiriman</span>
                  <div className="text-zinc-400 flex items-start gap-1 leading-normal">
                    <MapPin className="w-3.5 h-3.5 text-zinc-500 mt-0.5 flex-shrink-0" /> {selectedCustomer.address}
                  </div>
                </div>
              </div>

              {/* Right side: Lifetime Stats */}
              <div className="bg-zinc-950 border border-zinc-800 rounded-2xl p-4 flex flex-col justify-between gap-4">
                <div className="space-y-3">
                  <span className="text-[9px] text-zinc-500 block uppercase font-bold">Statistik Seumur Hidup (Lifetime Value)</span>
                  
                  <div className="grid grid-cols-2 gap-3">
                    <div className="p-2.5 bg-zinc-900 border border-zinc-800 rounded-xl">
                      <span className="text-zinc-500 text-[8px] block mb-0.5">FREKUENSI</span>
                      <span className="text-white font-bold text-xs flex items-center gap-1"><ShoppingBag className="w-3 h-3 text-brand" /> {selectedCustomer.totalOrders} Order</span>
                    </div>
                    
                    <div className="p-2.5 bg-zinc-900 border border-zinc-800 rounded-xl">
                      <span className="text-zinc-500 text-[8px] block mb-0.5">LTV SPENDING</span>
                      <span className="text-brand-ghost font-bold text-xs flex items-center gap-0.5">Rp {selectedCustomer.totalSpend.toLocaleString()}</span>
                    </div>
                  </div>
                  
                  <div className="p-2.5 bg-zinc-900 border border-zinc-800 rounded-xl flex items-center justify-between text-[9px]">
                    <span className="text-zinc-500">TRANSAKSI TERAKHIR:</span>
                    <span className="text-zinc-300 font-bold flex items-center gap-1"><Clock className="w-3 h-3 text-zinc-500" /> {selectedCustomer.lastOrderDate}</span>
                  </div>
                </div>

                <div className="p-3 bg-brand/5 border border-brand/20 rounded-xl">
                  <span className="text-[8px] text-brand font-bold uppercase block mb-1">Catatan Bisnis (Notes)</span>
                  <p className="text-[10px] text-zinc-300 leading-normal">{selectedCustomer.notes}</p>
                </div>
              </div>
            </div>

            <div className="pt-5 border-t border-zinc-800 mt-5 flex justify-end">
              <button 
                onClick={() => setSelectedCustomer(null)}
                className="px-6 py-2.5 border border-zinc-800 text-zinc-400 hover:text-white hover:bg-zinc-800 rounded-xl font-bold transition-all"
              >
                Tutup Profil
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
