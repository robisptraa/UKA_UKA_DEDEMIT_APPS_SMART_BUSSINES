from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from datetime import datetime, time, date

from app.database import get_async_db
from app.models.order import OrderModel
from app.models.product_service import ProductServiceModel
from app.models.customer import CustomerModel
from app.schemas.dashboard import DashboardSummaryResponse
from app.security import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=DashboardSummaryResponse)
async def get_dashboard_summary(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil data ringkasan bisnis (dashboard summary) asinkron harian untuk owner UMKM:
    - Jumlah pesanan masuk hari ini.
    - Total pendapatan hari ini dari order yang berstatus lunas (paid).
    - Jumlah produk aktif dengan persediaan kritis (< 3).
    - Jumlah pelanggan baru terdaftar hari ini.
    """
    today_start = datetime.combine(date.today(), time.min)
    
    # 1. Jumlah pesanan hari ini
    orders_today_query = select(func.count(OrderModel.id)).where(
        and_(
            OrderModel.user_id == current_user.id,
            OrderModel.created_at >= today_start
        )
    )
    orders_today_res = await db.execute(orders_today_query)
    total_orders_today = orders_today_res.scalar() or 0

    # 2. Total pendapatan hari ini (lunas)
    revenue_today_query = select(func.sum(OrderModel.total)).where(
        and_(
            OrderModel.user_id == current_user.id,
            OrderModel.payment_status == "paid",
            OrderModel.created_at >= today_start
        )
    )
    revenue_today_res = await db.execute(revenue_today_query)
    revenue_today = float(revenue_today_res.scalar() or 0.0)

    # 3. Jumlah produk hampir habis (< 3)
    low_stock_query = select(func.count(ProductServiceModel.id)).where(
        and_(
            ProductServiceModel.user_id == current_user.id,
            ProductServiceModel.type == "product",
            ProductServiceModel.is_active == True,
            ProductServiceModel.stock < 3
        )
    )
    low_stock_res = await db.execute(low_stock_query)
    low_stock_count = low_stock_res.scalar() or 0

    # 4. Pelanggan baru hari ini
    new_customers_query = select(func.count(CustomerModel.id)).where(
        and_(
            CustomerModel.user_id == current_user.id,
            CustomerModel.created_at >= today_start
        )
    )
    new_customers_res = await db.execute(new_customers_query)
    new_customers_today = new_customers_res.scalar() or 0

    return {
        "total_orders_today": total_orders_today,
        "revenue_today": revenue_today,
        "low_stock_count": low_stock_count,
        "new_customers_today": new_customers_today
    }
