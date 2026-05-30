# 👻 Dedemit UMKM — AI Business OS untuk Semua Sektor UMKM Indonesia by Mas Obets Dev

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

## 🏗️ Arsitektur Sistem

```
╔═══════════════════════════════════════════════════════════════╗
║                    DEDEMIT OS ARCHITECTURE                    ║
╠═══════════════════════════════════════════════════════════════╣
║                                                               ║
║  📱 Flutter Mobile          🌐 Next.js Web                    ║
║  (iOS & Android)           (Dashboard + Landing)             ║
║        │                          │                           ║
║        └──────────────┬───────────┘                           ║
║                       │ HTTPS / REST API                      ║
║                       ▼                                       ║
║          ┌─────────────────────────────┐                      ║
║          │    FastAPI Backend (Python)  │                      ║
║          │                             │                      ║
║          │  ┌────────┐  ┌──────────┐   │                      ║
║          │  │ Auth   │  │Inventory │   │                      ║
║          │  │ Orders │  │Analytics │   │  ──► 🤖 Gemini AI    ║
║          │  │Payments│  │ Finance  │   │  ──► 🧠 Claude AI    ║
║          │  └────────┘  └──────────┘   │  ──► 💳 Midtrans    ║
║          └──────┬───────────────┬───────┘                     ║
║                 │               │                             ║
║          ┌──────▼──┐      ┌─────▼───┐                         ║
║          │PostgreSQL│      │  Redis  │                         ║
║          │   (DB)  │      │ (Cache) │                         ║
║          └─────────┘      └─────────┘                         ║
║                                                               ║
║  🤖 Telegram Bot ──────────────► Backend API                  ║
║  (Python Worker)                                              ║
╚═══════════════════════════════════════════════════════════════╝
```

---

## ✨ Fitur Utama

| Fitur | Deskripsi | Status |
|-------|-----------|--------|
| 📸 **AI Product Scanner** | Foto produk → AI identifikasi nama, kategori, harga | ✅ Live |
| 📦 **Manajemen Inventory** | Stok real-time, alert hampir habis, bulk import CSV | ✅ Live |
| 🛒 **Order Management** | Buat order, tracking status, history lengkap | ✅ Live |
| 💳 **Pembayaran Midtrans** | QRIS, transfer bank, dompet digital, kartu kredit | ✅ Live |
| 🧾 **OCR Bukti Transfer** | Upload foto struk → AI verifikasi otomatis | ✅ Live |
| 🤖 **Telegram Bot** | Pelanggan order via bot, notif real-time ke owner | ✅ Live |
| 📊 **Analytics Dashboard** | Grafik revenue, best sellers, retensi pelanggan | ✅ Live |
| 🧠 **AI Business Insight** | Rekomendasi aksi berbasis data aktual | ✅ Live |
| 💰 **Laporan Keuangan** | Laba rugi, pengeluaran, arus kas per periode | ✅ Live |
| 📱 **Mobile App (Flutter)** | Native iOS & Android untuk owner di lapangan | ✅ Live |

---

## ⚡ Quick Start (5 Langkah)

### Prasyarat
- Docker & Docker Compose
- Python 3.11+
- Node.js 18+

### Langkah 1: Clone & Setup Environment
```bash
git clone https://github.com/yourusername/uka-uka.git
cd uka-uka

# Jalankan wizard setup interaktif
bash setup-env.sh
```

### Langkah 2: Cek Dependency
```bash
bash check-deps.sh
```

### Langkah 3: Jalankan Semua Service
```bash
docker-compose up --build -d
```

### Langkah 4: Isi Database dengan Data Demo
```bash
cd backend
pip install -r requirements.txt
python seed_demo_data.py
```

### Langkah 5: Buka Aplikasi
```
🌐 Web Dashboard:  http://localhost:3000
📚 API Docs:       http://localhost:8000/docs
❤️  Health Check:  http://localhost:8000/health

👤 Login Demo:
   Email:    bos@dedemit.id
   Password: Password123!
```

---

## 🛠️ Tech Stack

### Backend
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| **FastAPI** | 0.109 | REST API Framework |
| **SQLAlchemy** | 2.0 | ORM Async |
| **PostgreSQL** | 15 | Database Utama |
| **Redis** | 7 | Cache & Session |
| **Alembic** | 1.13 | Database Migrations |
| **PyJWT** | 2.8 | Authentication |
| **Google Gemini** | 0.4 | AI Vision & Analysis |
| **Anthropic Claude** | 0.18 | AI Fallback |
| **Midtrans** | SDK | Payment Gateway |

### Frontend
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| **Next.js** | 14 | Web Dashboard |
| **React** | 18 | UI Framework |
| **Tailwind CSS** | 3.4 | Styling |
| **Recharts** | 3.8 | Data Visualization |
| **Framer Motion** | 12 | Animasi |
| **SWR** | 2.4 | Data Fetching |

### Mobile
| Teknologi | Versi | Fungsi |
|-----------|-------|--------|
| **Flutter** | 3.x | Native iOS & Android |
| **Riverpod** | 2.6 | State Management |
| **Dio** | 5.x | HTTP Client |
| **Go Router** | 13 | Navigation |

### DevOps
| Teknologi | Fungsi |
|-----------|--------|
| **Docker** | Containerization |
| **Docker Compose** | Local Orchestration |
| **Railway** | Backend Hosting |
| **Vercel** | Frontend Hosting |
| **pytest** | Integration Testing |

---

## 🧪 Menjalankan Tests

```bash
cd backend

# Install test dependencies
pip install pytest pytest-asyncio httpx aiosqlite

# Jalankan 6 integration test suites
pytest tests/test_integration.py -v

# Jalankan dengan coverage report
pytest tests/test_integration.py -v --tb=short
```

**Test Suites yang tersedia:**
1. ✅ Register toko → Login → Dashboard accessible
2. ✅ Upload item → AI analyze → Simpan inventory
3. ✅ Buat order → Payment link → Webhook → Status paid
4. ✅ Upload bukti transfer → AI OCR → Order confirmed
5. ✅ Telegram Bot flow (via API simulation)
6. ✅ Dashboard analytics akurasi data

---

## 🚀 Deploy ke Production

Lihat panduan lengkap di **[DEPLOY.md](DEPLOY.md)**:
- **Railway** untuk Backend + PostgreSQL + Redis + Telegram Bot
- **Vercel** untuk Next.js Web Dashboard
- Setup Midtrans Webhook & Telegram Webhook

---

## 📁 Struktur Project

```
uka-uka/
├── 📁 backend/              # FastAPI REST API
│   ├── app/
│   │   ├── api/v1/          # Route handlers (auth, items, orders, dll)
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── ai_service.py    # Integrasi Gemini & Claude
│   │   ├── payment_service.py # Integrasi Midtrans
│   │   └── main.py          # FastAPI app entry point
│   ├── alembic/             # Database migrations
│   ├── tests/               # Integration tests (pytest)
│   ├── seed_demo_data.py    # Demo data seeder
│   └── Dockerfile           # Multi-stage build
│
├── 📁 web/                  # Next.js Web Dashboard
│   ├── app/
│   │   ├── dashboard/       # Dashboard pages
│   │   ├── inventory/       # Inventory pages
│   │   ├── orders/          # Order pages
│   │   └── ...              # Other pages
│   └── Dockerfile           # Standalone Next.js build
│
├── 📁 mobile/               # Flutter Mobile App
│   ├── lib/
│   │   ├── core/            # API client, theming, routing
│   │   ├── features/        # Auth, Dashboard, Inventory, Orders
│   │   └── shared/          # Providers, Models
│   └── pubspec.yaml
│
├── 📁 bot/                  # Telegram Bot (Python)
│   ├── bot/
│   │   └── main.py          # Bot handlers
│   └── Dockerfile           # Alpine-based image
│
├── 📄 docker-compose.yml    # Local development
├── 📄 docker-compose.prod.yml # Production dengan resource limits
├── 📄 setup-env.sh          # Interactive environment setup
├── 📄 check-deps.sh         # Dependency checker
├── 📄 DEMO_SCRIPT.md        # Panduan demo 7 menit
├── 📄 DEPLOY.md             # Deploy guide (Railway + Vercel)
└── 📄 README.md             # File ini
```

---

## 🤝 Kontribusi

Kontribusi sangat kami sambut! Silakan:

1. Fork repository ini
2. Buat branch fitur: `git checkout -b feature/nama-fitur`
3. Commit perubahan: `git commit -m 'feat: tambah fitur X'`
4. Push ke branch: `git push origin feature/nama-fitur`
5. Buat Pull Request

### Konvensi Commit
```
feat: tambah fitur baru
fix: perbaiki bug
docs: update dokumentasi
test: tambah/update tests
refactor: refactor kode
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
*Dibuat dengan ❤️ oleh Mas Obets Dev

