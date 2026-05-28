from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func, and_
from typing import List, Optional

from app.database import get_async_db
from app.models.expense import ExpenseModel
from app.models.order import OrderModel
from app.schemas.finance import ExpenseCreate, ExpenseResponse, FinanceSummaryResponse, CashflowResponse, CashflowDatapoint
from app.security import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/finance", tags=["Finance & Bookkeeping"])

@router.get("/expenses", response_model=List[ExpenseResponse])
async def list_expenses(
    category: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil semua catatan pengeluaran operasional bisnis milik owner aktif secara asinkron.
    Mendukung penyaringan kategori pengeluaran, rentang tanggal, serta pagination.
    """
    query = select(ExpenseModel).where(ExpenseModel.user_id == current_user.id)
    
    if category:
        query = query.where(ExpenseModel.category == category)
    if start_date:
        query = query.where(ExpenseModel.date >= start_date)
    if end_date:
        query = query.where(ExpenseModel.date <= end_date)
        
    query = query.order_by(ExpenseModel.date.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    expenses = result.scalars().all()
    return expenses

@router.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED)
async def create_expense(
    expense_in: ExpenseCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mencatat pengeluaran operasional bisnis baru secara asinkron.
    """
    db_expense = ExpenseModel(
        user_id=current_user.id,
        category=expense_in.category,
        description=expense_in.description,
        amount=expense_in.amount,
        date=expense_in.date,
        receipt_url=expense_in.receipt_url
    )
    db.add(db_expense)
    await db.commit()
    await db.refresh(db_expense)
    return db_expense

@router.get("/summary", response_model=FinanceSummaryResponse)
async def get_finance_summary(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil rangkuman total pemasukan (omset dari order lunas), pengeluaran, 
    dan laba bersih operasional pada bulan berjalan secara asinkron.
    """
    today = date.today()
    start_of_month = date(today.year, today.month, 1)
    
    # 1. Total pemasukan bulan ini (Order lunas)
    income_query = select(func.sum(OrderModel.total)).where(
        and_(
            OrderModel.user_id == current_user.id,
            OrderModel.payment_status == "paid",
            OrderModel.created_at >= datetime.combine(start_of_month, datetime.min.time())
        )
    )
    income_res = await db.execute(income_query)
    total_income = income_res.scalar() or 0.0
    
    # 2. Total pengeluaran bulan ini
    expense_query = select(func.sum(ExpenseModel.amount)).where(
        and_(
            ExpenseModel.user_id == current_user.id,
            ExpenseModel.date >= start_of_month
        )
    )
    expense_res = await db.execute(expense_query)
    total_expense = expense_res.scalar() or 0.0
    
    net_profit = total_income - total_expense
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "net_profit": net_profit
    }

@router.get("/cashflow", response_model=CashflowResponse)
async def get_cashflow(
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil data riwayat cashflow harian (pemasukan vs pengeluaran) 
    selama 30 hari terakhir untuk kebutuhan grafik secara asinkron.
    """
    today = date.today()
    start_date = today - timedelta(days=29)
    
    # Inisialisasi peta tanggal
    cashflow_dict = {}
    for i in range(30):
        d = start_date + timedelta(days=i)
        cashflow_dict[d.strftime("%Y-%m-%d")] = {"income": 0.0, "expense": 0.0}
        
    # 1. Tarik data pendapatan harian dari order yang terbayar
    orders_query = select(
        func.date_trunc('day', OrderModel.created_at).label('day'),
        func.sum(OrderModel.total)
    ).where(
        and_(
            OrderModel.user_id == current_user.id,
            OrderModel.payment_status == "paid",
            OrderModel.created_at >= datetime.combine(start_date, datetime.min.time())
        )
    ).group_by('day')
    
    orders_res = await db.execute(orders_query)
    for row in orders_res.all():
        day_str = row[0].strftime("%Y-%m-%d")
        if day_str in cashflow_dict:
            cashflow_dict[day_str]["income"] = float(row[1] or 0.0)
            
    # 2. Tarik data pengeluaran harian
    expenses_query = select(
        ExpenseModel.date,
        func.sum(ExpenseModel.amount)
    ).where(
        and_(
            ExpenseModel.user_id == current_user.id,
            ExpenseModel.date >= start_date
        )
    ).group_by(ExpenseModel.date)
    
    expenses_res = await db.execute(expenses_query)
    for row in expenses_res.all():
        day_str = row[0].strftime("%Y-%m-%d")
        if day_str in cashflow_dict:
            cashflow_dict[day_str]["expense"] = float(row[1] or 0.0)
            
    # 3. Bentuk data list datapoints
    datapoints = [
        CashflowDatapoint(
            date=k,
            income=v["income"],
            expense=v["expense"]
        ) for k, v in sorted(cashflow_dict.items())
    ]
    
    return {"datapoints": datapoints}
