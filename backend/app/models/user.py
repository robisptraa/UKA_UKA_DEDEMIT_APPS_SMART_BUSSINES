import uuid
from sqlalchemy import Column, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base

class UserModel(Base):
    __tablename__ = "users"

    # ID primer menggunakan UUID string secara unik
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    phone = Column(String, nullable=False)
    store_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    business_type = Column(String, nullable=False, default="lainnya") # enum: warung/salon/bengkel/laundry/kafe/toko/jasa/lainnya
    city = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi satu pengguna ke banyak produk/jasa (One-to-Many)
    items = relationship("ProductServiceModel", back_populates="user", cascade="all, delete-orphan")
    
    # Relasi satu pengguna ke banyak pelanggan (One-to-Many)
    customers = relationship("CustomerModel", back_populates="user", cascade="all, delete-orphan")

    # Relasi satu pengguna ke banyak pesanan (One-to-Many)
    orders = relationship("OrderModel", back_populates="user", cascade="all, delete-orphan")

    # Relasi satu pengguna ke banyak pengeluaran (One-to-Many)
    expenses = relationship("ExpenseModel", back_populates="user", cascade="all, delete-orphan")

    # Relasi satu pengguna ke banyak notifikasi (One-to-Many)
    notifications = relationship("NotificationModel", back_populates="user", cascade="all, delete-orphan")
