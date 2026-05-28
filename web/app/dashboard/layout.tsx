"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Package, 
  ShoppingBag, 
  TrendingUp, 
  Menu, 
  X, 
  Bell, 
  LogOut, 
  Sun, 
  Moon, 
  Bot,
  Store,
  Users,
  Wallet,
  Settings as SettingsIcon
} from "lucide-react";
import { Toaster, toast } from "react-hot-toast";

interface SidebarLink {
  label: string;
  path: string;
  icon: React.ComponentType<any>;
  desc: string;
}

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const pathname = usePathname();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(true);
  const [notifications, setNotifications] = useState<string[]>([
    "Order baru #ORD-901 masuk via Telegram Bot! 🛒",
    "Pembayaran QRIS lunas #ORD-900 dari Sari R. ✅",
    "Stok Baju Batik Solo hampir habis (2 pcs) ⚠️",
  ]);
  const [unreadNotifications, setUnreadNotifications] = useState(3);
  const [showNotificationsDropdown, setShowNotificationsDropdown] = useState(false);

  const sidebarLinks: SidebarLink[] = [
    { label: "Overview", path: "/dashboard", icon: LayoutDashboard, desc: "Ringkasan bisnis" },
    { label: "Katalog Inventori", path: "/dashboard/inventory", icon: Package, desc: "Kelola produk & jasa" },
    { label: "Manajemen Order", path: "/dashboard/orders", icon: ShoppingBag, desc: "Pantau transaksi" },
    { label: "CRM Pelanggan", path: "/dashboard/customers", icon: Users, desc: "Manajemen pelanggan" },
    { label: "Laporan Keuangan", path: "/dashboard/finance", icon: Wallet, desc: "Arus kas & pengeluaran" },
    { label: "Analitik & AI", path: "/dashboard/analytics", icon: TrendingUp, desc: "Insight & ramalan stok" },
    { label: "Pengaturan Toko", path: "/dashboard/settings", icon: SettingsIcon, desc: "Integrasi bot & payment" },
  ];

  // Simulasi real-time polling notification setiap 30 detik
  useEffect(() => {
    const interval = setInterval(() => {
      const simulatedNotifs = [
        "🛒 Order baru #ORD-904 Cuci Motor Honda Beat masuk via Bot!",
        "✅ Pembayaran GoPay lunas #ORD-901 dari Sari R.!",
        "⚠️ Stok Beras Premium tinggal 2 kantong — segera restock!",
        "🛒 Order baru #ORD-905 Potong Rambut Salon kecantikan masuk!",
        "✅ QRIS terkonfirmasi #ORD-900 Rp 185,000 dari Dian K.",
        "⚠️ Stok Detergen Laundry hampir habis (< 3 botol)!",
      ];
      const randomNotif = simulatedNotifs[Math.floor(Math.random() * simulatedNotifs.length)];
      
      setNotifications(prev => [randomNotif, ...prev]);
      setUnreadNotifications(prev => prev + 1);
      
      toast.success(randomNotif, {
        icon: "👻",
        style: {
          borderRadius: "16px",
          background: "#18181B",
          color: "#fff",
          border: "1px solid #27272A",
          fontSize: "12px",
          fontFamily: "var(--font-outfit)"
        },
      });
    }, 30000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`${darkMode ? "dark" : ""} bg-zinc-950 text-zinc-100 min-h-screen font-sans flex overflow-hidden`}>
      <Toaster position="top-right" />

      {/* ================= SIDEBAR NAVIGATION ================= */}
      {sidebarOpen && (
        <div 
          onClick={() => setSidebarOpen(false)}
          className="fixed inset-0 z-40 bg-black/60 md:hidden backdrop-blur-sm"
        />
      )}

      <aside className={`fixed md:relative inset-y-0 left-0 z-50 w-64 bg-zinc-950 border-r border-zinc-900 flex flex-col justify-between p-5 transform ${
        sidebarOpen ? "translate-x-0" : "-translate-x-full"
      } md:translate-x-0 transition-transform duration-300 ease-in-out`}>
        
        <div>
          {/* Logo Brand */}
          <div className="flex items-center justify-between mb-6">
            <Link href="/" className="flex items-center gap-3">
              <span className="text-3xl">👻</span>
              <div>
                <h1 className="text-sm font-bold tracking-wider text-white">DEDEMIT UMKM</h1>
                <p className="text-[9px] tracking-widest text-brand-ghost uppercase font-bold">AI Business OS</p>
              </div>
            </Link>
            
            <button 
              onClick={() => setSidebarOpen(false)}
              className="md:hidden p-1 text-zinc-400 hover:text-white"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
 
          {/* Navigation Links */}
          <nav className="space-y-1">
            {sidebarLinks.map((link) => {
              const Icon = link.icon;
              const isActive = pathname === link.path;
              return (
                <Link
                  key={link.path}
                  href={link.path}
                  onClick={() => setSidebarOpen(false)}
                  className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-[11px] font-semibold tracking-wide transition-all ${
                    isActive
                      ? "bg-brand/10 border-l-4 border-brand text-white font-bold"
                      : "text-zinc-400 hover:text-white hover:bg-zinc-900/50"
                  }`}
                >
                  <Icon className="w-4 h-4 flex-shrink-0" />
                  <div className="truncate">
                    <div>{link.label}</div>
                    {isActive && <div className="text-[8px] text-brand font-normal opacity-85">{link.desc}</div>}
                  </div>
                </Link>
              );
            })}
          </nav>
 
          {/* Bot status indicator */}
          <div className="mt-4 p-3 rounded-xl bg-zinc-900 border border-zinc-800 text-[10px]">
            <div className="flex items-center gap-1.5 mb-1">
              <span className="w-2 h-2 rounded-full bg-brand animate-pulse" />
              <span className="font-bold text-white">Bot Telegram</span>
            </div>
            <p className="text-[9px] text-zinc-500 leading-tight">Aktif & terima order 24/7 otomatis.</p>
          </div>
        </div>

        {/* User profile & logout */}
        <div className="border-t border-zinc-900 pt-4 space-y-3">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-full bg-gradient-to-tr from-brand to-brand-ghost flex items-center justify-center font-bold text-white shadow-lg text-sm flex-shrink-0">
              <Store className="w-4 h-4" />
            </div>
            <div className="truncate">
              <h4 className="text-xs font-bold text-white truncate">Dedemit Coffee & Goods</h4>
              <p className="text-[9px] text-zinc-500 font-mono">Owner · Paket Pro</p>
            </div>
          </div>

          <Link href="/" className="w-full flex items-center gap-2.5 px-3 py-2 rounded-lg text-[10px] font-bold text-red-400 hover:bg-red-500/10 hover:text-red-300 transition-colors">
            <LogOut className="w-4 h-4" />
            Keluar Dashboard
          </Link>
        </div>
      </aside>

      {/* ================= MAIN CONTENT CONTAINER ================= */}
      <div className="flex-1 flex flex-col overflow-hidden">
        
        {/* ================= TOP HEADER BAR ================= */}
        <header className="h-20 border-b border-zinc-900 px-6 flex items-center justify-between bg-zinc-950/80 backdrop-blur-md sticky top-0 z-30">
          
          <div className="flex items-center gap-4">
            <button 
              onClick={() => setSidebarOpen(true)}
              className="md:hidden p-2 text-zinc-400 hover:text-white bg-zinc-900 rounded-xl"
            >
              <Menu className="w-5 h-5" />
            </button>
            
            <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full bg-brand/10 border border-brand/20 text-brand-light text-[10px] font-bold tracking-wider animate-pulse">
              <Bot className="w-3.5 h-3.5" /> GEMINI AI · AKTIF
            </div>
          </div>

          <div className="flex items-center gap-4">
            {/* Dark Mode toggle */}
            <button 
              onClick={() => setDarkMode(!darkMode)}
              className="p-2.5 rounded-xl bg-zinc-900 text-zinc-400 hover:text-white border border-zinc-800 transition-all"
            >
              {darkMode ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
            </button>

            {/* Notification bell dropdown */}
            <div className="relative">
              <button 
                onClick={() => {
                  setShowNotificationsDropdown(!showNotificationsDropdown);
                  setUnreadNotifications(0);
                }}
                className="p-2.5 rounded-xl bg-zinc-900 text-zinc-400 hover:text-white border border-zinc-800 relative transition-all"
              >
                <Bell className="w-4 h-4" />
                {unreadNotifications > 0 && (
                  <span className="absolute -top-1 -right-1 w-5 h-5 bg-brand rounded-full text-[9px] font-extrabold text-white flex items-center justify-center border border-zinc-950 font-mono animate-bounce">
                    {unreadNotifications > 9 ? "9+" : unreadNotifications}
                  </span>
                )}
              </button>

              {showNotificationsDropdown && (
                <>
                  <div className="fixed inset-0 z-40" onClick={() => setShowNotificationsDropdown(false)} />
                  <div className="absolute right-0 mt-3 w-80 bg-zinc-900 border border-zinc-800 rounded-2xl shadow-2xl p-4 z-50 text-xs font-mono space-y-3">
                    <div className="flex justify-between items-center pb-2 border-b border-zinc-800">
                      <span className="font-bold text-white uppercase tracking-wider">Notifikasi Bisnis</span>
                      <button className="text-[10px] text-zinc-500 hover:text-white" onClick={() => setNotifications([])}>Hapus Semua</button>
                    </div>
                    
                    <div className="max-h-60 overflow-y-auto space-y-2.5">
                      {notifications.length === 0 ? (
                        <p className="text-zinc-500 text-center py-4">Belum ada notifikasi baru.</p>
                      ) : (
                        notifications.map((notif, index) => (
                          <div key={index} className="p-2.5 bg-zinc-950 border border-zinc-800 rounded-xl flex items-start gap-2.5">
                            <span className="text-brand">⚡</span>
                            <span className="text-zinc-300 leading-normal text-[10px]">{notif}</span>
                          </div>
                        ))
                      )}
                    </div>
                  </div>
                </>
              )}
            </div>

            {/* Admin Mini Profile */}
            <div className="flex items-center gap-2.5 pl-2 border-l border-zinc-900">
              <div className="w-8 h-8 rounded-full bg-brand/20 border border-brand/40 flex items-center justify-center font-bold text-brand text-xs">
                👻
              </div>
              <span className="hidden lg:inline text-xs font-bold text-zinc-300 font-mono">Owner</span>
            </div>
          </div>
        </header>

        {/* ================= PAGE CONTAINER CONTENT ================= */}
        <main className="flex-1 overflow-y-auto p-6 md:p-8 bg-zinc-950 bg-ghost-glow bg-no-repeat bg-contain">
          {children}
        </main>
      </div>
    </div>
  );
}
