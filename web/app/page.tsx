"use client";

import React, { useState } from "react";
import Link from "next/link";
import { 
  Sparkles, 
  TrendingUp, 
  Package, 
  CreditCard, 
  MessageSquare, 
  ArrowRight, 
  Check, 
  HelpCircle, 
  Menu, 
  X, 
  Bot, 
  Zap, 
  ShieldCheck, 
  Smartphone,
  Star,
  Users,
  Store,
  BarChart3,
  Camera,
  Wallet,
  Clock,
  CheckCircle2
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export default function LandingPage() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [billingPeriod, setBillingPeriod] = useState<"monthly" | "annually">("monthly");
  const [activeFaq, setActiveFaq] = useState<number | null>(null);

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.15 }
    }
  } as const;

  const itemVariants = {
    hidden: { y: 30, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: { type: "spring", stiffness: 100, damping: 15 }
    }
  } as const;

  const businessTypes = [
    { emoji: "🍜", name: "Warung Makan" },
    { emoji: "👗", name: "Toko Fashion" },
    { emoji: "💄", name: "Salon & Beauty" },
    { emoji: "🧺", name: "Laundry" },
    { emoji: "🛒", name: "Toko Kelontong" },
    { emoji: "🔧", name: "Bengkel" },
    { emoji: "📸", name: "Foto Studio" },
    { emoji: "🎂", name: "Bakery & Kue" },
  ];

  const faqs = [
    {
      q: "Apakah Dedemit UMKM cocok untuk semua jenis usaha?",
      a: "Ya! Platform kami dirancang universal untuk semua jenis UMKM — mulai dari warung makan, toko kelontong, salon kecantikan, laundry, toko fashion, hingga bengkel dan usaha jasa lainnya."
    },
    {
      q: "Apakah saya perlu keahlian teknis untuk menggunakannya?",
      a: "Tidak sama sekali! Cukup dengan smartphone, Anda bisa langsung pakai fitur scan produk, terima order via Telegram Bot, dan pantau omset harian. Antarmuka kami sangat mudah digunakan bahkan untuk pemula."
    },
    {
      q: "Metode pembayaran apa saja yang didukung?",
      a: "Kami mendukung QRIS, GoPay, OVO, DANA, ShopeePay, Transfer Bank, dan Kartu Kredit/Debit via integrasi Midtrans Payment Gateway."
    },
    {
      q: "Bagaimana bot Telegram bekerja untuk bisnis saya?",
      a: "Pelanggan Anda cukup chat ke bot Telegram usaha Anda, memilih produk/jasa, bot otomatis membuatkan link tagihan, dan Anda menerima notifikasi real-time saat pembayaran berhasil."
    },
  ];

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 font-sans selection:bg-brand selection:text-white relative overflow-hidden bg-streetwear-glow bg-no-repeat bg-contain">
      <div className="absolute top-[20%] right-[-10%] w-[500px] h-[500px] rounded-full bg-brand/5 blur-[120px] pointer-events-none" />
      <div className="absolute bottom-[10%] left-[-10%] w-[500px] h-[500px] rounded-full bg-brand-ghost/5 blur-[120px] pointer-events-none" />

      {/* ================= HEADER NAVBAR ================= */}
      <header className="sticky top-0 z-50 bg-zinc-950/80 backdrop-blur-md border-b border-zinc-900">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3 group">
            <span className="text-3xl transition-transform group-hover:scale-110 duration-300">👻</span>
            <div>
              <h1 className="text-xl font-bold tracking-wider text-white">DEDEMIT UMKM</h1>
              <p className="text-[9px] tracking-widest text-brand-ghost uppercase font-bold">AI Business OS</p>
            </div>
          </Link>

          {/* Desktop Nav Links */}
          <nav className="hidden md:flex items-center gap-8 text-sm font-medium text-zinc-400">
            <a href="#problem" className="hover:text-white transition-colors">Masalah</a>
            <a href="#features" className="hover:text-white transition-colors">Fitur</a>
            <a href="#how-it-works" className="hover:text-white transition-colors">Cara Kerja</a>
            <a href="#testimonials" className="hover:text-white transition-colors">Testimoni</a>
            <a href="#pricing" className="hover:text-white transition-colors">Harga</a>
          </nav>

          {/* CTAs */}
          <div className="hidden md:flex items-center gap-4">
            <Link href="/dashboard" className="text-sm font-semibold text-zinc-300 hover:text-white transition-colors">
              Lihat Demo Dashboard
            </Link>
            <Link href="#pricing" className="bg-brand hover:bg-brand-dark text-white px-5 py-2.5 rounded-xl text-sm font-bold shadow-lg hover:shadow-brand/20 transition-all flex items-center gap-1.5 group">
              Coba Gratis <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button 
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="md:hidden p-2 text-zinc-400 hover:text-white"
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Navigation Drawer */}
        <AnimatePresence>
          {mobileMenuOpen && (
            <motion.div 
              initial={{ opacity: 0, height: 0 }}
              animate={{ opacity: 1, height: "auto" }}
              exit={{ opacity: 0, height: 0 }}
              className="md:hidden bg-zinc-950 border-b border-zinc-900 overflow-hidden"
            >
              <div className="px-6 py-6 flex flex-col gap-4 text-zinc-400">
                <a href="#problem" onClick={() => setMobileMenuOpen(false)} className="hover:text-white py-2 border-b border-zinc-900">Masalah</a>
                <a href="#features" onClick={() => setMobileMenuOpen(false)} className="hover:text-white py-2 border-b border-zinc-900">Fitur</a>
                <a href="#how-it-works" onClick={() => setMobileMenuOpen(false)} className="hover:text-white py-2 border-b border-zinc-900">Cara Kerja</a>
                <a href="#testimonials" onClick={() => setMobileMenuOpen(false)} className="hover:text-white py-2 border-b border-zinc-900">Testimoni</a>
                <a href="#pricing" onClick={() => setMobileMenuOpen(false)} className="hover:text-white py-2 border-b border-zinc-900">Harga</a>
                
                <div className="pt-4 flex flex-col gap-3">
                  <Link href="/dashboard" onClick={() => setMobileMenuOpen(false)} className="text-center py-3 rounded-xl border border-zinc-800 text-zinc-300 text-sm font-semibold">
                    Lihat Demo Dashboard
                  </Link>
                  <Link href="#pricing" onClick={() => setMobileMenuOpen(false)} className="bg-brand text-white py-3 rounded-xl text-center text-sm font-bold shadow-lg">
                    Coba Gratis Sekarang
                  </Link>
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </header>

      {/* ================= SECTION 1: HERO ================= */}
      <section className="max-w-7xl mx-auto px-6 pt-16 pb-24 md:pt-24 md:pb-32 grid grid-cols-1 lg:grid-cols-12 gap-12 items-center">
        <motion.div 
          initial={{ x: -50, opacity: 0 }}
          animate={{ x: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="lg:col-span-6 space-y-6 text-center lg:text-left"
        >
          <div className="inline-flex items-center gap-2 bg-brand/10 border border-brand/35 px-4 py-1.5 rounded-full text-brand-light text-xs font-bold uppercase tracking-wider">
            <Sparkles className="w-3.5 h-3.5" /> AI Business OS #1 untuk UMKM Indonesia
          </div>
          
          <h2 className="text-4xl sm:text-5xl md:text-6xl font-extrabold tracking-tight text-white leading-[1.1]">
            Kelola Bisnis UMKM Anda <span className="text-transparent bg-clip-text bg-gradient-to-r from-brand-light to-brand-ghost">10x Lebih Cepat dengan AI</span>
          </h2>
          
          <p className="text-zinc-400 text-lg md:text-xl max-w-2xl mx-auto lg:mx-0 leading-relaxed">
            Dari scan produk otomatis via kamera, pembuatan caption promo sosmed, terima pembayaran QRIS instan via Bot Telegram — semua dalam satu platform pintar untuk <strong className="text-white">semua jenis UMKM</strong>.
          </p>

          {/* Business type ticker */}
          <div className="flex flex-wrap gap-2 justify-center lg:justify-start">
            {businessTypes.map((b, i) => (
              <span key={i} className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-zinc-900 border border-zinc-800 text-xs text-zinc-400 font-medium">
                {b.emoji} {b.name}
              </span>
            ))}
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
            <Link href="#pricing" className="w-full sm:w-auto bg-brand hover:bg-brand-dark text-white px-8 py-4 rounded-2xl text-base font-bold shadow-xl hover:shadow-brand/25 transition-all text-center">
              Mulai Sekarang (Gratis)
            </Link>
            <Link href="/dashboard" className="w-full sm:w-auto bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 text-white px-8 py-4 rounded-2xl text-base font-bold transition-all text-center flex items-center justify-center gap-2">
              Lihat Demo Dashboard <ArrowRight className="w-4 h-4" />
            </Link>
          </div>

          <div className="flex items-center justify-center lg:justify-start gap-6 pt-2 text-xs text-zinc-500 font-mono">
            <span className="flex items-center gap-1.5"><ShieldCheck className="w-4 h-4 text-brand" /> Tanpa Kartu Kredit</span>
            <span className="flex items-center gap-1.5"><Zap className="w-4 h-4 text-brand-ghost" /> Setup &lt; 5 Menit</span>
            <span className="flex items-center gap-1.5"><Users className="w-4 h-4 text-brand" /> 2.000+ UMKM Aktif</span>
          </div>
        </motion.div>

        {/* Mockup App Display */}
        <motion.div 
          initial={{ scale: 0.95, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="lg:col-span-6 relative flex justify-center"
        >
          <div className="absolute inset-0 bg-gradient-to-tr from-brand/20 to-brand-ghost/20 rounded-3xl filter blur-[40px] opacity-40 pointer-events-none" />
          
          <div className="w-full max-w-[500px] aspect-[4/3] rounded-3xl bg-zinc-900/40 border border-zinc-800 p-4 shadow-2xl relative overflow-hidden backdrop-blur-sm group hover:border-zinc-700 transition-all duration-500">
            {/* Window bar */}
            <div className="flex gap-1.5 mb-3">
              <span className="w-3 h-3 rounded-full bg-red-500/80"></span>
              <span className="w-3 h-3 rounded-full bg-yellow-500/80"></span>
              <span className="w-3 h-3 rounded-full bg-green-500/80"></span>
              <span className="text-[10px] text-zinc-500 font-mono ml-2">Dedemit UMKM Dashboard v2.0</span>
            </div>

            {/* Content mockup */}
            <div className="bg-zinc-950 rounded-2xl p-4 border border-zinc-900 h-[calc(100%-24px)] flex flex-col justify-between font-mono text-xs">
              <div className="space-y-3">
                <div className="grid grid-cols-2 gap-2">
                  <div className="bg-zinc-900/50 p-3 rounded-xl border border-zinc-800">
                    <span className="text-zinc-500 text-[9px] block mb-1">OMSET HARI INI</span>
                    <span className="text-brand font-bold text-sm">Rp 3,250,000</span>
                  </div>
                  <div className="bg-zinc-900/50 p-3 rounded-xl border border-zinc-800">
                    <span className="text-zinc-500 text-[9px] block mb-1">ORDER MASUK</span>
                    <span className="text-brand-ghost font-bold text-sm">24 Order</span>
                  </div>
                </div>

                <div className="p-3 bg-zinc-900/30 border border-zinc-800/80 rounded-xl space-y-1.5">
                  <span className="text-[9px] text-zinc-500 block">🤖 AI SCAN PRODUK:</span>
                  <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-[9px]">
                    <div>Produk: <span className="text-white font-bold">Baju Batik Solo</span></div>
                    <div>Harga AI: <span className="text-brand font-bold">Rp 185,000</span></div>
                    <div>Kategori: <span className="text-brand-ghost">Fashion</span></div>
                    <div>Akurasi: <span className="text-zinc-300">96.4%</span></div>
                  </div>
                </div>

                <div className="p-2.5 bg-brand/5 border border-brand/20 rounded-xl flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <span className="w-2 h-2 rounded-full bg-brand animate-pulse" />
                    <span className="text-[9px] text-zinc-400">Bot Telegram aktif</span>
                  </div>
                  <span className="text-[9px] text-brand font-bold uppercase">ONLINE ✓</span>
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </section>

      {/* ================= SECTION 2: PROBLEM ================= */}
      <section id="problem" className="max-w-7xl mx-auto px-6 py-20 border-t border-zinc-900">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs font-bold tracking-widest text-brand uppercase mb-3">TANTANGAN UMKM INDONESIA</h2>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-white">
            Kenapa Bisnis UMKM Anda Masih Ketinggalan?
          </h3>
          <p className="text-zinc-400 mt-4">
            Ribuan pelaku UMKM di Indonesia masih bergulat dengan masalah operasional yang sama setiap harinya. Saatnya berubah.
          </p>
        </div>

        <motion.div 
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
          className="grid grid-cols-1 md:grid-cols-3 gap-8"
        >
          <motion.div 
            variants={itemVariants}
            className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-zinc-700 transition-all flex flex-col gap-4 group"
          >
            <div className="text-4xl group-hover:scale-110 transition-transform duration-300">📋</div>
            <h4 className="text-xl font-bold text-white">Catat Stok Manual Setiap Hari</h4>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Pemilik warung, toko, atau salon masih mencatat stok di buku tulis atau tabel Excel yang berantakan. Rawan salah hitung dan sulit dilacak.
            </p>
          </motion.div>

          <motion.div 
            variants={itemVariants}
            className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-zinc-700 transition-all flex flex-col gap-4 group"
          >
            <div className="text-4xl group-hover:scale-110 transition-transform duration-300">😵</div>
            <h4 className="text-xl font-bold text-white">Bingung Buat Promo & Konten</h4>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Memikirkan caption Instagram, TikTok, dan poster promo untuk produk toko setiap hari bikin pusing dan menguras waktu berharga owner.
            </p>
          </motion.div>

          <motion.div 
            variants={itemVariants}
            className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-zinc-700 transition-all flex flex-col gap-4 group"
          >
            <div className="text-4xl group-hover:scale-110 transition-transform duration-300">🛑</div>
            <h4 className="text-xl font-bold text-white">Rawan Penipuan Bayar Manual</h4>
            <p className="text-sm text-zinc-400 leading-relaxed">
              Konfirmasi pembayaran transfer satu per satu lewat WA, screenshot palsu dari pelanggan nakal, dan belum ada notifikasi otomatis saat uang masuk.
            </p>
          </motion.div>
        </motion.div>
      </section>

      {/* ================= SECTION 3: FEATURES ================= */}
      <section id="features" className="max-w-7xl mx-auto px-6 py-20 border-t border-zinc-900">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs font-bold tracking-widest text-brand uppercase mb-3">FITUR UNGGULAN DEDEMIT UMKM</h2>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-white">
            Semua yang Dibutuhkan Bisnis Anda, Dalam Satu Platform
          </h3>
          <p className="text-zinc-400 mt-4">
            Ditenagai oleh Gemini AI dan Midtrans Payment — platform AI terlengkap khusus untuk pelaku UMKM Indonesia.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {/* Feature 1 */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-brand/40 transition-all space-y-5 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
              <Camera className="w-32 h-32 text-brand" />
            </div>
            <div className="w-12 h-12 rounded-2xl bg-brand/10 border border-brand/30 flex items-center justify-center text-brand">
              <Camera className="w-6 h-6" />
            </div>
            <h4 className="text-xl font-bold text-white">Scan AI Produk Universal</h4>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Foto produk apa pun dengan kamera HP — baju, makanan, alat, bahan baku. Gemini AI deteksi otomatis: nama produk, kategori, estimasi harga jual, dan generate caption promo siap posting ke Instagram & TikTok.
            </p>
            <div className="flex flex-wrap gap-2">
              {["Fashion", "Kuliner", "Kecantikan", "Jasa", "Retail"].map(tag => (
                <span key={tag} className="px-2 py-0.5 text-[10px] bg-brand/10 text-brand rounded-md border border-brand/20 font-mono">{tag}</span>
              ))}
            </div>
          </div>

          {/* Feature 2 */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-brand/40 transition-all space-y-5 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
              <Bot className="w-32 h-32 text-brand-ghost" />
            </div>
            <div className="w-12 h-12 rounded-2xl bg-brand-ghost/10 border border-brand-ghost/30 flex items-center justify-center text-brand-ghost">
              <Bot className="w-6 h-6" />
            </div>
            <h4 className="text-xl font-bold text-white">Bot Telegram Order Otomatis</h4>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Pelanggan pesan langsung via Telegram Bot bisnis Anda. Bot cek stok, buat tagihan Midtrans (QRIS, GoPay, OVO, transfer bank), konfirmasi bayar, dan notifikasi ke Anda — semua otomatis 24/7.
            </p>
            <div className="flex flex-wrap gap-2">
              {["QRIS", "GoPay", "OVO", "DANA", "Transfer"].map(tag => (
                <span key={tag} className="px-2 py-0.5 text-[10px] bg-brand-ghost/10 text-brand-ghost rounded-md border border-brand-ghost/20 font-mono">{tag}</span>
              ))}
            </div>
          </div>

          {/* Feature 3 */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-brand/40 transition-all space-y-5 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
              <BarChart3 className="w-32 h-32 text-umkm-teal" />
            </div>
            <div className="w-12 h-12 rounded-2xl bg-teal-500/10 border border-teal-500/30 flex items-center justify-center text-teal-400">
              <BarChart3 className="w-6 h-6" />
            </div>
            <h4 className="text-xl font-bold text-white">Analitik & Laporan Keuangan</h4>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Pantau omset harian, mingguan, dan bulanan secara real-time. AI memberikan insight produk terlaris, prediksi stok habis, dan rekomendasi taktis bisnis berbasis data penjualan Anda.
            </p>
            <div className="flex flex-wrap gap-2">
              {["Grafik Omset", "Prediksi Stok", "AI Insight"].map(tag => (
                <span key={tag} className="px-2 py-0.5 text-[10px] bg-teal-500/10 text-teal-400 rounded-md border border-teal-500/20 font-mono">{tag}</span>
              ))}
            </div>
          </div>

          {/* Feature 4 */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-brand/40 transition-all space-y-5 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
              <Package className="w-32 h-32 text-umkm-purple" />
            </div>
            <div className="w-12 h-12 rounded-2xl bg-purple-500/10 border border-purple-500/30 flex items-center justify-center text-purple-400">
              <Package className="w-6 h-6" />
            </div>
            <h4 className="text-xl font-bold text-white">Manajemen Stok Cerdas</h4>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Kelola ratusan produk dengan mudah. Notifikasi otomatis saat stok hampir habis, import produk massal via CSV, dan kategori produk fleksibel sesuai jenis usaha Anda.
            </p>
            <div className="flex flex-wrap gap-2">
              {["Alert Stok", "Import CSV", "Multi Kategori"].map(tag => (
                <span key={tag} className="px-2 py-0.5 text-[10px] bg-purple-500/10 text-purple-400 rounded-md border border-purple-500/20 font-mono">{tag}</span>
              ))}
            </div>
          </div>

          {/* Feature 5 */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-brand/40 transition-all space-y-5 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
              <Wallet className="w-32 h-32 text-umkm-gold" />
            </div>
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400">
              <Wallet className="w-6 h-6" />
            </div>
            <h4 className="text-xl font-bold text-white">Pembayaran Digital Terintegrasi</h4>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Tidak perlu konfirmasi bayar manual lagi! Midtrans Webhook otomatis memverifikasi setiap transaksi, update status order, dan kirim notifikasi ke owner — bahkan saat Anda tidur.
            </p>
            <div className="flex flex-wrap gap-2">
              {["Auto-Konfirmasi", "Webhook", "Anti-Fraud"].map(tag => (
                <span key={tag} className="px-2 py-0.5 text-[10px] bg-amber-500/10 text-amber-400 rounded-md border border-amber-500/20 font-mono">{tag}</span>
              ))}
            </div>
          </div>

          {/* Feature 6 */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 hover:border-brand/40 transition-all space-y-5 relative overflow-hidden group">
            <div className="absolute top-0 right-0 p-6 opacity-5 group-hover:opacity-10 transition-opacity">
              <Smartphone className="w-32 h-32 text-umkm-sky" />
            </div>
            <div className="w-12 h-12 rounded-2xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
              <Smartphone className="w-6 h-6" />
            </div>
            <h4 className="text-xl font-bold text-white">Aplikasi Mobile Owner</h4>
            <p className="text-zinc-400 text-sm leading-relaxed">
              Pantau bisnis kapanpun dari HP Anda. Terima notifikasi order baru, approve/tolak pesanan, lihat summary harian, dan scan produk langsung dari aplikasi Flutter mobile.
            </p>
            <div className="flex flex-wrap gap-2">
              {["Android", "iOS", "Real-time Push"].map(tag => (
                <span key={tag} className="px-2 py-0.5 text-[10px] bg-sky-500/10 text-sky-400 rounded-md border border-sky-500/20 font-mono">{tag}</span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ================= SECTION 4: HOW IT WORKS ================= */}
      <section id="how-it-works" className="max-w-7xl mx-auto px-6 py-20 border-t border-zinc-900 bg-ghost-glow bg-no-repeat bg-contain bg-right-bottom">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs font-bold tracking-widest text-brand uppercase mb-3">CARA KERJA SISTEM</h2>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-white">
            4 Langkah, Bisnis Anda Langsung Jalan
          </h3>
          <p className="text-zinc-400 mt-4">
            Dedemit UMKM dirancang sangat mudah agar pemilik usaha bisa fokus melayani pelanggan, bukan mengurus administrasi.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 relative">
          {[
            {
              step: "01",
              icon: "🏪",
              title: "Daftarkan Usaha",
              desc: "Buat akun gratis, isi profil usaha (nama toko, jenis bisnis, alamat). Tidak perlu keahlian teknis — siap dalam 5 menit."
            },
            {
              step: "02",
              icon: "📸",
              title: "Input Produk via AI Scan",
              desc: "Foto produk Anda, AI langsung mendeteksi detail, mengisi form otomatis. Tambahkan harga & stok, klik Simpan."
            },
            {
              step: "03",
              icon: "🤖",
              title: "Aktifkan Bot Telegram",
              desc: "Sambungkan Bot Telegram toko Anda dalam satu klik. Pelanggan sudah bisa order dan bayar otomatis 24/7."
            },
            {
              step: "04",
              icon: "📊",
              title: "Pantau & Kembangkan",
              desc: "Monitor omset real-time, baca insight AI, lihat produk terlaris, dan kembangkan bisnis berdasarkan data akurat."
            }
          ].map((item, i) => (
            <div key={i} className="space-y-4 relative">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-xl bg-brand text-white flex items-center justify-center font-bold font-mono text-sm">
                  {item.step}
                </div>
                <span className="text-2xl">{item.icon}</span>
              </div>
              <h4 className="text-lg font-bold text-white">{item.title}</h4>
              <p className="text-xs text-zinc-400 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* ================= SECTION 5: TESTIMONIAL ================= */}
      <section id="testimonials" className="max-w-7xl mx-auto px-6 py-20 border-t border-zinc-900">
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-xs font-bold tracking-widest text-brand uppercase mb-3">CERITA SUKSES UMKM</h2>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-white">
            Telah Membantu 2.000+ Pelaku UMKM Indonesia
          </h3>
          <p className="text-zinc-400 mt-4">
            Dari warung makan Bandung, toko baju Surabaya, hingga salon kecantikan Medan — mereka sudah merasakan manfaatnya.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="p-8 rounded-3xl bg-zinc-900/20 border border-zinc-800 flex flex-col justify-between gap-6 hover:border-zinc-700 transition-all">
            <div>
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-brand-ghost text-brand-ghost" />)}
              </div>
              <p className="text-sm italic text-zinc-300 leading-relaxed">
                "Dulu ngitung stok bahan baku warung makan manual tiap pagi — sekarang tinggal lihat dashboard. Bot Telegram-nya juga langsung terima order takeaway pelanggan, saya bisa fokus masak!"
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-brand flex items-center justify-center font-bold text-white text-sm">
                SR
              </div>
              <div>
                <h4 className="text-xs font-bold text-white">Sari Rahayu</h4>
                <p className="text-[10px] text-zinc-500">Warung Bu Sari — Bandung 🍜</p>
              </div>
            </div>
          </div>

          <div className="p-8 rounded-3xl bg-zinc-900/20 border border-zinc-800 flex flex-col justify-between gap-6 hover:border-zinc-700 transition-all">
            <div>
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-brand-ghost text-brand-ghost" />)}
              </div>
              <p className="text-sm italic text-zinc-300 leading-relaxed">
                "Saya punya toko baju di Pasar Atom. Fitur scan AI-nya gila — foto baju langsung keluar estimasi harga, kategori, dan caption Instagram yang udah siap posting. Omset naik 35% dalam 2 bulan!"
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-brand-ghost flex items-center justify-center font-bold text-zinc-950 text-sm">
                DK
              </div>
              <div>
                <h4 className="text-xs font-bold text-white">Dian Kusuma</h4>
                <p className="text-[10px] text-zinc-500">Toko Fashion Dian — Surabaya 👗</p>
              </div>
            </div>
          </div>

          <div className="p-8 rounded-3xl bg-zinc-900/20 border border-zinc-800 flex flex-col justify-between gap-6 hover:border-zinc-700 transition-all">
            <div>
              <div className="flex gap-1 mb-4">
                {[...Array(5)].map((_, i) => <Star key={i} className="w-4 h-4 fill-brand-ghost text-brand-ghost" />)}
              </div>
              <p className="text-sm italic text-zinc-300 leading-relaxed">
                "Salon saya menerima booking via Telegram Bot sekarang. Pembayaran QRIS otomatis terkonfirmasi, tidak perlu cek rekening manual lagi. Customer makin percaya karena terasa profesional!"
              </p>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full bg-teal-500 flex items-center justify-center font-bold text-white text-sm">
                NF
              </div>
              <div>
                <h4 className="text-xs font-bold text-white">Nurul Fadilah</h4>
                <p className="text-[10px] text-zinc-500">Salon Nurul Beauty — Medan 💄</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ================= SECTION 6: PRICING ================= */}
      <section id="pricing" className="max-w-7xl mx-auto px-6 py-20 border-t border-zinc-900">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-xs font-bold tracking-widest text-brand uppercase mb-3">PAKET BERLANGGANAN</h2>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-white">
            Harga Terjangkau untuk Semua Skala UMKM
          </h3>
          <p className="text-zinc-400 mt-4">
            Mulai gratis tanpa batas waktu, upgrade kapanpun bisnis Anda siap berkembang lebih jauh.
          </p>

          {/* Billing Toggle */}
          <div className="mt-8 inline-flex items-center gap-2 p-1.5 bg-zinc-900 rounded-2xl border border-zinc-800">
            <button 
              onClick={() => setBillingPeriod("monthly")}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                billingPeriod === "monthly" ? "bg-brand text-white" : "text-zinc-400 hover:text-white"
              }`}
            >
              Bulanan
            </button>
            <button 
              onClick={() => setBillingPeriod("annually")}
              className={`px-4 py-2 rounded-xl text-xs font-bold transition-all ${
                billingPeriod === "annually" ? "bg-brand text-white" : "text-zinc-400 hover:text-white"
              }`}
            >
              Tahunan (-20%) 🎉
            </button>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {/* Plan 1: Free */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 flex flex-col justify-between gap-8 hover:border-zinc-700 transition-all">
            <div className="space-y-6">
              <div>
                <span className="text-xs font-bold text-zinc-500 uppercase tracking-wider">PEMULA</span>
                <h4 className="text-xl font-bold text-white mt-1">Paket Gratis</h4>
                <p className="text-xs text-zinc-500 mt-1">Cocok untuk UMKM yang baru mulai berjualan online.</p>
              </div>
              
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-extrabold text-white">Rp0</span>
                <span className="text-zinc-500 text-xs font-mono">/selamanya</span>
              </div>

              <div className="border-t border-zinc-800 pt-6 space-y-3 text-xs text-zinc-400">
                {[
                  "10 Scan AI Produk / bulan",
                  "Bot Telegram Standar",
                  "50 Transaksi / bulan",
                  "Dashboard Web Dasar",
                  "Laporan Mingguan",
                ].map(f => (
                  <div key={f} className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-brand flex-shrink-0" /> {f}
                  </div>
                ))}
              </div>
            </div>

            <Link href="/dashboard" className="w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 text-white text-center py-3 rounded-2xl text-xs font-bold transition-all block">
              Mulai Gratis Sekarang
            </Link>
          </div>

          {/* Plan 2: Pro */}
          <div className="p-8 rounded-3xl bg-zinc-900/60 border border-brand/50 flex flex-col justify-between gap-8 relative overflow-hidden group hover:border-brand transition-all shadow-xl hover:shadow-brand/10">
            <div className="absolute top-0 right-0 bg-brand text-white text-[9px] font-extrabold uppercase py-1 px-4 tracking-widest rounded-bl-xl font-mono">
              TERPOPULER
            </div>

            <div className="space-y-6">
              <div>
                <span className="text-xs font-bold text-brand uppercase tracking-wider">PRO UMKM</span>
                <h4 className="text-xl font-bold text-white mt-1 flex items-center gap-1.5">
                  Paket Bisnis <Sparkles className="w-4 h-4 text-brand-ghost" />
                </h4>
                <p className="text-xs text-zinc-400 mt-1">Untuk UMKM yang ingin tumbuh cepat dan efisien.</p>
              </div>

              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-extrabold text-white">
                  {billingPeriod === "monthly" ? "Rp99.000" : "Rp79.000"}
                </span>
                <span className="text-zinc-500 text-xs font-mono">/bulan</span>
              </div>

              <div className="border-t border-zinc-800 pt-6 space-y-3 text-xs text-zinc-300">
                {[
                  "Unlimited Scan AI Gemini",
                  "Caption Generator Sosmed",
                  "Bot Telegram Unlimited Order",
                  "QRIS + E-Wallet + Bank Transfer",
                  "Analitik & Laporan Keuangan",
                  "Prediksi Stok Habis AI",
                  "Notifikasi WhatsApp & Telegram",
                ].map(f => (
                  <div key={f} className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-brand flex-shrink-0" /> {f}
                  </div>
                ))}
              </div>
            </div>

            <Link href="/dashboard" className="w-full bg-brand hover:bg-brand-dark text-white text-center py-3 rounded-2xl text-xs font-bold shadow-lg hover:shadow-brand/20 transition-all block">
              Upgrade ke Pro
            </Link>
          </div>

          {/* Plan 3: Enterprise */}
          <div className="p-8 rounded-3xl bg-zinc-900/30 border border-zinc-800 flex flex-col justify-between gap-8 hover:border-zinc-700 transition-all">
            <div className="space-y-6">
              <div>
                <span className="text-xs font-bold text-zinc-500 uppercase tracking-wider">KORPORAT</span>
                <h4 className="text-xl font-bold text-white mt-1">Paket Enterprise</h4>
                <p className="text-xs text-zinc-500 mt-1">Untuk jaringan toko atau franchise dengan banyak cabang.</p>
              </div>
              
              <div className="flex items-baseline gap-1">
                <span className="text-4xl font-extrabold text-white">Custom</span>
              </div>

              <div className="border-t border-zinc-800 pt-6 space-y-3 text-xs text-zinc-400">
                {[
                  "Multi-Outlet Management",
                  "Custom AI Model Training",
                  "Dedicated Account Manager",
                  "API Integrasi Custom",
                  "SLA & Priority Support 24/7",
                  "Laporan Konsolidasi Cabang",
                ].map(f => (
                  <div key={f} className="flex items-center gap-2">
                    <CheckCircle2 className="w-4 h-4 text-brand-ghost flex-shrink-0" /> {f}
                  </div>
                ))}
              </div>
            </div>

            <a href="https://t.me/dedemit_umkm" className="w-full bg-zinc-900 hover:bg-zinc-800 border border-zinc-800 hover:border-zinc-700 text-white text-center py-3 rounded-2xl text-xs font-bold transition-all block">
              Hubungi Tim Sales
            </a>
          </div>
        </div>
      </section>

      {/* ================= SECTION 7: FAQ ================= */}
      <section id="faq" className="max-w-4xl mx-auto px-6 py-20 border-t border-zinc-900">
        <div className="text-center mb-16">
          <h2 className="text-xs font-bold tracking-widest text-brand uppercase mb-3">PERTANYAAN UMUM</h2>
          <h3 className="text-3xl sm:text-4xl font-extrabold text-white">Ada Pertanyaan?</h3>
        </div>

        <div className="space-y-4">
          {faqs.map((faq, i) => (
            <div key={i} className="border border-zinc-800 rounded-2xl overflow-hidden hover:border-zinc-700 transition-all">
              <button
                onClick={() => setActiveFaq(activeFaq === i ? null : i)}
                className="w-full flex justify-between items-center p-6 text-left"
              >
                <span className="text-sm font-semibold text-white">{faq.q}</span>
                <HelpCircle className={`w-5 h-5 flex-shrink-0 ml-4 transition-all ${activeFaq === i ? "text-brand rotate-180" : "text-zinc-600"}`} />
              </button>
              <AnimatePresence>
                {activeFaq === i && (
                  <motion.div
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: "auto", opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="overflow-hidden"
                  >
                    <p className="px-6 pb-6 text-sm text-zinc-400 leading-relaxed">{faq.a}</p>
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </section>

      {/* ================= FOOTER ================= */}
      <footer className="max-w-7xl mx-auto px-6 py-12 border-t border-zinc-900 text-xs text-zinc-500">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          <div className="flex items-center gap-3">
            <span className="text-2xl">👻</span>
            <div>
              <h4 className="text-sm font-bold text-white tracking-wider">DEDEMIT UMKM</h4>
              <p className="text-[8px] tracking-widest text-zinc-600 uppercase font-semibold">AI Business OS untuk Semua UMKM</p>
            </div>
          </div>

          <div className="flex flex-wrap justify-center items-center gap-6 font-mono">
            <a href="https://instagram.com" className="hover:text-white transition-colors">Instagram</a>
            <a href="https://tiktok.com" className="hover:text-white transition-colors">TikTok</a>
            <a href="https://t.me/dedemit_umkm" className="hover:text-white transition-colors">Telegram</a>
            <a href="https://wa.me/6281234567890" className="hover:text-white transition-colors">WhatsApp</a>
            <a href="mailto:support@dedemit-umkm.id" className="hover:text-white transition-colors">Email</a>
          </div>

          <p className="text-center md:text-right font-mono">
            &copy; 2026 Dedemit UMKM. Dibuat dengan ❤️ untuk UMKM Indonesia.
          </p>
        </div>
      </footer>
    </div>
  );
}
