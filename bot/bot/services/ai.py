import os
import httpx
from typing import Dict, Any, Optional

BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://localhost:8000")

async def request_ai_estimation(image_url: str, category: str) -> Optional[Dict[str, Any]]:
    """
    Mengirimkan request ke Backend API untuk mendapatkan analisis AI
    terhadap foto barang thrift yang diunggah.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_API_URL}/api/v1/ai/estimate",
                params={"image_url": image_url, "category": category},
                timeout=30.0
            )
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error calling backend AI service: {e}")
            return None

async def register_new_product(product_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Mengirim data produk baru hasil konfirmasi ke Backend API untuk disimpan di database.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{BACKEND_API_URL}/api/v1/products",
                json=product_data,
                headers={"Content-Type": "application/json"},
                timeout=10.0
            )
            if response.status_code == 201:
                return response.json()
            return None
        except Exception as e:
            print(f"Error creating product via backend: {e}")
            return None
