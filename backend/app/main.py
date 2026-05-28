from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.v1 import router as api_v1_router

# Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title=settings.project_name,
    description="Main RESTful API Backend untuk Operasi AI Bisnis UMKM Thrift/Streetwear Indonesia (Uka-Uka)",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Konfigurasi CORS (Cross-Origin Resource Sharing)
# Mengizinkan integrasi Next.js (http://localhost:3000) dan Flutter client secara aman
allowed_origins = [
    "http://localhost:3000",  # Dashboard Next.js local
    "http://127.0.0.1:3000",
    # Flutter Web / Local Emulator Gateways
    "http://localhost",
    "http://127.0.0.1",
]

app.add_middleware(
    CORSMiddleware,
    # Di environment development, kami mengizinkan wildcard jika dibutuhkan,
    # namun kami mendaftarkan origin spesifik demi standar keamanan premium
    allow_origins=allowed_origins if settings.env == "production" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Daftarkan Router API versi 1 (v1)
app.include_router(api_v1_router, prefix="/api")

# Endpoint Healthcheck Utama
@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": settings.project_name,
        "environment": settings.env,
        "features": {
            "ai_integration": "active" if (settings.gemini_api_key or settings.anthropic_api_key) else "simulated",
            "payments_integration": "active" if settings.midtrans_server_key else "inactive"
        }
    }

if __name__ == "__main__":
    import uvicorn
    # Menjalankan uvicorn server pada port 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
