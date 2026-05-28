from pydantic import Field
from typing import Optional, List
from datetime import date as dt_date, datetime
from app.schemas.base import BaseModelConfig

class ExpenseBase(BaseModelConfig):
    category: str = Field(..., examples=["stok", "listrik", "gaji", "sewa", "lainnya"])
    description: Optional[str] = Field(None, examples=["Membeli beras 2 karung"])
    amount: float = Field(..., gt=0, examples=[500000.0])
    date: dt_date = Field(..., examples=["2026-05-28"])
    receipt_url: Optional[str] = Field(None, examples=["https://example.com/receipt.jpg"])

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseResponse(ExpenseBase):
    id: str
    user_id: str
    created_at: datetime

class FinanceSummaryResponse(BaseModelConfig):
    total_income: float
    total_expense: float
    net_profit: float

class CashflowDatapoint(BaseModelConfig):
    date: str # YYYY-MM-DD
    income: float
    expense: float

class CashflowResponse(BaseModelConfig):
    datapoints: List[CashflowDatapoint]
