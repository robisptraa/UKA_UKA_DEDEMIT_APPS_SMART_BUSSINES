"use client";

import React, { useState } from "react";
import { 
  Settings, 
  Store, 
  Bot, 
  CreditCard, 
  Bell, 
  ShieldAlert, 
  Save, 
  Trash2, 
  Upload,
  Lock,
  Check
} from "lucide-react";
import { toast } from "react-hot-toast";

export default function SettingsPage() {
  // 1. Store Info States
  const [storeName, setStoreName] = useState("Dedemit Coffee & Goods");
  const [businessType, setBusinessType] = useState("kafe");
  const [city, setCity] = useState("Bandung");
  const [logoUrl, setLogoUrl] = useState("https://images.unsplash.com/photo-1541167760496-1628856ab772?w=100&q=80");
  const [openHours, setOpenHours] = useState("09:00 - 22:00");
  const [location, setLocation] = useState("Jl. Dago No. 102, Bandung Jawa Barat");

  // 2. Telegram Bot Config States
  const [botToken, setBotToken] = useState("7182930411:AAHgFD82jKLskw918js9AHSk2j1");
  const [chatId, setChatId] = useState("1029384756");
  const [botActive, setBotActive] = useState(true);

  // 3. Payment Gateway Config States
  const [midtransServerKey, setMidtransServerKey] = useState("SB-Mid-server-8a9dF23JKla90S");
  const [midtransClientKey, setMidtransClientKey] = useState("SB-Mid-client-2j8A9dLlaJK91a");
  const [payQris, setPayQris] = useState(true);
  const [payGoPay, setPayGoPay] = useState(true);
  const [payOVO, setPayOVO] = useState(true);
  const [payBcaVa, setPayBcaVa] = useState(true);

  // 4. Notifications States
  const [stockThreshold, setStockThreshold] = useState("5");
  const [dailySummaryTime, setDailySummaryTime] = useState("21:00");

  // 5. Account Security
  const [oldPassword, setOldPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");

  const handleSaveSettings = (e: React.FormEvent, section: string) => {
    e.preventDefault();
    toast.success(`Pengaturan ${section} berhasil diperbarui! 👻💾`, {
      style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
    });
  };

  const handleDeleteAccount = () => {
    const confirm = window.confirm("PERINGATAN: Apakah Anda yakin ingin menghapus akun toko Anda secara permanen? Data kasir, CRM, dan inventori akan dihapus dan tidak bisa dikembalikan.");
    if (confirm) {
      toast.error("Akun berhasil dihapus. Menghubungi pusat...", {
        style: { borderRadius: "12px", background: "#18181B", color: "#fff" }
      });
    }
  };

  return (
    <div className="space-y-8 font-mono text-xs max-w-4xl">
      
      {/* HEADER SETTINGS */}
      <header className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h2 className="text-xl font-bold tracking-tight text-white flex items-center gap-2 font-sans">
            Konfigurasi & Pengaturan OS <span className="animate-pulse">⚙️</span>
          </h2>
          <p className="text-[10px] text-zinc-500">Kelola profil wirausaha, sambungkan token API bot Telegram pelanggan, aktifkan kunci pembayaran Midtrans, dan kelola akun.</p>
        </div>
      </header>

      {/* ================= SECTION 1: PROFIL USAHA ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 space-y-6">
        <div className="flex items-center gap-2 pb-3 border-b border-zinc-800">
          <Store className="w-5 h-5 text-brand" />
          <h3 className="text-sm font-bold text-white font-sans">1. Informasi Toko & Profil Usaha</h3>
        </div>

        <form onSubmit={(e) => handleSaveSettings(e, "Profil Usaha")} className="space-y-4">
          <div className="flex flex-col md:flex-row gap-6 items-center">
            {/* Logo simulation */}
            <div className="space-y-2 text-center">
              <span className="text-[9px] text-zinc-500 block uppercase">Logo Toko</span>
              <div className="w-16 h-16 rounded-full overflow-hidden border-2 border-brand bg-zinc-950 relative flex items-center justify-center group">
                <img src={logoUrl} alt="Store Logo" className="w-full h-full object-cover" />
                <button 
                  type="button"
                  onClick={() => toast.success("Simulasi upload logo berhasil!")}
                  className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center text-white"
                >
                  <Upload className="w-4 h-4" />
                </button>
              </div>
            </div>

            <div className="flex-1 grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
              <div>
                <label className="text-zinc-500 block mb-1">NAMA TOKO / UMKM *</label>
                <input 
                  type="text" 
                  value={storeName} 
                  onChange={(e) => setStoreName(e.target.value)} 
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-200 focus:outline-none"
                />
              </div>
              <div>
                <label className="text-zinc-500 block mb-1">SEKTOR USAHA</label>
                <select 
                  value={businessType} 
                  onChange={(e) => setBusinessType(e.target.value)} 
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-300 focus:outline-none"
                >
                  <option value="kafe">🍜 Kafe & Kuliner</option>
                  <option value="fashion">👗 Toko Baju & Fashion</option>
                  <option value="salon">💇‍♀️ Salon Kecantikan</option>
                  <option value="laundry">🧺 Jasa Laundry</option>
                  <option value="toko">🛒 Toko Kelontong & Sembako</option>
                  <option value="bengkel">🔧 Bengkel Otomotif</option>
                </select>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="text-zinc-500 block mb-1">LOKASI KOTA *</label>
              <input 
                type="text" 
                value={city} 
                onChange={(e) => setCity(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-200 focus:outline-none"
              />
            </div>
            <div>
              <label className="text-zinc-500 block mb-1">JAM OPERASIONAL *</label>
              <input 
                type="text" 
                value={openHours} 
                onChange={(e) => setOpenHours(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-200 focus:outline-none"
              />
            </div>
            <div className="md:col-span-1">
              <label className="text-zinc-500 block mb-1">ALAMAT DETAIL LOKASI</label>
              <input 
                type="text" 
                value={location} 
                onChange={(e) => setLocation(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-200 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button 
              type="submit" 
              className="flex items-center gap-1.5 px-4 py-2.5 bg-brand hover:bg-brand-dark text-white rounded-xl font-bold font-sans text-xs"
            >
              <Save className="w-3.5 h-3.5" /> Simpan Profil
            </button>
          </div>
        </form>
      </section>

      {/* ================= SECTION 2: TELEGRAM BOT INTEGRASI ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 space-y-6">
        <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
          <div className="flex items-center gap-2">
            <Bot className="w-5 h-5 text-brand-ghost" />
            <h3 className="text-sm font-bold text-white font-sans">2. Otomatisasi Bot Telegram Pelanggan</h3>
          </div>
          
          <button 
            type="button" 
            onClick={() => setBotActive(!botActive)}
            className={`px-3 py-1 rounded-full text-[9px] font-extrabold uppercase font-mono border ${
              botActive 
                ? "bg-brand/10 text-brand border-brand/20" 
                : "bg-zinc-800 text-zinc-500 border-zinc-900"
            }`}
          >
            {botActive ? "AKTIF ✓" : "NONAKTIF ✕"}
          </button>
        </div>

        <form onSubmit={(e) => handleSaveSettings(e, "Integrasi Bot Telegram")} className="space-y-4">
          <p className="text-[10px] text-zinc-500 leading-normal">
            Gunakan BotFather di Telegram untuk membuat bot baru, lalu rekatkan token bot Anda di bawah agar pelanggan Anda bisa langsung memesan barang/jasa via Telegram secara otomatis.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-zinc-500 block mb-1">API TOKEN BOT TELEGRAM *</label>
              <input 
                type="text" 
                value={botToken} 
                onChange={(e) => setBotToken(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
              />
            </div>
            <div>
              <label className="text-zinc-500 block mb-1">CHAT ID NOTIFIKASI OWNER *</label>
              <input 
                type="text" 
                value={chatId} 
                onChange={(e) => setChatId(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button 
              type="submit" 
              className="flex items-center gap-1.5 px-4 py-2.5 bg-brand hover:bg-brand-dark text-white rounded-xl font-bold font-sans text-xs"
            >
              <Save className="w-3.5 h-3.5" /> Hubungkan Bot
            </button>
          </div>
        </form>
      </section>

      {/* ================= SECTION 3: MIDTRANS SNAP KREDENSIAL ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 space-y-6">
        <div className="flex items-center gap-2 pb-3 border-b border-zinc-800">
          <CreditCard className="w-5 h-5 text-teal-400" />
          <h3 className="text-sm font-bold text-white font-sans">3. Payment Gateway Midtrans Indonesia</h3>
        </div>

        <form onSubmit={(e) => handleSaveSettings(e, "Gerbang Pembayaran")} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-zinc-500 block mb-1">MIDTRANS SERVER KEY *</label>
              <input 
                type="text" 
                value={midtransServerKey} 
                onChange={(e) => setMidtransServerKey(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
              />
            </div>
            <div>
              <label className="text-zinc-500 block mb-1">MIDTRANS CLIENT KEY *</label>
              <input 
                type="text" 
                value={midtransClientKey} 
                onChange={(e) => setMidtransClientKey(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-300 focus:outline-none"
              />
            </div>
          </div>

          <div className="space-y-2">
            <label className="text-zinc-500 block">METODE PEMBAYARAN DI-AKTIFKAN:</label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { label: "QRIS Tagihan", state: payQris, setter: setPayQris },
                { label: "GoPay Wallet", state: payGoPay, setter: setPayGoPay },
                { label: "OVO Wallet", state: payOVO, setter: setPayOVO },
                { label: "BCA Virtual Account", state: payBcaVa, setter: setPayBcaVa },
              ].map((method, idx) => (
                <div 
                  key={idx} 
                  onClick={() => method.setter(!method.state)}
                  className={`p-3 border rounded-xl flex items-center justify-between cursor-pointer transition-colors ${
                    method.state 
                      ? "border-brand/40 bg-brand/5 text-white font-bold" 
                      : "border-zinc-800 bg-zinc-950/40 text-zinc-500"
                  }`}
                >
                  <span>{method.label}</span>
                  {method.state && <Check className="w-3.5 h-3.5 text-brand" />}
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-end">
            <button 
              type="submit" 
              className="flex items-center gap-1.5 px-4 py-2.5 bg-brand hover:bg-brand-dark text-white rounded-xl font-bold font-sans text-xs"
            >
              <Save className="w-3.5 h-3.5" /> Aktifkan Midtrans
            </button>
          </div>
        </form>
      </section>

      {/* ================= SECTION 4: NOTIFICATIONS THRESHOLD ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-zinc-800 space-y-6">
        <div className="flex items-center gap-2 pb-3 border-b border-zinc-800">
          <Bell className="w-5 h-5 text-purple-400" />
          <h3 className="text-sm font-bold text-white font-sans">4. Ambang Batas Notifikasi Kritis</h3>
        </div>

        <form onSubmit={(e) => handleSaveSettings(e, "Notifikasi Ambang")} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-zinc-500 block mb-1">AMBANG KRITIS ALARM STOK BAHAN BAKU *</label>
              <div className="flex gap-2">
                <input 
                  type="number" 
                  value={stockThreshold} 
                  onChange={(e) => setStockThreshold(e.target.value)} 
                  className="w-2/3 bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 px-3 text-zinc-350 focus:outline-none"
                />
                <span className="w-1/3 bg-zinc-950 border border-zinc-800 rounded-xl py-2.5 flex items-center justify-center text-zinc-500 font-bold">Pcs Sisa</span>
              </div>
            </div>
            <div>
              <label className="text-zinc-500 block mb-1">JAM SUMMARY LAPORAN HARIAN BOT TELEGRAM *</label>
              <input 
                type="time" 
                value={dailySummaryTime} 
                onChange={(e) => setDailySummaryTime(e.target.value)} 
                className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-300 focus:outline-none text-center"
              />
            </div>
          </div>

          <div className="flex justify-end">
            <button 
              type="submit" 
              className="flex items-center gap-1.5 px-4 py-2.5 bg-brand hover:bg-brand-dark text-white rounded-xl font-bold font-sans text-xs"
            >
              <Save className="w-3.5 h-3.5" /> Simpan Konfigurasi
            </button>
          </div>
        </form>
      </section>

      {/* ================= SECTION 5: SECURITY & AKUN ================= */}
      <section className="p-6 rounded-3xl bg-zinc-900 border border-red-500/20 space-y-6">
        <div className="flex items-center gap-2 pb-3 border-b border-zinc-800">
          <ShieldAlert className="w-5 h-5 text-red-500" />
          <h3 className="text-sm font-bold text-white font-sans">5. Keamanan Akun & Zona Bahaya</h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 items-start">
          {/* Change password */}
          <form onSubmit={(e) => handleSaveSettings(e, "Kata Sandi")} className="space-y-4">
            <span className="text-[9px] text-zinc-500 block uppercase font-bold">Ganti Password Keamanan</span>
            
            <div className="space-y-3">
              <div>
                <label className="text-zinc-500 block mb-1">PASSWORD LAMA</label>
                <input 
                  type="password" 
                  value={oldPassword} 
                  onChange={(e) => setOldPassword(e.target.value)} 
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-300 focus:outline-none"
                />
              </div>
              <div>
                <label className="text-zinc-500 block mb-1">PASSWORD BARU</label>
                <input 
                  type="password" 
                  value={newPassword} 
                  onChange={(e) => setNewPassword(e.target.value)} 
                  className="w-full bg-zinc-950 border border-zinc-800 rounded-xl py-2 px-3 text-zinc-300 focus:outline-none"
                />
              </div>
            </div>

            <div className="flex justify-end">
              <button 
                type="submit" 
                className="flex items-center gap-1.5 px-4 py-2.5 bg-brand hover:bg-brand-dark text-white rounded-xl font-bold font-sans text-xs"
              >
                <Lock className="w-3.5 h-3.5" /> Ganti Password
              </button>
            </div>
          </form>

          {/* Danger zone delete */}
          <div className="space-y-4 bg-red-500/5 p-5 border border-red-500/20 rounded-2xl">
            <span className="text-[9px] text-red-400 block uppercase font-bold">ZONA BERBAHAYA (DANGER ZONE)</span>
            <p className="text-[10px] text-zinc-400 leading-normal">
              Penghapusan akun bersifat permanen. Seluruh data transaksi, basis pelanggan CRM, dan data stok inventori Anda akan terhapus selamanya dari sistem utama Dedemit UMKM.
            </p>
            
            <button 
              type="button" 
              onClick={handleDeleteAccount}
              className="flex items-center justify-center gap-1.5 w-full py-3 bg-red-500 text-white font-bold rounded-xl hover:bg-red-600 transition-all font-sans text-xs"
            >
              <Trash2 className="w-4 h-4" /> Hapus Akun Toko Permanen
            </button>
          </div>
        </div>
      </section>

    </div>
  );
}
