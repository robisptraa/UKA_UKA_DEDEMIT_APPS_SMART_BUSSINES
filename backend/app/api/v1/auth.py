from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Optional

from app.database import get_async_db
from app.models.user import UserModel
from app.schemas.auth import UserRegister, UserResponse, TokenResponse, UserLogin, UserUpdate
from app.security import hash_password, verify_password, create_access_token, get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user_in: UserRegister, db: AsyncSession = Depends(get_async_db)):
    """
    Mendaftarkan pengguna (owner bisnis UMKM) baru secara asinkron.
    Menyertakan field seperti tipe bisnis (business_type) dan kota (city).
    """
    # 1. Periksa apakah email sudah terdaftar
    result = await db.execute(select(UserModel).where(UserModel.email == user_in.email))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email sudah terdaftar. Silakan gunakan email lain."
        )

    # 2. Hashing password
    hashed_pwd = hash_password(user_in.password)

    # 3. Buat user baru
    db_user = UserModel(
        name=user_in.name,
        email=user_in.email,
        phone=user_in.phone,
        store_name=user_in.store_name,
        hashed_password=hashed_pwd,
        business_type=user_in.business_type,
        city=user_in.city,
        logo_url=user_in.logo_url,
        is_active=True
    )

    # 4. Simpan ke database
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user

@router.post("/login", response_model=TokenResponse)
async def login_user(user_in: UserLogin, db: AsyncSession = Depends(get_async_db)):
    """
    Mengautentikasi pengguna dan mengembalikan JWT access token.
    """
    # 1. Cari user berdasarkan email
    result = await db.execute(select(UserModel).where(UserModel.email == user_in.email))
    user = result.scalars().first()

    # 2. Validasi kredensial
    if not user or not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email atau password salah."
        )

    # 3. Generate token
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: UserModel = Depends(get_current_user)):
    """
    Mendapatkan profil pengguna aktif yang sedang login saat ini.
    """
    return current_user

@router.put("/profile", response_model=UserResponse)
async def update_profile(
    profile_data: UserUpdate,
    current_user: UserModel = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_db)
):
    """
    Memperbarui profil pengguna aktif secara asinkron.
    """
    if profile_data.name is not None:
        current_user.name = profile_data.name
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    if profile_data.store_name is not None:
        current_user.store_name = profile_data.store_name
    if profile_data.business_type is not None:
        current_user.business_type = profile_data.business_type
    if profile_data.city is not None:
        current_user.city = profile_data.city
    if profile_data.logo_url is not None:
        current_user.logo_url = profile_data.logo_url
    if profile_data.password is not None:
        current_user.hashed_password = hash_password(profile_data.password)

    db.add(current_user)
    await db.commit()
    await db.refresh(current_user)
    return current_user
