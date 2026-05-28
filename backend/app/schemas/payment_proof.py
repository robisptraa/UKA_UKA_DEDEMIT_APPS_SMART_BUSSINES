from pydantic import Field
from typing import Optional
from datetime import datetime
from app.schemas.base import BaseModelConfig

class PaymentProofResponse(BaseModelConfig):
    id: str
    order_id: str
    image_url: str
    extracted_amount: Optional[float] = Field(None, examples=[850000.0])
    extracted_sender: Optional[str] = Field(None, examples=["AHMAD FAUZI"])
    is_valid: bool = Field(False, examples=[True])
    validated_at: Optional[datetime] = None
