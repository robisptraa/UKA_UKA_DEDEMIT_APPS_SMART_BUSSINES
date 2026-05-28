import uuid
from sqlalchemy import Column, String, Float, DateTime, ForeignKey, func, JSON
from sqlalchemy.orm import relationship
from app.database import Base

class OrderModel(Base):
    __tablename__ = "orders"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    customer_id = Column(String, ForeignKey("customers.id", ondelete="SET NULL"), nullable=True)
    
    # items menyimpan array objek JSON: [{"product_id": "...", "qty": 1, "price": 15000}]
    items = Column(JSON, nullable=False, default=list)
    
    subtotal = Column(Float, nullable=False, default=0.0)
    discount = Column(Float, nullable=False, default=0.0)
    total = Column(Float, nullable=False, default=0.0)
    
    # enum: pending/confirmed/processing/done/cancelled
    status = Column(String, nullable=False, default="pending")
    payment_method = Column(String, nullable=True) # e.g. qris, transfer, cash
    # enum: unpaid/paid/refunded
    payment_status = Column(String, nullable=False, default="unpaid")
    payment_token = Column(String, nullable=True)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi
    user = relationship("UserModel", back_populates="orders")
    customer = relationship("CustomerModel", back_populates="orders")
    payment_proofs = relationship("PaymentProofModel", back_populates="order", cascade="all, delete-orphan")
