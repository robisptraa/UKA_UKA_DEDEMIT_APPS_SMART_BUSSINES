from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

from app.database import get_async_db
from app.models.order import OrderModel
from app.payment_service import create_payment_link, create_quick_payment_link, verify_webhook_signature, handle_payment_notification
from app.security import get_current_user
from app.models.user import UserModel
from app.config import settings

router = APIRouter(prefix="/payment", tags=["Payments & Cashier"])

# Pydantic validation schemas
class CreateLinkRequest(BaseModel):
    order_id: str = Field(..., description="ID pemesanan yang ingin dibuat link pembayarannya")
    expired_hours: Optional[int] = Field(24, description="Masa kedaluwarsa tautan pembayaran dalam jam")

class QuickLinkRequest(BaseModel):
    amount: float = Field(..., gt=0, description="Nominal pembayaran langsung")
    description: str = Field(..., description="Deskripsi singkat transaksi pembayaran jasa/produk langsung")
    customer_name: Optional[str] = Field("Pelanggan", description="Nama pembeli/pelanggan")
    customer_phone: Optional[str] = Field("", description="Nomor telepon pelanggan")

@router.post("/create-link")
async def make_payment_link(
    req: CreateLinkRequest,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Membuat tautan Snap pembayaran Midtrans baru untuk order terdaftar secara asinkron.
    Hanya dapat dipicu jika order merupakan milik toko owner yang aktif.
    """
    # 1. Cari pesanan di database
    result = await db.execute(
        select(OrderModel).where(OrderModel.id == req.order_id, OrderModel.user_id == current_user.id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pemesanan tidak ditemukan atau Anda tidak memiliki otorisasi keamanan."
        )

    # 2. Buat payment link via Midtrans SNAP API
    store_info = {"expired_hours": req.expired_hours}
    payment_data = await create_payment_link(order, store_info, db)
    
    # 3. Update payment token pada order jika link sukses terbuat
    if "snap_token" in payment_data and not payment_data.get("error"):
        order.payment_token = payment_data["snap_token"]
        db.add(order)
        await db.commit()

    return payment_data

@router.post("/quick-link")
async def make_quick_link(
    req: QuickLinkRequest,
    current_user: UserModel = Depends(get_current_user)
):
    """
    Membuat tautan pembayaran instan cepat secara asinkron (tanpa mencatat order formal ke sistem DB).
    Sangat berguna untuk proses kasir instan, jasa potong rambut salon, jasa cuci laundry, maupun servis motor langsung.
    """
    customer_data = {
        "name": req.customer_name,
        "phone": req.customer_phone
    }
    link_data = await create_quick_payment_link(req.amount, req.description, customer_data)
    return link_data

@router.get("/{order_id}/status")
async def check_payment_status(
    order_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengecek status pembayaran pesanan secara asinkron di sistem database.
    """
    result = await db.execute(
        select(OrderModel).where(OrderModel.id == order_id, OrderModel.user_id == current_user.id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pemesanan tidak ditemukan atau Anda tidak memiliki akses."
        )

    return {
        "order_id": order.id,
        "status": order.status,
        "payment_status": order.payment_status,
        "payment_method": order.payment_method,
        "total": order.total,
        "created_at": order.created_at
    }

# Webhook Endpoint (Sebagai redundansi / kelengkapan rute di bawah /payment/webhook)
@router.post("/webhook")
async def midtrans_payment_webhook(
    request: Request,
    db: AsyncSession = Depends(get_async_db)
):
    """
    Rute cadangan webhook Midtrans yang memvalidasi SHA512 dan mendelegasikan pemrosesan notifikasi.
    """
    try:
        notification = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="JSON payload tidak valid.")

    server_key = settings.midtrans_server_key or "your_midtrans_server_key_here"
    if not verify_webhook_signature(notification, server_key):
        raise HTTPException(status_code=400, detail="Signature key verifikasi gagal.")

    result = await handle_payment_notification(notification, db)
    return result
