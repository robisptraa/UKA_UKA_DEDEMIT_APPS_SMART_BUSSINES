#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# Dedemit OS — Setup Environment Script
# Guided interactive setup untuk semua .env variables dengan validasi
# ═══════════════════════════════════════════════════════════════════════════════
set -e

# ── Colors ───────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Banner ────────────────────────────────────────────────────────────────────
clear
echo -e "${CYAN}${BOLD}"
echo "  ██████╗ ███████╗██████╗ ███████╗███╗   ███╗██╗████████╗"
echo "  ██╔══██╗██╔════╝██╔══██╗██╔════╝████╗ ████║██║╚══██╔══╝"
echo "  ██║  ██║█████╗  ██║  ██║█████╗  ██╔████╔██║██║   ██║   "
echo "  ██║  ██║██╔══╝  ██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║   "
echo "  ██████╔╝███████╗██████╔╝███████╗██║ ╚═╝ ██║██║   ██║   "
echo "  ╚═════╝ ╚══════╝╚═════╝ ╚══════╝╚═╝     ╚═╝╚═╝   ╚═╝   "
echo -e "${RESET}"
echo -e "${BOLD}  👻 Dedemit OS — Environment Setup Wizard${RESET}"
echo -e "  AI Business Operating System untuk UMKM Indonesia"
echo ""
echo -e "${YELLOW}  Tekan ENTER untuk menggunakan nilai default (ditampilkan dalam [])${RESET}"
echo ""

# ── Helper Functions ──────────────────────────────────────────────────────────
ask() {
    local var_name="$1"
    local prompt="$2"
    local default="$3"
    local is_secret="${4:-false}"

    if [ "$is_secret" = "true" ]; then
        echo -ne "  ${BLUE}${prompt}${RESET} ${YELLOW}[${default:+******}${default:-(kosong)}]${RESET}: "
        read -rs value
        echo ""
    else
        echo -ne "  ${BLUE}${prompt}${RESET} ${YELLOW}[${default:-(kosong)}]${RESET}: "
        read -r value
    fi

    if [ -z "$value" ]; then
        value="$default"
    fi

    eval "$var_name='$value'"
}

validate_not_empty() {
    local val="$1"
    local name="$2"
    if [ -z "$val" ]; then
        echo -e "  ${RED}⚠️  $name tidak boleh kosong untuk production!${RESET}"
        return 1
    fi
    return 0
}

section() {
    echo ""
    echo -e "${CYAN}${BOLD}── $1 ──────────────────────────────────────────${RESET}"
}

# ── Check existing .env ───────────────────────────────────────────────────────
ENV_FILE=".env"
if [ -f "$ENV_FILE" ]; then
    echo -e "  ${YELLOW}⚠️  File .env sudah ada.${RESET}"
    echo -ne "  Timpa file yang ada? [y/N]: "
    read -r overwrite
    if [[ ! "$overwrite" =~ ^[Yy]$ ]]; then
        echo -e "  ${GREEN}✅ Setup dibatalkan. File .env tidak diubah.${RESET}"
        exit 0
    fi
    cp "$ENV_FILE" "${ENV_FILE}.backup.$(date +%Y%m%d_%H%M%S)"
    echo -e "  ${GREEN}💾 Backup disimpan ke ${ENV_FILE}.backup.$(date +%Y%m%d_%H%M%S)${RESET}"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 1: Environment
# ═══════════════════════════════════════════════════════════════════════════════
section "1. Environment"
ask ENV "Environment (development/production)" "development"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 2: Database
# ═══════════════════════════════════════════════════════════════════════════════
section "2. Database PostgreSQL"
echo -e "  ${YELLOW}💡 Untuk Railway: salin DATABASE_URL dari tab Variables${RESET}"
ask POSTGRES_USER "PostgreSQL Username" "dedemit"
ask POSTGRES_PASSWORD "PostgreSQL Password" "dedemit_secret_2024" "true"
ask POSTGRES_DB "PostgreSQL Database Name" "dedemit_db"
DATABASE_URL="postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@localhost:5432/${POSTGRES_DB}"
echo -e "  ${GREEN}✅ DATABASE_URL: postgresql://${POSTGRES_USER}:***@localhost:5432/${POSTGRES_DB}${RESET}"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 3: Redis
# ═══════════════════════════════════════════════════════════════════════════════
section "3. Redis"
echo -e "  ${YELLOW}💡 Untuk Railway: salin REDIS_URL dari service Redis${RESET}"
ask REDIS_URL "Redis URL" "redis://localhost:6379/0"
ask REDIS_PASSWORD "Redis Password (kosongkan jika tidak ada)" ""

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 4: Security
# ═══════════════════════════════════════════════════════════════════════════════
section "4. Security Secrets"
echo -e "  ${YELLOW}💡 JWT Secret: gunakan string random minimal 32 karakter${RESET}"
DEFAULT_JWT=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || echo "change_this_jwt_secret_in_production_$(date +%s)")
ask JWT_SECRET "JWT Secret Key" "$DEFAULT_JWT" "true"
DEFAULT_NEXTAUTH=$(python3 -c "import secrets; print(secrets.token_hex(32))" 2>/dev/null || echo "change_this_nextauth_secret_$(date +%s)")
ask NEXTAUTH_SECRET "NextAuth Secret Key" "$DEFAULT_NEXTAUTH" "true"
ask NEXTAUTH_URL "NextAuth URL (URL web kamu)" "http://localhost:3000"

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 5: AI API Keys
# ═══════════════════════════════════════════════════════════════════════════════
section "5. AI API Keys"
echo -e "  ${YELLOW}💡 Minimal 1 AI key diperlukan untuk fitur scanner produk${RESET}"
echo -e "  ${YELLOW}   Google Gemini: https://aistudio.google.com/apikey${RESET}"
echo -e "  ${YELLOW}   Anthropic Claude: https://console.anthropic.com${RESET}"
ask GEMINI_API_KEY "Google Gemini API Key" ""
ask ANTHROPIC_API_KEY "Anthropic (Claude) API Key" ""

if [ -z "$GEMINI_API_KEY" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
    echo -e "  ${YELLOW}⚠️  Tidak ada AI key — fitur AI akan berjalan dalam mode simulasi${RESET}"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 6: Midtrans Payment Gateway
# ═══════════════════════════════════════════════════════════════════════════════
section "6. Midtrans Payment Gateway"
echo -e "  ${YELLOW}💡 Daftar di: https://dashboard.midtrans.com${RESET}"
echo -e "  ${YELLOW}   Settings → Access Keys → Server Key & Client Key${RESET}"
ask MIDTRANS_SERVER_KEY "Midtrans Server Key" ""
ask MIDTRANS_CLIENT_KEY "Midtrans Client Key" ""
ask MIDTRANS_IS_PRODUCTION "Midtrans Mode Production? (true/false)" "false"

if [ -n "$MIDTRANS_SERVER_KEY" ]; then
    BACKEND_URL="${NEXTAUTH_URL/3000/8000}"
    echo ""
    echo -e "  ${CYAN}${BOLD}📋 Setup Midtrans Webhook:${RESET}"
    echo -e "  1. Login ke https://dashboard.midtrans.com"
    echo -e "  2. Settings → Configuration"
    echo -e "  3. Notification URL: ${GREEN}${BACKEND_URL}/api/v1/webhooks/midtrans${RESET}"
    echo -e "  4. Centang: Payment & Refund notifications"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# SECTION 7: Telegram Bot
# ═══════════════════════════════════════════════════════════════════════════════
section "7. Telegram Bot"
echo -e "  ${YELLOW}💡 Buat bot via @BotFather di Telegram → /newbot${RESET}"
ask TELEGRAM_BOT_TOKEN "Telegram Bot Token" ""

if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    BACKEND_URL="${NEXTAUTH_URL/3000/8000}"
    echo ""
    echo -e "  ${CYAN}${BOLD}📋 Setup Telegram Webhook (setelah deploy):${RESET}"
    echo -e "  Jalankan command ini:"
    echo -e "  ${GREEN}curl -X POST https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/setWebhook \\"
    echo -e "    -d url=${BACKEND_URL}/api/v1/webhooks/telegram${RESET}"
fi

# ═══════════════════════════════════════════════════════════════════════════════
# WRITE .env FILE
# ═══════════════════════════════════════════════════════════════════════════════
echo ""
echo -e "${CYAN}${BOLD}── Menulis file .env ────────────────────────────────────${RESET}"

cat > "$ENV_FILE" << EOF
# ═══════════════════════════════════════════════════════════════
# Dedemit OS — Environment Variables
# Generated by setup-env.sh pada $(date)
# ⚠️  JANGAN commit file ini ke Git!
# ═══════════════════════════════════════════════════════════════

# Environment
ENV=${ENV}

# ── Database ─────────────────────────────────────────────────
POSTGRES_USER=${POSTGRES_USER}
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
POSTGRES_DB=${POSTGRES_DB}
DATABASE_URL=${DATABASE_URL}

# ── Redis ─────────────────────────────────────────────────────
REDIS_URL=${REDIS_URL}
REDIS_PASSWORD=${REDIS_PASSWORD}

# ── Security ──────────────────────────────────────────────────
JWT_SECRET=${JWT_SECRET}
NEXTAUTH_SECRET=${NEXTAUTH_SECRET}
NEXTAUTH_URL=${NEXTAUTH_URL}

# ── AI API Keys ───────────────────────────────────────────────
GEMINI_API_KEY=${GEMINI_API_KEY}
ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}

# ── Midtrans Payment Gateway ──────────────────────────────────
MIDTRANS_SERVER_KEY=${MIDTRANS_SERVER_KEY}
MIDTRANS_CLIENT_KEY=${MIDTRANS_CLIENT_KEY}
MIDTRANS_IS_PRODUCTION=${MIDTRANS_IS_PRODUCTION}

# ── Telegram Bot ──────────────────────────────────────────────
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}

# ── Next.js Public ────────────────────────────────────────────
NEXT_PUBLIC_API_URL=http://localhost:8000
EOF

echo -e "  ${GREEN}✅ File .env berhasil dibuat!${RESET}"

# ── Copy .env untuk backend ───────────────────────────────────
cp "$ENV_FILE" backend/.env
echo -e "  ${GREEN}✅ Disalin ke backend/.env${RESET}"

echo ""
echo -e "${GREEN}${BOLD}══════════════════════════════════════════════════════"
echo -e "  🎉 Setup selesai! Langkah selanjutnya:"
echo -e "══════════════════════════════════════════════════════${RESET}"
echo ""
echo -e "  ${BOLD}1. Jalankan dependency check:${RESET}"
echo -e "     ${CYAN}bash check-deps.sh${RESET}"
echo ""
echo -e "  ${BOLD}2. Jalankan semua service:${RESET}"
echo -e "     ${CYAN}docker-compose up --build -d${RESET}"
echo ""
echo -e "  ${BOLD}3. Isi database dengan data demo:${RESET}"
echo -e "     ${CYAN}cd backend && python seed_demo_data.py${RESET}"
echo ""
echo -e "  ${BOLD}4. Akses aplikasi:${RESET}"
echo -e "     Web Dashboard: ${CYAN}http://localhost:3000${RESET}"
echo -e "     API Backend:   ${CYAN}http://localhost:8000${RESET}"
echo -e "     API Docs:      ${CYAN}http://localhost:8000/docs${RESET}"
echo ""
