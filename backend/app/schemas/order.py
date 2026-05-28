from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseModelConfig

class OrderItem(BaseModelConfig):
    product_id: str = Field(..., description="ID produk atau jasa yang dibeli")
    qty: int = Field(..., ge=1, description="Jumlah kuantitas", examples=[2])
    price: float = Field(..., gt=0, description="Harga satuan saat dibeli", examples=[15000.0])

class OrderCreate(BaseModelConfig):
    customer_id: Optional[str] = Field(None, description="ID pelanggan jika terdaftar di CRM")
    items: List[OrderItem] = Field(..., min_length=1, description="Daftar item belanjaan")
    discount: Optional[float] = Field(0.0, ge=0.0, description="Potongan harga/diskon")
    payment_method: Optional[str] = Field("cash", description="Metode pembayaran (cash/qris/transfer)")
    notes: Optional[str] = Field(None, description="Catatan tambahan pesanan")

class OrderStatusUpdate(BaseModelConfig):
    status: Optional[str] = Field(None, description="pending/confirmed/processing/done/cancelled")
    payment_status: Optional[str] = Field(None, description="unpaid/paid/refunded")

class PaymentProofResponse(BaseModelConfig):
    id: str
    image_url: str
    extracted_amount: Optional[float] = None
    extracted_sender: Optional[str] = None
    extracted_bank: Optional[str] = None
    is_valid: bool
    validated_at: Optional[datetime] = None
    validated_by: Optional[str] = None

class OrderResponse(BaseModelConfig):
    id: str
    user_id: str
    customer_id: Optional[str] = None
    items: List[OrderItem]
    subtotal: float
    discount: float
    total: float
    status: str
    payment_method: Optional[str] = None
    payment_status: str
    payment_token: Optional[str] = None
    notes: Optional[str] = None
    created_at: datetime
    payment_proofs: List[PaymentProofResponse] = []
