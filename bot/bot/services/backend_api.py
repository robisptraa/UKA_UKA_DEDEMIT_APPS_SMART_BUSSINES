import os
import logging
from typing import List, Dict, Any, Optional
import httpx

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("bot.backend_api")

# URL API Backend dibaca dari environment variable (default localhost:8000)
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

async def fetch_products() -> List[Dict[str, Any]]:
    """
    Mengambil daftar seluruh katalog produk yang aktif dari Backend API.
    """
    url = f"{BACKEND_API_URL}/api/v1/items?is_active=true"
    logger.info(f"Mengambil produk/jasa dari backend: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            logger.error(f"Gagal mengambil produk. Status: {response.status_code}, Body: {response.text}")
            return []
        except Exception as e:
            logger.error(f"Error saat menghubungi backend API fetch_products: {str(e)}")
            return []

async def fetch_product_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Mencari produk berdasarkan kecocokan nama (case-insensitive) di katalog backend.
    """
    products = await fetch_products()
    if not products:
        return None
        
    search_name = name.lower().strip()
    for product in products:
        prod_name = product.get("name", "").lower()
        if search_name in prod_name:
            return product
    return None

async def create_order_api(
    product_id: str,
    qty: int,
    price: float,
    buyer_name: str,
    buyer_phone: str,
    buyer_address: str
) -> Optional[Dict[str, Any]]:
    """
    Membuat pesanan baru di Backend API secara asinkron.
    """
    url = f"{BACKEND_API_URL}/api/v1/orders"
    logger.info(f"Membuat order baru di backend untuk Product ID: {product_id}, Qty: {qty}, Price: {price}")
    
    payload = {
        "customerId": None,
        "items": [
            {
                "productId": product_id,
                "qty": qty,
                "price": price
            }
        ],
        "discount": 0.0,
        "paymentMethod": "qris",
        "notes": f"Pemesanan via Telegram Bot. Nama: {buyer_name}, Telp: {buyer_phone}, Alamat: {buyer_address}"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=15.0
            )
            if response.status_code in [200, 201]:
                return response.json()
            logger.error(f"Gagal membuat order. Status: {response.status_code}, Body: {response.text}")
            return None
        except Exception as e:
            logger.error(f"Error saat menghubungi backend API create_order: {str(e)}")
            return None

async def fetch_order_by_id(order_id: str) -> Optional[Dict[str, Any]]:
    """
    Mengambil data pesanan spesifik berdasarkan ID pesanan dari Backend API.
    """
    url = f"{BACKEND_API_URL}/api/v1/orders/{order_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error fetch order: {str(e)}")
            return None

async def update_order_status_api(order_id: str, new_status: str, payment_status: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """
    Memperbarui status transaksi pesanan (pending/confirmed/processing/done/cancelled) di Backend API.
    """
    url = f"{BACKEND_API_URL}/api/v1/orders/{order_id}/status"
    logger.info(f"Mengupdate status order {order_id} menjadi '{new_status}'")
    
    payload = {
        "status": new_status
    }
    if payment_status:
        payload["paymentStatus"] = payment_status
        
    async with httpx.AsyncClient() as client:
        try:
            response = await client.patch(
                url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10.0
            )
            if response.status_code == 200:
                return response.json()
            logger.error(f"Gagal update status order. Status: {response.status_code}, Body: {response.text}")
            return None
        except Exception as e:
            logger.error(f"Error saat mengupdate status order: {str(e)}")
            return None

async def validate_payment_proof_api(
    order_id: str,
    file_bytes: bytes,
    filename: str
) -> Optional[Dict[str, Any]]:
    """
    Mengirimkan unggahan file bukti transfer ke Backend API untuk divalidasi OCR secara asinkron.
    """
    # Endpoint backend yang tepat untuk payment proof per order
    url = f"{BACKEND_API_URL}/api/v1/orders/{order_id}/payment-proof"
    logger.info(f"Mengirimkan bukti transfer untuk divalidasi ke backend. Order ID: {order_id}")
    
    files = {
        "file": (filename, file_bytes, "image/jpeg")
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                url,
                files=files,
                timeout=30.0
            )
            if response.status_code in [200, 201]:
                return response.json()
            logger.error(f"Gagal validasi bukti transfer. Status: {response.status_code}, Body: {response.text}")
            return None
        except Exception as e:
            logger.error(f"Error saat menghubungi backend API validate_payment_proof: {str(e)}")
            return None

async def fetch_finance_summary() -> Optional[Dict[str, Any]]:
    """
    Mengambil data rangkuman laporan keuangan bulanan.
    """
    url = f"{BACKEND_API_URL}/api/v1/finance/summary"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error fetch finance summary: {str(e)}")
            return None

async def fetch_dashboard_summary() -> Optional[Dict[str, Any]]:
    """
    Mengambil data ringkasan dasbor harian.
    """
    url = f"{BACKEND_API_URL}/api/v1/dashboard/summary"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, timeout=10.0)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            logger.error(f"Error fetch dashboard summary: {str(e)}")
            return None
