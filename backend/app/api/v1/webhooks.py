from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.database import get_async_db
from app.config import settings
from app.payment_service import verify_webhook_signature, handle_payment_notification

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.webhooks")

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("/midtrans", status_code=status.HTTP_200_OK)
async def midtrans_webhook(
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    """
    FastAPI Webhook endpoint untuk menerima notifikasi status pembayaran dari Midtrans.
    Memverifikasi keaslian signature dan memperbarui status pesanan secara asinkron.
    """
    try:
        # 1. Parse payload JSON notifikasi
        notification = await request.json()
        logger.info(f"Webhook Midtrans diterima. Payload: {notification}")
    except Exception as parse_error:
        logger.error(f"Gagal mem-parse JSON payload webhook: {str(parse_error)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Payload JSON tidak valid."
        )

    # 2. Verifikasi signature key untuk menjamin keamanan dari fraud/replay attack
    server_key = settings.midtrans_server_key or "your_midtrans_server_key_here"
    signature_verified = verify_webhook_signature(notification, server_key)
    
    if not signature_verified:
        logger.warning("Upaya panggilan webhook gagal: Signature Key tidak cocok/tidak valid.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Verifikasi signature key gagal. Permintaan tidak diizinkan."
        )

    # 3. Proses notifikasi status pembayaran, update status pemesanan di database,
    # dan picu notifikasi Telegram ke owner.
    result = await handle_payment_notification(notification, db)
    
    logger.info(f"Selesai memproses webhook Midtrans: {result}")
    return result
