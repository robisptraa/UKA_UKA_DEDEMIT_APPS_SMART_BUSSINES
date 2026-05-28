import uuid
from sqlalchemy import Column, String, Float, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class PaymentProofModel(Base):
    __tablename__ = "payment_proofs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = Column(String, ForeignKey("orders.id", ondelete="CASCADE"), nullable=False)
    
    image_url = Column(String, nullable=False)
    extracted_amount = Column(Float, nullable=True)
    extracted_sender = Column(String, nullable=True)
    extracted_bank = Column(String, nullable=True)
    is_valid = Column(Boolean, nullable=False, default=False)
    validated_at = Column(DateTime(timezone=True), nullable=True)
    validated_by = Column(String, nullable=True) # e.g. ai, manual

    # Relasi balik ke OrderModel (Many-to-One)
    order = relationship("OrderModel", back_populates="payment_proofs")
