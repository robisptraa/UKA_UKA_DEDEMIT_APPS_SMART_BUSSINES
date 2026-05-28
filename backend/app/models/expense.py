import uuid
from sqlalchemy import Column, String, Float, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class ExpenseModel(Base):
    __tablename__ = "expenses"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    category = Column(String, nullable=False, index=True) # e.g. stok, listrik, gaji, sewa, dll
    description = Column(String, nullable=True)
    amount = Column(Float, nullable=False)
    date = Column(Date, nullable=False, index=True)
    receipt_url = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi balik ke UserModel (Many-to-One)
    user = relationship("UserModel", back_populates="expenses")
