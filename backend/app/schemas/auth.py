from pydantic import Field, EmailStr
from datetime import datetime
from typing import Optional
from app.schemas.base import BaseModelConfig

class UserRegister(BaseModelConfig):
    name: str = Field(..., min_length=2, max_length=50, examples=["Budi Santoso"])
    email: EmailStr = Field(..., examples=["budi@example.com"])
    phone: str = Field(..., min_length=9, max_length=15, examples=["081234567890"])
    store_name: str = Field(..., min_length=3, max_length=50, examples=["Toko Kelontong Berkah"])
    password: str = Field(..., min_length=6, examples=["rahasia123"])
    business_type: str = Field("lainnya", examples=["toko"]) # warung/salon/bengkel/laundry/kafe/toko/jasa/lainnya
    city: Optional[str] = Field(None, examples=["Jakarta"])
    logo_url: Optional[str] = Field(None, examples=["https://example.com/logo.png"])

class UserLogin(BaseModelConfig):
    email: EmailStr = Field(..., examples=["budi@example.com"])
    password: str = Field(..., examples=["rahasia123"])

class TokenResponse(BaseModelConfig):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModelConfig):
    id: str
    name: str
    email: EmailStr
    phone: str
    store_name: str
    business_type: str
    city: Optional[str] = None
    logo_url: Optional[str] = None
    is_active: bool
    created_at: datetime

class UserUpdate(BaseModelConfig):
    name: Optional[str] = None
    phone: Optional[str] = None
    store_name: Optional[str] = None
    business_type: Optional[str] = None
    city: Optional[str] = None
    logo_url: Optional[str] = None
    password: Optional[str] = None
