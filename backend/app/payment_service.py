import os
import base64
import logging
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.config import settings
from app.models.order import OrderModel
from app.models.product_service import ProductServiceModel
from app.models.stock_movement import StockMovementModel
from app.models.notification import NotificationModel

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app.payment_service")

# Menentukan URL dasar Midtrans Snap API berdasarkan status mode lingkungan
MIDTRANS_SANDBOX_URL = "https://app.sandbox.midtrans.com/snap/v1/transactions"
MIDTRANS_PRODUCTION_URL = "https://app.midtrans.com/snap/v1/transactions"

# Setup Redis client jika tersedia untuk pengecekan idempotensi
redis_client = None
try:
    import redis
    if settings.redis_url:
        redis_client = redis.from_url(settings.redis_url, decode_responses=True)
except Exception as e:
    logger.warning(f"Koneksi Redis untuk idempotensi pembayaran tidak tersedia: {str(e)}")

_in_memory_processed_payments = set()

def _get_midtrans_headers() -> Dict[str, str]:
    """
    Menghasilkan header autentikasi Basic Auth yang dibutuhkan oleh Midtrans Snap API.
    """
    server_key = settings.midtrans_server_key or "your_midtrans_server_key_here"
    auth_bytes = f"{server_key}:".encode("utf-8")
    auth_base64 = base64.b64encode(auth_bytes).decode("utf-8")
    
    return {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_base64}"
    }

async def send_telegram_notification(message: str) -> bool:
    """
    Mengirim notifikasi asinkron ke bot Telegram owner toko.
    """
    token = settings.telegram_bot_token
    chat_id = os.getenv("TELEGRAM_CHAT_ID") or os.getenv("OWNER_CHAT_ID")

    if not token or token == "your_telegram_bot_token_here" or not chat_id:
        logger.warning("Notifikasi Telegram dilewati karena token/chat_id belum dikonfigurasi.")
        return False

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "HTML"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, timeout=10.0)
            return response.status_code == 200
    except Exception as e:
        logger.error(f"Gagal mengirim notifikasi Telegram: {str(e)}")
        return False

async def create_payment_link(order: OrderModel, store_info: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
    """
    Membuat tautan pembayaran snap Midtrans asinkron berdasarkan order belanja multi-item.
    Mendukung VA, GoPay, OVO, Dana, ShopeePay, QRIS, CC, Indomaret, Alfamart.
    """
    logger.info(f"Memulai pembuatan link pembayaran Midtrans untuk Order ID: {order.id}, Total: Rp {order.total:,.0f}")
    
    now_utc = datetime.now(timezone.utc)
    expired_hours = store_info.get("expired_hours", 24)
    expired_at = (now_utc + timedelta(hours=expired_hours)).isoformat()
    
    fallback_response = {
        "snap_token": f"mock-token-{order.id}",
        "payment_url": f"https://app.sandbox.midtrans.com/snap/v2/vtweb/mock-token-{order.id}",
        "expired_at": expired_at,
        "order_id": order.id,
        "error": "Menggunakan tautan simulasi (Midtrans Credentials Belum Aktif)."
    }

    # Tarik detail item untuk dikirim ke Midtrans
    midtrans_items = []
    for item in order.items:
        p_res = await db.execute(select(ProductServiceModel).where(ProductServiceModel.id == item["product_id"]))
        product = p_res.scalars().first()
        name = product.name if product else f"Item {item['product_id'][:8]}"
        
        midtrans_items.append({
            "id": item["product_id"],
            "price": int(item["price"]),
            "quantity": item["qty"],
            "name": name[:50] # batas karakter nama midtrans
        })

    # Tambahkan diskon jika ada
    if order.discount > 0:
        midtrans_items.append({
            "id": "discount",
            "price": -int(order.discount),
            "quantity": 1,
            "name": "Diskon Belanja"
        })

    is_prod = settings.midtrans_is_production
    snap_url = MIDTRANS_PRODUCTION_URL if is_prod else MIDTRANS_SANDBOX_URL

    payload = {
        "transaction_details": {
            "order_id": order.id,
            "gross_amount": int(order.total)
        },
        "item_details": midtrans_items,
        "expiry": {
            "duration": expired_hours * 60,
            "unit": "minutes"
        },
        "credit_card": {"secure": True},
        "enabled_payments": [
            "credit_card", "bca_va", "bni_va", "bri_va", "other_va",
            "gopay", "shopeepay", "qris", "indomaret", "alfamart"
        ]
    }

    try:
        headers = _get_midtrans_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(snap_url, json=payload, headers=headers, timeout=15.0)
            if response.status_code in [200, 201]:
                res_data = response.json()
                logger.info(f"Link pembayaran Midtrans berhasil dibuat untuk Order ID: {order.id}.")
                return {
                    "snap_token": res_data.get("token"),
                    "payment_url": res_data.get("redirect_url"),
                    "expired_at": expired_at,
                    "order_id": order.id
                }
            else:
                logger.error(f"Gagal menghubungi Midtrans Snap API. HTTP {response.status_code}: {response.text}")
                return fallback_response
    except Exception as e:
        logger.error(f"Error Snap API: {str(e)}", exc_info=True)
        return fallback_response

async def create_quick_payment_link(amount: float, description: str, customer: Dict[str, Any]) -> Dict[str, Any]:
    """
    Membuat link pembayaran cepat instan (tanpa harus mendaftarkan order di database).
    Sangat berguna untuk transaksi kasir/toko langsung maupun pembayaran jasa kilat.
    """
    quick_id = f"quick-{secrets.token_hex(6)}"
    logger.info(f"Membuat link pembayaran cepat ID: {quick_id}, Nominal: Rp {amount:,.0f}")
    
    now_utc = datetime.now(timezone.utc)
    expired_at = (now_utc + timedelta(hours=24)).isoformat()
    
    fallback_response = {
        "payment_url": f"https://app.sandbox.midtrans.com/snap/v2/vtweb/mock-quick-{quick_id}",
        "expired_at": expired_at,
        "error": "Menggunakan tautan simulasi quick payment."
    }

    is_prod = settings.midtrans_is_production
    snap_url = MIDTRANS_PRODUCTION_URL if is_prod else MIDTRANS_SANDBOX_URL

    payload = {
        "transaction_details": {
            "order_id": quick_id,
            "gross_amount": int(amount)
        },
        "item_details": [{
            "id": "quick-pay",
            "price": int(amount),
            "quantity": 1,
            "name": description[:50]
        }],
        "customer_details": {
            "first_name": customer.get("name", "Pelanggan Jasa"),
            "phone": customer.get("phone", "")
        },
        "expiry": {
            "duration": 1440,
            "unit": "minutes"
        }
    }

    try:
        headers = _get_midtrans_headers()
        async with httpx.AsyncClient() as client:
            response = await client.post(snap_url, json=payload, headers=headers, timeout=15.0)
            if response.status_code in [200, 201]:
                res_data = response.json()
                return {
                    "payment_url": res_data.get("redirect_url"),
                    "expired_at": expired_at
                }
            return fallback_response
    except Exception as e:
        logger.error(f"Error Quick Snap API: {str(e)}")
        return fallback_response

def verify_webhook_signature(notification: Dict[str, Any], server_key: str) -> bool:
    """
    Memverifikasi keaslian signature key SHA512 yang dikirim oleh Midtrans untuk keamanan.
    """
    order_id = notification.get("order_id")
    status_code = notification.get("status_code")
    gross_amount = notification.get("gross_amount")
    signature_key = notification.get("signature_key")

    if not (order_id and status_code and gross_amount and signature_key):
        return False

    payload_str = f"{order_id}{status_code}{gross_amount}{server_key}"
    calculated_signature = hashlib.sha512(payload_str.encode("utf-8")).hexdigest()
    return calculated_signature == signature_key

async def handle_payment_notification(notification: Dict[str, Any], db: AsyncSession) -> Dict[str, Any]:
    """
    Memproses webhook notifikasi status dari Midtrans secara asinkron.
    Idempotensi dilindungi menggunakan Redis (pencegahan penanganan duplikat).
    Jika status dibatalkan/expired, stok barang fisik akan dikembalikan (restored).
    """
    order_id = notification.get("order_id", "")
    transaction_status = notification.get("transaction_status", "")
    transaction_id = notification.get("transaction_id", "")
    payment_type = notification.get("payment_type", "")
    
    logger.info(f"Memproses notifikasi pembayaran Order ID: {order_id}, Status: {transaction_status}")

    if not order_id:
        return {"error": "Order ID tidak ditemukan dalam notifikasi."}

    # 1. Pengecekan Idempotensi (Cegah notifikasi ganda diproses ulang)
    cache_key = f"payment_processed:{transaction_id}:{transaction_status}"
    if redis_client:
        try:
            if redis_client.get(cache_key):
                logger.info(f"Idempotensi: Transaksi {transaction_id} dengan status {transaction_status} sudah pernah diproses.")
                return {"order_id": order_id, "message": "Sudah diproses sebelumnya (Redis cache hit).", "action_taken": "none"}
        except Exception as e:
            logger.error(f"Idempotency cache fetch error: {str(e)}")
    else:
        if cache_key in _in_memory_processed_payments:
            return {"order_id": order_id, "message": "Sudah diproses sebelumnya (In-Memory hit).", "action_taken": "none"}

    # 2. Ambil pesanan dari DB
    result = await db.execute(select(OrderModel).where(OrderModel.id == order_id))
    order = result.scalars().first()
    
    if not order:
        return {"error": f"Order {order_id} tidak ditemukan di database."}

    # 3. Pemetaan status
    new_payment_status = "unpaid"
    new_order_status = "pending"
    action_taken = "none"
    is_success = False

    if transaction_status in ["capture", "settlement"]:
        new_payment_status = "paid"
        new_order_status = "confirmed"
        is_success = True
    elif transaction_status in ["deny", "expire", "cancel"]:
        new_payment_status = "unpaid"
        new_order_status = "cancelled"
        
        # 4. RESTOCK LOGIC: Kembalikan persediaan produk fisik jika order batal/kadaluarsa
        if order.status != "cancelled":
            for item in order.items:
                p_res = await db.execute(select(ProductServiceModel).where(ProductServiceModel.id == item["product_id"]))
                product = p_res.scalars().first()
                
                # Kembalikan stok jika bertipe produk fisik
                if product and product.type == "product":
                    if product.stock is not None:
                        product.stock += item["qty"]
                        
                    # Catat log pemulihan stok
                    movement = StockMovementModel(
                        product_id=product.id,
                        type="in",
                        qty=item["qty"],
                        note=f"Pemulihan Stok - Order Batal #{order.id[:8]}"
                    )
                    db.add(movement)
            action_taken = "restocked"
    elif transaction_status == "refund":
        new_payment_status = "refunded"
        new_order_status = "cancelled"

    # 5. Lakukan update status DB dengan retry logic sederhana
    retry_count = 3
    while retry_count > 0:
        try:
            order.payment_status = new_payment_status
            order.status = new_order_status
            
            # Tambah notifikasi internal toko jika lunas
            if is_success:
                notif = NotificationModel(
                    user_id=order.user_id,
                    type="order",
                    title="Pembayaran Berhasil! 💰",
                    message=f"Invoice #{order.id[:8]} telah lunas dibayar via {payment_type.upper() or 'QRIS/VA'} senilai Rp {order.total:,.0f}."
                )
                db.add(notif)
                
            await db.commit()
            break
        except Exception as db_error:
            retry_count -= 1
            logger.error(f"Gagal melakukan pembaruan status ke DB. Mengulang kembali... Sisa: {retry_count}. Detail: {str(db_error)}")
            await db.rollback()
            if retry_count == 0:
                return {"error": "Database update failed after maximum retries."}

    # 6. Kirim notifikasi Telegram ke owner toko jika lunas (settlement)
    if is_success:
        formatted_amount = f"Rp {order.total:,.0f}"
        telegram_msg = (
            f"👻 <b>DEDEMIT UMKM: PEMBAYARAN LUNAS!</b> 👻\n\n"
            f"Bisnis Kakak makin cuan! Pembayaran sukses masuk:\n"
            f"• <b>Order ID:</b> <code>{order.id}</code>\n"
            f"• <b>Nominal:</b> {formatted_amount}\n"
            f"• <b>Metode:</b> {payment_type.upper() if payment_type else 'QRIS/VA/E-wallet'}\n"
            f"• <b>Status:</b> SETTLEMENT\n\n"
            f"🔥 <i>Yuk, buruan diproses dan dikirimkan pesanan pelanggan agar mereka puas belanja di toko Kakak! Mantap!</i> 👍"
        )
        await send_telegram_notification(telegram_msg)

    # 7. Tandai transaksi telah diproses pada cache
    if redis_client:
        try:
            redis_client.setex(cache_key, 86400, "1") # Expire 24 jam
        except Exception as e:
            logger.error(f"Redis set idempotency error: {str(e)}")
    else:
        _in_memory_processed_payments.add(cache_key)

    return {
        "order_id": order_id,
        "new_status": new_order_status,
        "message": f"Notifikasi Midtrans berhasil diproses. Status transaksi: {transaction_status}",
        "action_taken": action_taken
    }
