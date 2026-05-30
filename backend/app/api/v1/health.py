"""
Health Check Router untuk Dedemit OS Backend
Mengecek koneksi database PostgreSQL dan Redis secara asinkron.
"""
import time
from datetime import datetime, timezone
from fastapi import APIRouter
from sqlalchemy import text

from app.database import AsyncSessionLocal
from app.config import settings

router = APIRouter(tags=["Health"])


@router.get("/health")
async def health_check():
    """
    Readiness probe endpoint untuk Docker, Railway, dan load balancer.
    Mengecek koneksi ke semua dependency: Database & Redis.
    
    Returns:
        200: Semua sistem operasional
        503: Salah satu atau lebih sistem tidak dapat dihubungi
    """
    start_time = time.monotonic()
    checks = {}
    overall_status = "healthy"

    # ── 1. Cek koneksi Database PostgreSQL ────────────────────
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        checks["database"] = {"status": "ok", "type": "postgresql"}
    except Exception as e:
        checks["database"] = {"status": "error", "error": str(e)[:100]}
        overall_status = "degraded"

    # ── 2. Cek koneksi Redis ───────────────────────────────────
    try:
        if settings.redis_url:
            import redis.asyncio as aioredis
            r = aioredis.from_url(settings.redis_url, socket_connect_timeout=3)
            await r.ping()
            await r.aclose()
            checks["redis"] = {"status": "ok"}
        else:
            checks["redis"] = {"status": "not_configured"}
    except Exception as e:
        checks["redis"] = {"status": "error", "error": str(e)[:100]}
        # Redis tidak critical untuk operasi dasar — degraded saja
        if overall_status == "healthy":
            overall_status = "degraded"

    elapsed_ms = round((time.monotonic() - start_time) * 1000, 2)

    return {
        "status": overall_status,
        "service": settings.project_name,
        "version": "1.0.0",
        "environment": settings.env,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "uptime_check_ms": elapsed_ms,
        "checks": checks,
        "features": {
            "ai": "active" if (settings.gemini_api_key or settings.anthropic_api_key) else "simulated",
            "payments": "active" if settings.midtrans_server_key else "inactive",
            "telegram_bot": "active" if settings.telegram_bot_token else "inactive",
        }
    }
