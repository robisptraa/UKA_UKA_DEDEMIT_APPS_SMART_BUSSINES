from pydantic import Field
from typing import List
from app.schemas.base import BaseModelConfig

class DashboardSummaryResponse(BaseModelConfig):
    total_orders_today: int = Field(..., description="Jumlah pesanan masuk hari ini", examples=[5])
    revenue_today: float = Field(..., description="Pendapatan hari ini", examples=[125000.0])
    low_stock_count: int = Field(..., description="Jumlah item yang stoknya kritis", examples=[3])
    new_customers_today: int = Field(..., description="Jumlah pelanggan baru hari ini", examples=[2])

class BestSellerItem(BaseModelConfig):
    item_id: str
    name: str
    type: str # product / service
    category: str
    total_qty_sold: int
    total_revenue: float

class CustomerRetentionResponse(BaseModelConfig):
    new_customers: int
    repeat_customers: int
    retention_rate: float # Persentase repeat customer dari total customer

class HourlyTrafficDatapoint(BaseModelConfig):
    hour: int # 0 - 23
    order_count: int
    revenue: float

class HourlyTrafficResponse(BaseModelConfig):
    traffic: List[HourlyTrafficDatapoint]
