from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from typing import List
from datetime import datetime, timedelta

from app.database import get_async_db
from app.models.product_service import ProductServiceModel
from app.models.order import OrderModel
from app.models.customer import CustomerModel
from app.schemas.dashboard import BestSellerItem, CustomerRetentionResponse, HourlyTrafficResponse, HourlyTrafficDatapoint
from app.security import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/best-sellers", response_model=List[BestSellerItem])
async def get_best_sellers(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil peringkat produk/jasa (items) terlaris berdasarkan kuantitas penjualan lunas secara asinkron.
    """
    # 1. Ambil semua order terbayar (paid) milik owner
    orders_query = select(OrderModel).where(
        and_(
            OrderModel.user_id == current_user.id,
            OrderModel.payment_status == "paid"
        )
    )
    orders_res = await db.execute(orders_query)
    orders = orders_res.scalars().all()
    
    # 2. Agregasikan kuantitas dan omset di Python (dialect-agnostic & robust)
    sales_aggregation = {}
    for o in orders:
        for item in o.items:
            p_id = item.get("product_id")
            qty = item.get("qty", 0)
            price = item.get("price", 0.0)
            
            if p_id:
                if p_id not in sales_aggregation:
                    sales_aggregation[p_id] = {"qty": 0, "revenue": 0.0}
                sales_aggregation[p_id]["qty"] += qty
                sales_aggregation[p_id]["revenue"] += qty * price

    # 3. Ambil metadata item untuk item yang laku terjual
    response_items = []
    if sales_aggregation:
        items_query = select(ProductServiceModel).where(
            and_(
                ProductServiceModel.user_id == current_user.id,
                ProductServiceModel.id.in_(sales_aggregation.keys())
            )
        )
        items_res = await db.execute(items_query)
        items = items_res.scalars().all()
        
        for item in items:
            agg = sales_aggregation[item.id]
            response_items.append(
                BestSellerItem(
                    item_id=item.id,
                    name=item.name,
                    type=item.type,
                    category=item.category,
                    total_qty_sold=agg["qty"],
                    total_revenue=agg["revenue"]
                )
            )
            
    # Urutkan berdasarkan total kuantitas terjual
    response_items.sort(key=lambda x: x.total_qty_sold, reverse=True)
    return response_items[:10] # Top 10

@router.get("/customer-retention", response_model=CustomerRetentionResponse)
async def get_customer_retention(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil analisis tingkat retensi pelanggan CRM secara asinkron:
    - Jumlah pelanggan baru (transaksi 1 kali)
    - Jumlah repeat customer (transaksi >= 2 kali)
    - Persentase rasio retensi pelanggan.
    """
    # 1. Dapatkan semua pelanggan terdaftar milik owner
    customers_query = select(CustomerModel).where(CustomerModel.user_id == current_user.id)
    customers_res = await db.execute(customers_query)
    customers = customers_res.scalars().all()
    
    total_customers_count = len(customers)
    if total_customers_count == 0:
        return {
            "new_customers": 0,
            "repeat_customers": 0,
            "retention_rate": 0.0
        }
        
    # 2. Hitung jumlah order lunas per customer
    orders_query = select(
        OrderModel.customer_id,
        func.count(OrderModel.id)
    ).where(
        and_(
            OrderModel.user_id == current_user.id,
            OrderModel.customer_id.isnot(None),
            OrderModel.payment_status == "paid"
        )
    ).group_by(OrderModel.customer_id)
    
    orders_res = await db.execute(orders_query)
    
    repeat_count = 0
    for row in orders_res.all():
        order_count = row[1]
        if order_count >= 2:
            repeat_count += 1
            
    new_count = total_customers_count - repeat_count
    retention_rate = (repeat_count / total_customers_count) * 100
    
    return {
        "new_customers": new_count,
        "repeat_customers": repeat_count,
        "retention_rate": retention_rate
    }

@router.get("/hourly-traffic", response_model=HourlyTrafficResponse)
async def get_hourly_traffic(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil data tren kepadatan transaksi per jam (00:00 - 23:00) 
    secara asinkron berdasarkan historis pesanan lunas dalam 30 hari terakhir.
    """
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    
    # Inisialisasi peta jam 0-23
    hourly_data = {h: {"count": 0, "revenue": 0.0} for h in range(24)}
    
    # Ambil order dalam 30 hari terakhir
    query = select(OrderModel).where(
        and_(
            OrderModel.user_id == current_user.id,
            OrderModel.payment_status == "paid",
            OrderModel.created_at >= thirty_days_ago
        )
    )
    result = await db.execute(query)
    orders = result.scalars().all()
    
    # Kelompokkan berdasarkan jam pembuatan (local hour / UTC hour)
    for o in orders:
        hour = o.created_at.hour
        if hour in hourly_data:
            hourly_data[hour]["count"] += 1
            hourly_data[hour]["revenue"] += o.total
            
    datapoints = [
        HourlyTrafficDatapoint(
            hour=h,
            order_count=v["count"],
            revenue=v["revenue"]
        ) for h, v in sorted(hourly_data.items())
    ]
    
    return {"traffic": datapoints}
