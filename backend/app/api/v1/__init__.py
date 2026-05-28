from fastapi import APIRouter

# Impor router individual
from app.api.v1.auth import router as auth_router
from app.api.v1.items import router as items_router
from app.api.v1.customers import router as customers_router
from app.api.v1.orders import router as orders_router
from app.api.v1.payments import router as payments_router
from app.api.v1.finance import router as finance_router
from app.api.v1.dashboard import router as dashboard_router
from app.api.v1.analytics import router as analytics_router
from app.api.v1.ocr import router as ocr_router
from app.api.v1.webhooks import router as webhooks_router
from app.api.v1.ai import router as ai_router

# Inisialisasi API router utama untuk versi 1 (v1)
router = APIRouter(prefix="/v1")

# Daftarkan sub-router ke router utama v1
router.include_router(auth_router)
router.include_router(items_router)
router.include_router(customers_router)
router.include_router(orders_router)
router.include_router(payments_router)
router.include_router(finance_router)
router.include_router(dashboard_router)
router.include_router(analytics_router)
router.include_router(ocr_router)
router.include_router(webhooks_router)
router.include_router(ai_router)
