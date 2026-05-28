import secrets
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import and_, or_
from typing import List, Optional

from app.database import get_async_db
from app.models.order import OrderModel
from app.models.product_service import ProductServiceModel
from app.models.stock_movement import StockMovementModel
from app.models.notification import NotificationModel
from app.models.payment_proof import PaymentProofModel
from app.schemas.order import OrderCreate, OrderStatusUpdate, OrderResponse, PaymentProofResponse
from app.security import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.get("", response_model=List[OrderResponse])
async def list_orders(
    status: Optional[str] = None,
    customer_id: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil semua pesanan masuk milik owner toko aktif secara asinkron.
    Mendukung penyaringan berdasarkan status pesanan, ID pelanggan, rentang tanggal, serta pagination.
    """
    query = select(OrderModel).where(OrderModel.user_id == current_user.id)
    
    if status:
        query = query.where(OrderModel.status == status)
    if customer_id:
        query = query.where(OrderModel.customer_id == customer_id)
    if start_date:
        query = query.where(OrderModel.created_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        query = query.where(OrderModel.created_at <= datetime.combine(end_date, datetime.max.time()))
        
    query = query.order_by(OrderModel.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    orders = result.scalars().all()
    return orders

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Membuat pesanan baru untuk owner secara asinkron.
    Validasi stok dilakukan untuk tipe 'product', mencatat riwayat pergerakan stok (stock movement), 
    serta memicu notifikasi jika stok berada di tingkat kritis (< 3).
    """
    subtotal = 0.0
    items_list = []
    
    # 1. Validasi seluruh item pesanan
    for item in order_in.items:
        # Cari produk/jasa di DB
        p_res = await db.execute(
            select(ProductServiceModel)
            .where(ProductServiceModel.id == item.product_id, ProductServiceModel.user_id == current_user.id)
        )
        product = p_res.scalars().first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Produk/Jasa dengan ID {item.product_id} tidak ditemukan."
            )
            
        if not product.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Item {product.name} sedang tidak aktif dan tidak dapat dibeli."
            )
            
        # Jika barang fisik, cek stok
        if product.type == "product":
            if product.stock is None or product.stock < item.qty:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Stok untuk produk {product.name} tidak mencukupi (Tersedia: {product.stock}, Diminta: {item.qty})."
                )
            
            # Kurangi stok produk
            product.stock -= item.qty
            
            # Catat pergerakan stok (Stock Movement)
            movement = StockMovementModel(
                product_id=product.id,
                type="out",
                qty=item.qty,
                note=f"Penjualan via Order"
            )
            db.add(movement)
            
            # Buat notifikasi jika stok kritis (< 3)
            if product.stock < 3:
                notif = NotificationModel(
                    user_id=current_user.id,
                    type="stock",
                    title="Peringatan Stok Kritis!",
                    message=f"Stok produk '{product.name}' tersisa {product.stock} {product.unit}. Harap lakukan restock segera."
                )
                db.add(notif)
                
        subtotal += product.price * item.qty
        items_list.append({
            "product_id": item.product_id,
            "qty": item.qty,
            "price": product.price
        })

    # 2. Hitung total
    total = max(0.0, subtotal - order_in.discount)
    simulated_payment_token = f"snap-token-{secrets.token_hex(8)}"
    
    # 3. Simpan order ke database
    db_order = OrderModel(
        user_id=current_user.id,
        customer_id=order_in.customer_id,
        items=items_list,
        subtotal=subtotal,
        discount=order_in.discount,
        total=total,
        status="pending",
        payment_method=order_in.payment_method,
        payment_status="unpaid",
        payment_token=simulated_payment_token,
        notes=order_in.notes
    )
    
    db.add(db_order)
    
    # Pemicu notifikasi order baru
    notif_order = NotificationModel(
        user_id=current_user.id,
        type="order",
        title="Pesanan Baru Masuk",
        message=f"Order baru senilai Rp {total:,.0f} diterima. Menunggu pembayaran."
    )
    db.add(notif_order)
    
    await db.commit()
    await db.refresh(db_order)
    return db_order

@router.get("/{id}", response_model=OrderResponse)
async def get_order_detail(
    id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil rincian detail pesanan secara asinkron berdasarkan ID.
    """
    result = await db.execute(
        select(OrderModel)
        .where(OrderModel.id == id, OrderModel.user_id == current_user.id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pesanan tidak ditemukan atau Anda tidak memiliki hak akses."
        )
    return order

@router.patch("/{id}/status", response_model=OrderResponse)
async def update_order_status(
    id: str,
    status_in: OrderStatusUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Memperbarui status pengerjaan pesanan dan status pembayaran secara asinkron.
    """
    result = await db.execute(
        select(OrderModel)
        .where(OrderModel.id == id, OrderModel.user_id == current_user.id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pesanan tidak ditemukan atau Anda tidak memiliki akses keamanan."
        )

    if status_in.status is not None:
        order.status = status_in.status
    if status_in.payment_status is not None:
        order.payment_status = status_in.payment_status

    await db.commit()
    await db.refresh(order)
    return order

@router.post("/{id}/payment-proof", response_model=PaymentProofResponse)
async def upload_payment_proof(
    id: str,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengunggah berkas foto bukti transfer pembayaran pesanan secara asinkron.
    Simulasi ekstraksi data pembayaran digital OCR AI otomatis dijalankan.
    """
    # 1. Pastikan order tersedia
    result = await db.execute(
        select(OrderModel)
        .where(OrderModel.id == id, OrderModel.user_id == current_user.id)
    )
    order = result.scalars().first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pesanan tidak ditemukan atau Anda tidak berwenang mengelola bukti pembayaran untuk transaksi ini."
        )

    # Simulasikan path penyimpanan
    simulated_url = f"https://supabase.storage/dedemit-umkm/proofs/{secrets.token_hex(4)}_{file.filename}"
    
    # 2. Simulasikan OCR AI ekstraksi informasi dari struk transfer bank
    extracted_amount = order.total
    extracted_sender = "ANTON WIJAYA"
    extracted_bank = "BCA"
    
    proof = PaymentProofModel(
        order_id=order.id,
        image_url=simulated_url,
        extracted_amount=extracted_amount,
        extracted_sender=extracted_sender,
        extracted_bank=extracted_bank,
        is_valid=True, # Validasi otomatis karena jumlahnya sama
        validated_at=datetime.utcnow(),
        validated_by="ai"
    )
    
    # 3. Update status pembayaran order jika valid
    order.payment_status = "paid"
    order.status = "confirmed"
    
    db.add(proof)
    db.add(order)
    
    # Notifikasi pembayaran berhasil
    notif = NotificationModel(
        user_id=current_user.id,
        type="order",
        title="Pembayaran Terverifikasi (AI)",
        message=f"Bukti transfer pesanan #{order.id[:8]} berhasil diverifikasi oleh AI senilai Rp {extracted_amount:,.0f}."
    )
    db.add(notif)
    
    await db.commit()
    await db.refresh(proof)
    return proof
