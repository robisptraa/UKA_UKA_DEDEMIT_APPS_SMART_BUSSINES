from pydantic import Field
from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseModelConfig

class ItemBase(BaseModelConfig):
    name: str = Field(..., min_length=2, max_length=100, examples=["Nasi Goreng Rendang"])
    category: str = Field(..., examples=["Kuliner"])
    type: str = Field("product", examples=["product"]) # product / service
    description: Optional[str] = Field(None, examples=["Nasi goreng dengan bumbu rendang khas Padang"])
    price: float = Field(..., gt=0, examples=[25000.0])
    stock: Optional[int] = Field(None, ge=0, examples=[50]) # Null untuk jasa/service
    unit: Optional[str] = Field("pcs", examples=["pcs"]) # pcs, kg, liter, jam, paket, dll
    image_url: Optional[str] = Field(None, examples=["https://example.com/item.jpg"])
    is_active: bool = Field(True, examples=[True])

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModelConfig):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    category: Optional[str] = None
    type: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None

class ItemResponse(ItemBase):
    id: str
    user_id: str
    created_at: datetime

class BulkImportResponse(BaseModelConfig):
    success: bool
    imported_count: int
    errors: List[str] = []
