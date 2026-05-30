# 🚀 Panduan Deploy Dedemit OS ke Production

## Ringkasan Arsitektur Deploy

```
┌──────────────────────────────────────────────────────┐
│                    PRODUCTION                         │
│                                                       │
│  ┌─────────────┐      ┌──────────────────────────┐   │
│  │   VERCEL    │      │        RAILWAY            │   │
│  │             │      │                           │   │
│  │  Next.js    │ ────►│  FastAPI Backend (:8000)  │   │
│  │  Web App    │      │  Telegram Bot (worker)    │   │
│  │             │      │  PostgreSQL (managed)     │   │
│  └─────────────┘      │  Redis (managed)          │   │
│                       └──────────────────────────┘   │
└──────────────────────────────────────────────────────┘
```

---

## Part 1: Railway (Backend + Database + Bot)

### 1.1 Setup Akun Railway

1. Daftar/Login di [railway.app](https://railway.app)
2. Klik **"New Project"**
3. Pilih **"Deploy from GitHub repo"**
4. Pilih repo `uka-uka`

### 1.2 Setup PostgreSQL

1. Di project Railway, klik **"New Service"** → **"Database"** → **"PostgreSQL"**
2. Railway akan otomatis provisioning database
3. Klik service PostgreSQL → tab **"Variables"**
4. Salin nilai `DATABASE_URL` (format: `postgresql://user:pass@host:port/db`)

### 1.3 Setup Redis

1. Klik **"New Service"** → **"Database"** → **"Redis"**
2. Klik service Redis → tab **"Variables"**
3. Salin nilai `REDIS_URL`

### 1.4 Deploy Backend FastAPI

1. Klik **"New Service"** → **"GitHub Repo"**
2. Pilih repo `uka-uka`
3. Di **"Settings"** → **"Root Directory"**: set ke `backend`
4. Di tab **"Variables"**, tambahkan semua environment variables:

```bash
# ── Core ─────────────────────────────────────────────
ENV=production
DATABASE_URL=postgresql://...  # Dari service PostgreSQL di atas

# ── Redis ─────────────────────────────────────────────
REDIS_URL=redis://...           # Dari service Redis di atas

# ── Security ──────────────────────────────────────────
JWT_SECRET=your_very_long_random_secret_at_least_32_chars

# ── AI APIs ───────────────────────────────────────────
GEMINI_API_KEY=AIza...          # Dari Google AI Studio
ANTHROPIC_API_KEY=sk-ant-...    # Dari Anthropic Console (opsional)

# ── Midtrans ──────────────────────────────────────────
MIDTRANS_SERVER_KEY=SB-Mid-server-...   # Atau Mid-server- untuk production
MIDTRANS_CLIENT_KEY=SB-Mid-client-...
MIDTRANS_IS_PRODUCTION=false            # true untuk production Midtrans

# ── Telegram ──────────────────────────────────────────
TELEGRAM_BOT_TOKEN=123456789:ABC...

# ── CORS ──────────────────────────────────────────────
ALLOWED_ORIGINS=https://dedemit.vercel.app,https://your-custom-domain.com
```

5. Di **"Settings"** → **"Start Command"**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 2
   ```

6. Di **"Settings"** → **"Health Check Path"**: `/health`

7. Deploy akan otomatis berjalan → tunggu status **"Active"**

8. Catat URL backend: `https://your-service.up.railway.app`

### 1.5 Setup Telegram Bot (Worker Service)

1. Klik **"New Service"** → **"GitHub Repo"** (repo yang sama)
2. Di **"Settings"** → **"Root Directory"**: set ke `bot`
3. Di tab **"Variables"**:

```bash
TELEGRAM_BOT_TOKEN=123456789:ABC...
BACKEND_API_URL=https://your-backend.up.railway.app
ENV=production
```

4. Di **"Settings"** → **"Start Command"**:
   ```bash
   python -m bot.main
   ```

5. **Catatan:** Bot tidak perlu domain publik — dia menggunakan long-polling

### 1.6 Setup Webhook Midtrans (Setelah Backend Live)

1. Login ke [dashboard.midtrans.com](https://dashboard.midtrans.com)
2. **Settings** → **Configuration** → **Notification URL**
3. Masukkan:
   ```
   https://your-backend.up.railway.app/api/v1/webhooks/midtrans
   ```
4. Centang: **Payment**, **Refund**, **Dispute**
5. Klik **Save**

### 1.7 Run Database Migrations

Setelah backend deployed, jalankan via Railway CLI atau terminal:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Pilih project
railway link

# Jalankan migrasi Alembic
railway run -s backend -- alembic upgrade head

# Seed data demo
railway run -s backend -- python seed_demo_data.py
```

---

## Part 2: Vercel (Next.js Web Dashboard)

### 2.1 Setup Akun Vercel

1. Daftar/Login di [vercel.com](https://vercel.com)
2. Klik **"New Project"**
3. Import repo `uka-uka` dari GitHub

### 2.2 Konfigurasi Build

Di halaman setup project Vercel:

| Setting | Value |
|---------|-------|
| **Framework Preset** | Next.js |
| **Root Directory** | `web` |
| **Build Command** | `npm run build` |
| **Output Directory** | `.next` (auto-detect) |
| **Install Command** | `npm install` |

### 2.3 Environment Variables Vercel

Di tab **"Environment Variables"**, tambahkan:

```bash
# ── API Backend ───────────────────────────────────────
NEXT_PUBLIC_API_URL=https://your-backend.up.railway.app

# ── NextAuth ──────────────────────────────────────────
NEXTAUTH_URL=https://your-project.vercel.app  # Atau custom domain
NEXTAUTH_SECRET=your_nextauth_secret_at_least_32_chars

# ── Opsional ──────────────────────────────────────────
NEXT_PUBLIC_MIDTRANS_CLIENT_KEY=SB-Mid-client-...
```

### 2.4 Custom Domain (Opsional)

1. Di Vercel project → **"Settings"** → **"Domains"**
2. Klik **"Add Domain"**
3. Masukkan domain kamu (contoh: `dedemit.id`)
4. Ikuti instruksi DNS di registrar domain kamu:
   - Tambahkan `CNAME record`: `www` → `cname.vercel-dns.com`
   - Atau `A record`: `@` → `76.76.19.19`
5. Klik **"Verify"** — SSL otomatis digenerate

### 2.5 Deploy

Klik **"Deploy"** — Vercel akan:
1. Install dependencies
2. Build Next.js dengan `output: standalone`
3. Deploy ke CDN global

URL akan tersedia: `https://your-project.vercel.app`

---

## Part 3: Verifikasi Post-Deploy

### 3.1 Health Check Backend

```bash
curl https://your-backend.up.railway.app/health
```

Expected response:
```json
{
  "status": "healthy",
  "checks": {
    "database": {"status": "ok"},
    "redis": {"status": "ok"}
  }
}
```

### 3.2 Test Login API

```bash
curl -X POST https://your-backend.up.railway.app/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "bos@dedemit.id", "password": "Password123!"}'
```

### 3.3 Verify Web Dashboard

Buka `https://your-project.vercel.app` → Harus tampil landing page Dedemit.

---

## Part 4: Environment Variables Reference Lengkap

| Variable | Wajib | Deskripsi | Contoh |
|----------|-------|-----------|--------|
| `ENV` | ✅ | Mode aplikasi | `production` |
| `DATABASE_URL` | ✅ | PostgreSQL connection string | `postgresql://user:pass@host/db` |
| `REDIS_URL` | ✅ | Redis connection string | `redis://default:pass@host:6379` |
| `JWT_SECRET` | ✅ | Secret untuk JWT signing | String random 32+ karakter |
| `NEXTAUTH_SECRET` | ✅ | Secret untuk NextAuth | String random 32+ karakter |
| `NEXTAUTH_URL` | ✅ | URL web deployment | `https://dedemit.vercel.app` |
| `NEXT_PUBLIC_API_URL` | ✅ | URL backend (publik) | `https://backend.up.railway.app` |
| `GEMINI_API_KEY` | 🟡 | Google Gemini AI | `AIzaSy...` |
| `ANTHROPIC_API_KEY` | 🟡 | Claude AI (alternatif) | `sk-ant-...` |
| `MIDTRANS_SERVER_KEY` | 🟡 | Midtrans server key | `SB-Mid-server-...` |
| `MIDTRANS_CLIENT_KEY` | 🟡 | Midtrans client key | `SB-Mid-client-...` |
| `MIDTRANS_IS_PRODUCTION` | 🟡 | Mode Midtrans | `false` (sandbox) |
| `TELEGRAM_BOT_TOKEN` | 🟡 | Telegram bot token | `123456:ABC...` |
| `ALLOWED_ORIGINS` | 🟡 | CORS origins (comma-separated) | `https://dedemit.vercel.app` |

> ✅ = Wajib untuk fungsi dasar  
> 🟡 = Opsional, fitur terkait tidak aktif jika tidak diisi

---

## Part 5: Monitoring & Logs

### Railway Logs
```bash
railway logs -s backend --tail
```

### Vercel Logs
- Buka Vercel dashboard → Project → **"Deployments"** → klik deployment → **"Logs"**

### Health Check Monitoring
Setup UptimeRobot gratis untuk monitoring 24/7:
1. Daftar di [uptimerobot.com](https://uptimerobot.com)
2. Add monitor: `https://your-backend.up.railway.app/health`
3. Alert via email/Telegram jika down
