from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_
from typing import List, Optional

from app.database import get_async_db
from app.models.customer import CustomerModel
from app.models.order import OrderModel
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerResponse, CustomerDetailResponse, CustomerOrderHistory
from app.security import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/customers", tags=["CRM (Customers)"])

@router.get("", response_model=List[CustomerResponse])
async def list_customers(
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil daftar pelanggan CRM milik owner toko aktif secara asinkron.
    Mendukung pencarian nama atau nomor telepon pelanggan serta pagination.
    """
    query = select(CustomerModel).where(CustomerModel.user_id == current_user.id)
    
    if search:
        query = query.where(
            or_(
                CustomerModel.name.ilike(f"%{search}%"),
                CustomerModel.phone.ilike(f"%{search}%")
            )
        )
        
    query = query.order_by(CustomerModel.name.asc()).offset(offset).limit(limit)
    result = await db.execute(query)
    customers = result.scalars().all()
    return customers

@router.post("", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED)
async def create_customer(
    customer_in: CustomerCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mendaftarkan pelanggan baru ke dalam database CRM owner secara asinkron.
    """
    db_customer = CustomerModel(
        user_id=current_user.id,
        name=customer_in.name,
        phone=customer_in.phone,
        email=customer_in.email,
        address=customer_in.address,
        notes=customer_in.notes
    )
    db.add(db_customer)
    await db.commit()
    await db.refresh(db_customer)
    return db_customer

@router.get("/{customer_id}", response_model=CustomerDetailResponse)
async def get_customer_detail(
    customer_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil detail data pelanggan CRM tertentu beserta riwayat pesanan (order history) mereka secara asinkron.
    """
    # 1. Cari data customer
    c_result = await db.execute(
        select(CustomerModel)
        .where(CustomerModel.id == customer_id, CustomerModel.user_id == current_user.id)
    )
    customer = c_result.scalars().first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pelanggan tidak ditemukan atau Anda tidak memiliki izin keamanan."
        )

    # 2. Ambil riwayat order
    o_result = await db.execute(
        select(OrderModel)
        .where(OrderModel.customer_id == customer_id, OrderModel.user_id == current_user.id)
        .order_by(OrderModel.created_at.desc())
    )
    orders = o_result.scalars().all()

    # 3. Bentuk history order response
    order_history = [
        CustomerOrderHistory(
            id=o.id,
            total=o.total,
            status=o.status,
            payment_status=o.payment_status,
            created_at=o.created_at
        ) for o in orders
    ]

    return CustomerDetailResponse(
        id=customer.id,
        user_id=customer.user_id,
        name=customer.name,
        phone=customer.phone,
        email=customer.email,
        address=customer.address,
        notes=customer.notes,
        created_at=customer.created_at,
        orders=order_history
    )

@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_in: CustomerUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Memperbarui data profil pelanggan CRM tertentu secara asinkron.
    """
    result = await db.execute(
        select(CustomerModel)
        .where(CustomerModel.id == customer_id, CustomerModel.user_id == current_user.id)
    )
    customer = result.scalars().first()
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pelanggan tidak ditemukan atau Anda tidak memiliki akses pengeditan."
        )

    update_data = customer_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(customer, key, value)

    await db.commit()
    await db.refresh(customer)
    return customer
