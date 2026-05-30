# 🎬 Panduan Demo Dedemit OS — 7 Menit
## #JuaraVibeCoding Competition Demo Script

> **Target Audience:** Juri kompetisi, investor, pengguna baru  
> **Durasi:** 7 menit (+ 3 menit Q&A)  
> **Mode Demo:** Live dengan akun `bos@dedemit.id`  
> **URL Live:** [https://dedemit.vercel.app](https://dedemit.vercel.app)

---

## Pre-Demo Checklist (5 menit sebelum)

- [ ] Backend Railway aktif: `https://dedemit-backend.up.railway.app/health` → status "healthy"
- [ ] Web Vercel aktif: `https://dedemit.vercel.app`
- [ ] Database sudah di-seed: `python seed_demo_data.py` sudah dijalankan
- [ ] Telegram Bot aktif: @DedemitOSBot di Telegram
- [ ] Browser tabs siap: Web dashboard + Telegram + Postman/API docs
- [ ] Screen recording aktif (backup jika internet kurang stabil)

---

## 🕐 Menit 1–2: Landing Page → Register → Pilih Jenis Usaha

### Talking Points:
> *"Dedemit OS hadir untuk UMKM Indonesia yang selama ini mengelola bisnis hanya dari catatan dan WhatsApp. Dengan satu aplikasi, semua bisa dikelola — dari inventory, order, hingga laporan keuangan."*

### Steps:
1. **Buka** `https://dedemit.vercel.app`
   - Highlight: hero section, tagline "AI untuk Warung, Salon, Bengkel kamu"
   - Tunjukkan: showcase fitur di landing page

2. **Klik** tombol "Mulai Gratis" atau "Daftar Sekarang"
   - Isi form registrasi:
     - Nama: `Demo Juri 2024`  
     - Email: `demo.juri@test.id`
     - Tipe Usaha: **Warung** (showcase 3 pilihan yang tersedia)
     - Kota: `Jakarta`
     - Password: `Demo1234!`

3. **Setelah register**, sistem otomatis login dan redirect ke dashboard

> **Key Highlight:** "Cuma 30 detik untuk onboarding — tidak perlu konfigurasi teknis apapun!"

---

## 🕑 Menit 2–3: AI Scanner (Foto Produk → Analisis → Simpan Inventory)

### Talking Points:
> *"Fitur paling revolusioner Dedemit: cukup foto produk kamu, AI akan otomatis mengidentifikasi nama produk, kategori, dan harga pasar. Owner warung tidak perlu input manual satu-satu."*

### Steps:
1. **Navigasi** ke menu "Inventory" di sidebar

2. **Klik** tombol "📷 Scan Produk Baru"

3. **Upload** foto produk (contoh: foto mie instan, baju thrift, dll)
   - AI akan menganalisis foto (2-3 detik)
   - Tampilkan loading state dengan animasi

4. **Review hasil AI:**
   - Nama produk terdeteksi otomatis
   - Kategori terdeteksi
   - Estimasi harga pasar

5. **Edit jika perlu** dan klik "Simpan ke Inventory"

6. **Tampilkan** daftar inventory yang bertambah real-time

> **Key Highlight:** "Dibandingkan input manual, AI scanner menghemat 80% waktu pencatatan inventory!"

---

## 🕒 Menit 3–4: Buat Order → Payment Link → Simulasi Bayar

### Talking Points:
> *"Dedemit terintegrasi langsung dengan Midtrans — payment gateway terbesar Indonesia. Owner bisa generate link pembayaran dalam satu klik, dan pelanggan bisa bayar via transfer bank, QRIS, atau dompet digital."*

### Steps:
1. **Navigasi** ke menu "Orders"

2. **Klik** "Buat Order Baru"
   - Pilih pelanggan: "Pak Budi Santoso" (dari daftar)
   - Tambah items dari inventory (klik produk)
   - Set jumlah

3. **Review total** dan klik "Buat & Generate Payment Link"

4. **Tampilkan payment link** yang dihasilkan:
   ```
   https://app.midtrans.com/snap/v2/vtweb/snap-token-xxxxx
   ```

5. **Demo simulasi bayar** (jika di sandbox):
   - Buka link di tab baru
   - Pilih metode pembayaran
   - Konfirmasi (sandbox tidak perlu bayar beneran)

6. **Kembali ke dashboard** — status order otomatis berubah ke "✅ Paid" via webhook

> **Key Highlight:** "Webhook otomatis dari Midtrans — tidak perlu cek manual!"

---

## 🕓 Menit 4–5: Bot Telegram → Pelanggan Order → Notif Owner

### Talking Points:
> *"Pelanggan setia kamu bisa order langsung via Telegram Bot — tanpa download aplikasi apapun! Dan owner langsung dapat notifikasi di HP-nya."*

### Steps:
1. **Buka** Telegram di HP atau browser (t.me/DedemitOSBot)

2. **Kirim** `/start` ke bot
   - Bot menyambut dengan menu interaktif

3. **Pilih** "🛒 Lihat Menu / Order"
   - Bot menampilkan daftar produk dengan harga

4. **Pilih** produk dan jumlah

5. **Bot kirim** link pembayaran Midtrans ke pelanggan

6. **Tampilkan** di dashboard owner: notifikasi "🔔 Order baru dari Telegram!"
   - Real-time via polling/webhook

> **Key Highlight:** "Bot bekerja 24/7 — bahkan saat owner tidur, pesanan tetap masuk!"

---

## 🕔 Menit 5–6: Dashboard Analytics → AI Insight → Laporan Keuangan

### Talking Points:
> *"Semua data bisnis terangkum di dashboard analytics yang cantik. Dan AI akan memberikan insight dan rekomendasi aksi nyata — bukan sekedar grafik yang membingungkan."*

### Steps:
1. **Navigasi** ke "Analytics" di sidebar

2. **Tampilkan:**
   - Grafik revenue 30 hari (line chart)
   - Produk terlaris (bar chart)
   - Pelanggan paling aktif

3. **Scroll ke bagian "AI Insight":**
   - "Penjualan meningkat 23% minggu ini dibanding minggu lalu"
   - "Stok Nasi Goreng Spesial hampir habis — perlu restock dalam 2 hari"
   - "Pelanggan Pak Budi sudah 3x order bulan ini — pertimbangkan loyalty reward"

4. **Navigasi** ke "Keuangan":
   - Laporan laba rugi
   - Total pemasukan vs pengeluaran
   - Ekspor ke PDF (demo klik tombol)

> **Key Highlight:** "AI tidak hanya menampilkan data — dia memberikan rekomendasi yang bisa langsung dijalankan!"

---

## 🕕 Menit 6–7: Settings → Kemudahan Setup → Closing

### Talking Points:
> *"Dedemit dirancang untuk owner UMKM yang tidak punya tim IT. Setup lengkap bisa selesai dalam 10 menit."*

### Steps:
1. **Navigasi** ke "Settings"
   - Tampilkan: edit profil toko, logo, informasi kontak

2. **Highlight integrations panel:**
   - Midtrans (status: ✅ Terhubung)
   - Telegram Bot (status: ✅ Aktif)
   - AI Engine (status: ✅ Google Gemini)

3. **Tutup dengan closing statement:**

> *"Dedemit OS adalah solusi all-in-one untuk UMKM Indonesia — dari inventory AI, manajemen order, pembayaran otomatis, hingga bot Telegram. Semua dalam satu platform, tanpa biaya setup, tanpa tim IT. Karena setiap warung, salon, dan bengkel di Indonesia berhak punya sistem bisnis sekelas perusahaan besar."*
>
> *"Terima kasih! Ada pertanyaan?"*

---

## 💡 Tips Presentasi

| Situasi | Solusi |
|---------|--------|
| Internet lambat | Gunakan screen recording yang sudah disiapkan |
| AI timeout | Tunjukkan hasil yang sudah ada di seed data |
| Bot Telegram error | Demo via API endpoint di `/docs` |
| Payment gateway error | Tampilkan simulasi dengan order yang sudah ada |

## 🔑 Credential Demo

| Akun | Email | Password | Jenis Usaha |
|------|-------|----------|-------------|
| **Main Demo** | `bos@dedemit.id` | `Password123!` | Warung Bu Sari (Surabaya) |
| Salon Demo | `dewi.salon@dedemit.id` | `Password123!` | Salon Kecantikan Dewi |
| Bengkel Demo | `bengkel.jaya@dedemit.id` | `Password123!` | Bengkel Jaya Motor |

## 📊 Data Demo yang Tersedia
- **3 toko** dengan jenis usaha berbeda
- **30 produk/jasa** total (10 per toko)
- **24 pelanggan** total (8 per toko)
- **45 order** dengan berbagai status
- **30 hari history** transaksi untuk grafik
- **15 catatan pengeluaran** untuk laporan keuangan
