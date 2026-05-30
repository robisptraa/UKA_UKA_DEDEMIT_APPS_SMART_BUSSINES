"""
Dedemit OS — Backend FastAPI Utama
AI Business Operating System untuk UMKM Indonesia
"""
import logging
import sys
import json
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings
from app.api.v1 import router as api_v1_router
from app.api.v1.health import router as health_router


# ─────────────────────────────────────────────────────────
# Structured JSON Logging (mudah di-parse di Railway/Datadog)
# ─────────────────────────────────────────────────────────
class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_object = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": "dedemit-backend",
            "environment": settings.env,
        }
        if record.exc_info:
            log_object["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_object, ensure_ascii=False)


def setup_logging():
    """Konfigurasi logging terstruktur JSON untuk production."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO if settings.env == "production" else logging.DEBUG)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # Kurangi noise dari library pihak ketiga
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


setup_logging()
logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────
# Lifespan Context (startup & shutdown hooks)
# ─────────────────────────────────────────────────────────
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Dedemit OS Backend dimulai — environment: %s", settings.env)
    yield
    logger.info("🛑 Dedemit OS Backend dihentikan.")


# ─────────────────────────────────────────────────────────
# Inisialisasi Aplikasi FastAPI
# ─────────────────────────────────────────────────────────
app = FastAPI(
    title="Dedemit OS — AI Business Backend",
    description=(
        "RESTful API Backend untuk Dedemit OS — "
        "AI-powered Business Operating System untuk UMKM Indonesia. "
        "Fitur: inventory AI, manajemen order, pembayaran Midtrans, "
        "Telegram Bot, dan analitik keuangan."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ─────────────────────────────────────────────────────────
# Middleware CORS
# ─────────────────────────────────────────────────────────
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost",
    "http://127.0.0.1",
]

# Di production, tambahkan domain Railway/Vercel yang sebenarnya
if settings.env == "production":
    # Ambil dari env var ALLOWED_ORIGINS jika ada (comma-separated)
    import os
    extra_origins = os.getenv("ALLOWED_ORIGINS", "").split(",")
    allowed_origins.extend([o.strip() for o in extra_origins if o.strip()])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins if settings.env == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─────────────────────────────────────────────────────────
# Request Logging Middleware
# ─────────────────────────────────────────────────────────
@app.middleware("http")
async def log_requests(request: Request, call_next):
    import time
    start = time.monotonic()
    response = await call_next(request)
    duration_ms = round((time.monotonic() - start) * 1000, 2)

    logger.info(
        "HTTP %s %s → %s (%.1fms)",
        request.method,
        request.url.path,
        response.status_code,
        duration_ms,
    )
    return response


# ─────────────────────────────────────────────────────────
# Root Endpoint (backward-compatible)
# ─────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "service": "Dedemit OS API",
        "version": "1.0.0",
        "environment": settings.env,
        "docs": "/docs",
        "health": "/health",
    }


# ─────────────────────────────────────────────────────────
# Register Routers
# ─────────────────────────────────────────────────────────
# Health endpoint di root level (bukan /api/v1) agar mudah diakses probe
app.include_router(health_router)

# Semua API v1 routes
app.include_router(api_v1_router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=(settings.env != "production"),
        log_config=None,  # Disable uvicorn default logging (gunakan kita punya)
    )
