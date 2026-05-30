#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════════════════════
# Dedemit OS — Dependency Checker
# Verifikasi semua dependency tersedia sebelum menjalankan aplikasi
# ═══════════════════════════════════════════════════════════════════════════════

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

PASS=0
FAIL=0

check() {
    local name="$1"
    local cmd="$2"
    local min_ver="$3"

    if eval "$cmd" &>/dev/null; then
        echo -e "  ${GREEN}✅ $name${RESET}"
        ((PASS++))
        return 0
    else
        echo -e "  ${RED}❌ $name — TIDAK DITEMUKAN${RESET}"
        if [ -n "$min_ver" ]; then
            echo -e "     ${YELLOW}💡 Install: $min_ver${RESET}"
        fi
        ((FAIL++))
        return 1
    fi
}

check_port() {
    local port="$1"
    local service="$2"

    if lsof -ti :"$port" &>/dev/null; then
        echo -e "  ${YELLOW}⚠️  Port $port sedang dipakai (butuh untuk $service)${RESET}"
        lsof -ti :"$port" | xargs ps -p 2>/dev/null | tail -1 | awk '{print "     PID:", $1, "→", $NF}'
        ((FAIL++))
    else
        echo -e "  ${GREEN}✅ Port $port tersedia ($service)${RESET}"
        ((PASS++))
    fi
}

echo ""
echo -e "${CYAN}${BOLD}══════════════════════════════════════════════════════"
echo -e "  👻 Dedemit OS — Dependency Check"
echo -e "══════════════════════════════════════════════════════${RESET}"
echo ""

# ── Core Tools ────────────────────────────────────────────────────────────────
echo -e "${BOLD}🛠  Core Tools:${RESET}"
check "Docker" "docker --version" "https://docs.docker.com/get-docker/"
check "Docker Compose" "docker compose version || docker-compose --version" "Bundled dengan Docker Desktop"
check "Git" "git --version" "https://git-scm.com"
echo ""

# ── Runtime ───────────────────────────────────────────────────────────────────
echo -e "${BOLD}🐍 Runtime:${RESET}"
check "Python 3.11+" "python3 --version | grep -E '3\.(11|12|13)'" "https://www.python.org/downloads/"
check "Node.js 18+" "node --version | grep -E 'v(18|19|20|21|22)'" "https://nodejs.org"
check "pip" "pip3 --version"
check "npm" "npm --version"
echo ""

# ── Ports ─────────────────────────────────────────────────────────────────────
echo -e "${BOLD}🔌 Port Availability:${RESET}"
check_port 8000 "FastAPI Backend"
check_port 3000 "Next.js Web"
check_port 5432 "PostgreSQL"
check_port 6379 "Redis"
echo ""

# ── .env Check ────────────────────────────────────────────────────────────────
echo -e "${BOLD}📝 Environment Files:${RESET}"
if [ -f ".env" ]; then
    echo -e "  ${GREEN}✅ .env ditemukan${RESET}"
    ((PASS++))
    
    # Check critical vars
    source .env 2>/dev/null || true
    
    if [ -n "$JWT_SECRET" ] && [ "$JWT_SECRET" != "change_this_jwt_secret_in_production" ]; then
        echo -e "  ${GREEN}✅ JWT_SECRET dikonfigurasi${RESET}"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠️  JWT_SECRET belum dikonfigurasi dengan benar${RESET}"
        ((FAIL++))
    fi

    if [ -n "$GEMINI_API_KEY" ] || [ -n "$ANTHROPIC_API_KEY" ]; then
        echo -e "  ${GREEN}✅ AI API Key tersedia${RESET}"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠️  Tidak ada AI Key — fitur AI berjalan mode simulasi${RESET}"
    fi

    if [ -n "$MIDTRANS_SERVER_KEY" ]; then
        echo -e "  ${GREEN}✅ Midtrans dikonfigurasi${RESET}"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠️  Midtrans belum dikonfigurasi — pembayaran berjalan mode simulasi${RESET}"
    fi
else
    echo -e "  ${RED}❌ .env tidak ditemukan${RESET}"
    echo -e "     ${YELLOW}💡 Jalankan: bash setup-env.sh${RESET}"
    ((FAIL++))
fi
echo ""

# ── Docker Health ─────────────────────────────────────────────────────────────
echo -e "${BOLD}🐳 Docker Status:${RESET}"
if docker info &>/dev/null; then
    echo -e "  ${GREEN}✅ Docker daemon berjalan${RESET}"
    ((PASS++))
    
    # Check available disk space
    DOCKER_ROOT=$(docker info --format '{{.DockerRootDir}}' 2>/dev/null || echo "/var/lib/docker")
    AVAILABLE_GB=$(df -BG "$DOCKER_ROOT" 2>/dev/null | awk 'NR==2{print $4}' | sed 's/G//' || echo "?")
    if [ "$AVAILABLE_GB" != "?" ] && [ "$AVAILABLE_GB" -gt 2 ]; then
        echo -e "  ${GREEN}✅ Disk space tersedia: ${AVAILABLE_GB}GB${RESET}"
        ((PASS++))
    else
        echo -e "  ${YELLOW}⚠️  Disk space mungkin tidak cukup (tersedia: ${AVAILABLE_GB}GB, minimal 2GB)${RESET}"
    fi
else
    echo -e "  ${RED}❌ Docker daemon tidak berjalan — jalankan Docker Desktop${RESET}"
    ((FAIL++))
fi
echo ""

# ── Summary ───────────────────────────────────────────────────────────────────
TOTAL=$((PASS + FAIL))
echo -e "${BOLD}══════════════════════════════════════════════════════${RESET}"
echo -e "  Hasil: ${GREEN}${PASS} OK${RESET} / ${RED}${FAIL} GAGAL${RESET} dari ${TOTAL} checks"

if [ "$FAIL" -eq 0 ]; then
    echo ""
    echo -e "  ${GREEN}${BOLD}🎉 Semua dependency siap! Jalankan:${RESET}"
    echo -e "  ${CYAN}  docker-compose up --build -d${RESET}"
else
    echo ""
    echo -e "  ${YELLOW}⚠️  Ada ${FAIL} masalah yang perlu diselesaikan dahulu.${RESET}"
    echo -e "     Lihat instruksi di atas dan perbaiki sebelum menjalankan aplikasi."
fi
echo ""
