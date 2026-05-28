# 👻 Dedemit UMKM — AI Business OS untuk Semua Sektor UMKM Indonesia

**Dedemit UMKM** adalah sistem operasi bisnis berbasis Kecerdasan Buatan (AI) yang dirancang khusus untuk merevolusi ekosistem UMKM di Indonesia, mulai dari warung makan, toko fashion, salon kecantikan, laundry, bengkel, toko kelontong, hingga penyedia jasa. Sistem ini membantu pemilik bisnis mengelola katalog produk dan jasa, melakukan analisis produk/jasa berbasis AI (*AI smart scanner & describer*), menulis caption promosi otomatis untuk media sosial, memproses pembayaran via Midtrans, serta berinteraksi secara otomatis dengan pelanggan & owner via Telegram Bot.

Monorepo ini berisi seluruh platform yang terintegrasi secara modular untuk efisiensi pengembangan maksimum.

---

## 🛠️ Tech Stack & Platform

Platform ini didesain menggunakan arsitektur monorepo dengan pembagian kerja berikut:

*   📱 **`/mobile`**: Flutter 3.x + Riverpod + Dio (Aplikasi untuk Owner Bisnis - Android & iOS)
*   💻 **`/web`**: Next.js 14 (App Router) + TailwindCSS + shadcn/ui (Landing Page & Dashboard Web)
*   ⚙️ **`/backend`**: FastAPI + SQLAlchemy + Alembic + PostgreSQL (Main RESTful API)
*   🤖 **`/bot`**: python-telegram-bot v20 (Telegram Bot untuk Automasi Hubungan Pelanggan & Owner)
*   📦 **`/shared`**: TypeScript Shared Constants & Types (Skema Data Bersama)

---

## 📂 Struktur Direktori Monorepo

```text
dedemit-umkm/
├── .env.example            # Template Environment Variables global
├── .gitignore              # Git ignore terpadu untuk semua platform
├── docker-compose.yml      # Orkestrasi Docker untuk Database PostgreSQL
├── README.md               # Dokumentasi utama ini
│
├── shared/                 # Modul Konstan & Tipe Bersama (TypeScript)
│   ├── package.json
│   ├── tsconfig.json
│   └── src/
│       ├── constants.ts    # Status order, kategori usaha (kuliner, jasa, dll)
│       └── types.ts        # Interface & Types bersama
│
├── backend/                # RESTful API Utama (Python FastAPI)
│   ├── requirements.txt    # Library python (FastAPI, SQLAlchemy, Alembic, Pydantic)
│   ├── alembic.ini         # Konfigurasi migrasi database Alembic
│   ├── Dockerfile          # Kontainerisasi API
│   ├── alembic/            # Folder migrasi database
│   └── app/                # Kode sumber backend (main.py, models, schemas, api, dll.)
│
├── bot/                    # Telegram Bot Service (Python)
│   ├── requirements.txt    # Library python-telegram-bot v20 & HTTPX
│   ├── Dockerfile          # Kontainerisasi Telegram Bot
│   └── bot/                # Handlers, services, dan entrypoint bot (main.py)
│
├── web/                    # Dashboard & Landing Page (Next.js 14)
│   ├── package.json        # Next.js, React, Tailwind, Lucide, dll.
│   ├── tsconfig.json       # Konfigurasi TypeScript
│   ├── tailwind.config.ts  # Desain sistem Tailwind & Token warna
│   └── app/                # Next.js 14 App Router (layout, page, dashboard)
│
└── mobile/                 # Mobile App Owner (Flutter 3.x)
    ├── pubspec.yaml        # Manajemen package (dio, flutter_riverpod, dll.)
    └── lib/                # Clean Architecture berorientasi fitur (core, features)
```

---

## ⚡ Panduan Menjalankan Platform (Quick Start)

### 1. Prasyarat Sistem
Pastikan perangkat Anda telah terinstal tools berikut:
*   Docker & Docker Compose (Untuk database PostgreSQL)
*   Python 3.10+ (Untuk backend & bot)
*   Node.js 18+ (Untuk web & shared constants)
*   Flutter SDK 3.19+ & Dart SDK 3.x (Untuk mobile)

### 2. Konfigurasi Environment Variables
Salin berkas `.env.example` menjadi `.env` di root direktori, lalu lengkapi nilai variabelnya:
```bash
cp .env.example .env
```

### 3. Jalankan Database Lokal (PostgreSQL)
Jalankan Docker Compose untuk memulai layanan database PostgreSQL:
```bash
docker compose up -d postgres_db
```

---

## 🚀 Langkah Menjalankan Tiap Platform secara Lokal

### A. Shared Module (`/shared`)
Modul ini berisi tipe data TypeScript dan konstanta bisnis.
```bash
# Masuk ke direktori
cd shared

# Instal dependensi & build modul
npm install
npm run build
```

### B. Backend API (`/backend`)
```bash
# Masuk ke direktori
cd backend

# Membuat virtual environment
python -m venv venv
source venv/bin/activate  # Untuk macOS/Linux
# venv\Scripts\activate   # Untuk Windows

# Instal dependensi
pip install -r requirements.txt

# Menjalankan database migrasi (Alembic)
alembic upgrade head

# Jalankan server FastAPI (reload mode aktif)
uvicorn app.main:app --reload --port 8000
```
API akan tersedia secara lokal di: `http://localhost:8000` dengan Swagger UI interaktif di `http://localhost:8000/docs`.

### C. Telegram Bot (`/bot`)
```bash
# Masuk ke direktori
cd bot

# Aktifkan virtual environment (bisa buat venv terpisah atau gabung)
python -m venv venv
source venv/bin/activate

# Instal dependensi
pip install -r requirements.txt

# Jalankan Telegram Bot
python -m bot.main
```

### D. Web Dashboard & Landing (`/web`)
```bash
# Masuk ke direktori
cd web

# Instal dependensi
npm install

# Jalankan mode development
npm run dev
```
Aplikasi web dapat diakses di `http://localhost:3000`.

### E. Mobile App Owner (`/mobile`)
```bash
# Masuk ke direktori
cd mobile

# Dapatkan dependensi Dart/Flutter
flutter pub get

# Jalankan aplikasi (pastikan emulator/perangkat fisik terhubung)
flutter run
```

---

## 📐 Konvensi Penamaan (Naming Conventions)

Demi menjaga kebersihan dan konsistensi kode monorepo Dedemit UMKM:

*   **Python (FastAPI & Telegram Bot)**:
    *   Mengikuti gaya penulisan [PEP 8](https://peps.python.org/pep-0008/).
    *   File & Folder: `snake_case` (contoh: `product_model.py`, `auth_router.py`).
    *   Variabel & Fungsi: `snake_case` (contoh: `calculate_base_price()`, `business_category`).
    *   Kelas: `PascalCase` (contoh: `InventoryService`, `TelegramBotHandler`).
*   **Dart / Flutter**:
    *   Mengikuti panduan resmi [Dart Style Guide](https://dart.dev/guides/language/effective-dart/style).
    *   File & Folder: `snake_case` (contoh: `inventory_notifier.dart`, `product_card.dart`).
    *   Variabel & Fungsi: `camelCase` (contoh: `isLoading`, `updateStock()`).
    *   Kelas: `PascalCase` (contoh: `ProductCard`, `AuthScreenNotifier`).
*   **TypeScript & JavaScript (Web & Shared)**:
    *   Routing & Folder URL: `kebab-case` (contoh: `/dashboard/inventory-settings`).
    *   Fungsi & Variabel: `camelCase` (contoh: `fetchProductDetails()`, `totalAmount`).
    *   Komponen React & Kelas: `PascalCase` (contoh: `DashboardHeader`, `PaymentProcessor`).

---

## 🧠 Fitur Pintar AI & Integrasi Midtrans
1.  **AI Smart Scanner**: Cukup unggah foto produk/jasa melalui Telegram Bot atau Mobile App, AI akan menganalisis brand, estimasi kelayakan/kondisi produk, memprediksi jenis usaha, dan memberikan rekomendasi harga pasar berdasarkan basis data UMKM Indonesia menggunakan Google Gemini API.
2.  **Midtrans Snap Integrasi**: Mendukung pembayaran instan QRIS, Virtual Account bank nasional (BCA, Mandiri, BNI), dan e-wallet lokal untuk kemudahan transaksi pembeli bagi segala sektor usaha.

---
*Dibuat dengan ❤️ oleh Tim Senior Software Architect Dedemit UMKM.*
