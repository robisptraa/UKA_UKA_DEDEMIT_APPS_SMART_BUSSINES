import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import or_, and_, func
from typing import List, Optional

from app.database import get_async_db
from app.models.product_service import ProductServiceModel
from app.schemas.item import ItemCreate, ItemUpdate, ItemResponse, BulkImportResponse
from app.security import get_current_user
from app.models.user import UserModel

router = APIRouter(prefix="/items", tags=["Products & Services"])

@router.get("", response_model=List[ItemResponse])
async def list_items(
    category: Optional[str] = None,
    type: Optional[str] = None,
    is_active: Optional[bool] = None,
    search: Optional[str] = None,
    limit: int = 50,
    offset: int = 0,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil daftar produk dan jasa (items) milik owner toko aktif secara asinkron.
    Mendukung penyaringan berdasarkan kategori, tipe (product/service), keaktifan, pencarian kata kunci, serta pagination.
    """
    query = select(ProductServiceModel).where(ProductServiceModel.user_id == current_user.id)
    
    if category:
        query = query.where(ProductServiceModel.category == category)
    if type:
        query = query.where(ProductServiceModel.type == type)
    if is_active is not None:
        query = query.where(ProductServiceModel.is_active == is_active)
    if search:
        query = query.where(
            or_(
                ProductServiceModel.name.ilike(f"%{search}%"),
                ProductServiceModel.description.ilike(f"%{search}%")
            )
        )
    
    query = query.order_by(ProductServiceModel.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(query)
    items = result.scalars().all()
    return items

@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
async def create_item(
    item_in: ItemCreate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Menambahkan produk fisik atau jasa baru ke dalam database secara asinkron.
    Jika tipe item adalah 'service' (jasa), stok otomatis diatur menjadi null.
    """
    stock_value = None if item_in.type == "service" else item_in.stock
    
    db_item = ProductServiceModel(
        user_id=current_user.id,
        name=item_in.name,
        category=item_in.category,
        type=item_in.type,
        description=item_in.description,
        price=item_in.price,
        stock=stock_value,
        unit=item_in.unit,
        image_url=item_in.image_url,
        is_active=item_in.is_active
    )
    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item

@router.get("/{item_id}", response_model=ItemResponse)
async def get_item_detail(
    item_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengambil informasi detail produk/jasa tertentu secara asinkron berdasarkan ID.
    Hanya mengizinkan akses jika item merupakan milik pengguna aktif.
    """
    result = await db.execute(
        select(ProductServiceModel)
        .where(ProductServiceModel.id == item_id, ProductServiceModel.user_id == current_user.id)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item tidak ditemukan atau Anda tidak memiliki otorisasi keamanan."
        )
    return item

@router.put("/{item_id}", response_model=ItemResponse)
async def update_item(
    item_id: str,
    item_in: ItemUpdate,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Memperbarui spesifikasi produk/jasa secara asinkron.
    Hanya diperbolehkan jika item tersebut milik owner toko aktif.
    """
    result = await db.execute(
        select(ProductServiceModel)
        .where(ProductServiceModel.id == item_id, ProductServiceModel.user_id == current_user.id)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item tidak ditemukan atau Anda tidak memiliki akses pengeditan."
        )

    update_data = item_in.model_dump(exclude_unset=True)
    
    # Jika mengubah tipe ke service, pastikan stock di-null-kan
    if "type" in update_data and update_data["type"] == "service":
        item.stock = None
        if "stock" in update_data:
            del update_data["stock"]

    for key, value in update_data.items():
        setattr(item, key, value)

    await db.commit()
    await db.refresh(item)
    return item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(
    item_id: str,
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Menghapus item (produk/jasa) dari database secara asinkron.
    Hanya diizinkan jika item merupakan kepemilikan owner yang aktif.
    """
    result = await db.execute(
        select(ProductServiceModel)
        .where(ProductServiceModel.id == item_id, ProductServiceModel.user_id == current_user.id)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item tidak ditemukan atau Anda tidak memiliki otorisasi penghapusan."
        )

    await db.delete(item)
    await db.commit()
    return None

@router.post("/bulk-import", response_model=BulkImportResponse)
async def bulk_import_items(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_async_db),
    current_user: UserModel = Depends(get_current_user)
):
    """
    Mengimpor daftar produk/jasa dari berkas CSV yang diunggah secara asinkron.
    Format kolom CSV yang didukung: name, category, type, description, price, stock, unit, image_url
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ekstensi berkas tidak didukung. Harap unggah file berformat CSV."
        )

    contents = await file.read()
    string_data = contents.decode("utf-8")
    csv_file = StringIO(string_data)
    reader = csv.DictReader(csv_file)
    
    imported_count = 0
    errors = []
    
    for index, row in enumerate(reader, start=1):
        try:
            name = row.get("name")
            category = row.get("category", "Lain-lain")
            item_type = row.get("type", "product").strip().lower()
            description = row.get("description", "")
            price_str = row.get("price", "0")
            stock_str = row.get("stock", "0")
            unit = row.get("unit", "pcs")
            image_url = row.get("image_url", None)
            
            if not name:
                errors.append(f"Baris {index}: Kolom 'name' kosong.")
                continue
                
            price = float(price_str)
            stock = None if item_type == "service" else int(stock_str) if stock_str else 0
            
            db_item = ProductServiceModel(
                user_id=current_user.id,
                name=name,
                category=category,
                type=item_type,
                description=description,
                price=price,
                stock=stock,
                unit=unit,
                image_url=image_url,
                is_active=True
            )
            db.add(db_item)
            imported_count += 1
        except Exception as e:
            errors.append(f"Baris {index}: Gagal parsing baris. Detail error: {str(e)}")
            
    if imported_count > 0:
        await db.commit()
        
    return {
        "success": len(errors) == 0,
        "imported_count": imported_count,
        "errors": errors
    }
