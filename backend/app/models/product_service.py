import uuid
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class ProductServiceModel(Base):
    __tablename__ = "products_services"

    # ID primer menggunakan UUID string secara unik
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    # Relasi ke owner bisnis (users)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name = Column(String, nullable=False, index=True)
    category = Column(String, nullable=False, index=True) # Kategori (makanan, minuman, fashion, salon, laundry, dll)
    type = Column(String, nullable=False, default="product") # enum: product/service
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    stock = Column(Integer, nullable=True) # Null untuk service, integer untuk product
    unit = Column(String, nullable=True, default="pcs") # Satuan (pcs, kg, liter, jam, paket, dll)
    image_url = Column(String, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi balik ke UserModel (Many-to-One)
    user = relationship("UserModel", back_populates="items")

    # Relasi ke riwayat pergerakan stok (One-to-Many)
    stock_movements = relationship("StockMovementModel", back_populates="product", cascade="all, delete-orphan")
