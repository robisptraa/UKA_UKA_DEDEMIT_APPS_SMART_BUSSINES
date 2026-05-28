from pydantic import Field, EmailStr
from typing import Optional, List
from datetime import datetime
from app.schemas.base import BaseModelConfig

class CustomerBase(BaseModelConfig):
    name: str = Field(..., min_length=2, max_length=50, examples=["Rian Wijaya"])
    phone: Optional[str] = Field(None, examples=["08123456789"])
    email: Optional[EmailStr] = Field(None, examples=["rian@example.com"])
    address: Optional[str] = Field(None, examples=["Jl. Merdeka No. 10, Bandung"])
    notes: Optional[str] = Field(None, examples=["Pelanggan setia warkop, suka kopi manis"])

class CustomerCreate(CustomerBase):
    pass

class CustomerUpdate(BaseModelConfig):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    notes: Optional[str] = None

class CustomerResponse(CustomerBase):
    id: str
    user_id: str
    created_at: datetime

# Schema ringkas untuk order history
class CustomerOrderHistory(BaseModelConfig):
    id: str
    total: float
    status: str
    payment_status: str
    created_at: datetime

class CustomerDetailResponse(CustomerResponse):
    orders: List[CustomerOrderHistory] = []
