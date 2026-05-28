import uuid
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base

class StockMovementModel(Base):
    __tablename__ = "stock_movements"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = Column(String, ForeignKey("products_services.id", ondelete="CASCADE"), nullable=False)
    
    type = Column(String, nullable=False) # enum: in/out/adjustment
    qty = Column(Integer, nullable=False)
    note = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relasi balik ke ProductServiceModel (Many-to-One)
    product = relationship("ProductServiceModel", back_populates="stock_movements")
