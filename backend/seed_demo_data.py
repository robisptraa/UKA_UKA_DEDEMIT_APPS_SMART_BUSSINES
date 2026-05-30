"""
Dedemit OS — Demo Data Seeder
Mengisi database dengan data demo realistis untuk showcase kompetisi #JuaraVibeCoding.

Berisi:
  - 3 akun owner: Warung, Salon, Bengkel
  - Setiap owner: 10 produk/jasa, 8 pelanggan, 15 order, 5 pengeluaran
  - 30 hari history transaksi untuk grafik analytics yang menarik

Jalankan dengan:
  cd backend
  python seed_demo_data.py
"""

import asyncio
import random
import sys
import os
from datetime import datetime, timedelta, timezone
from typing import List

# Tambahkan root ke path agar bisa import app modules
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
from passlib.context import CryptContext

from app.config import settings
from app.database import Base
from app.models.user import UserModel
from app.models.product_service import ProductServiceModel
from app.models.customer import CustomerModel
from app.models.order import OrderModel
from app.models.expense import ExpenseModel
from app.models.notification import NotificationModel
from app.models.stock_movement import StockMovementModel

# ─────────────────────────────────────────────────────────────────────────────
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(pw: str) -> str:
    return pwd_context.hash(pw)

def random_date(days_back: int) -> datetime:
    """Generate random datetime dalam N hari terakhir."""
    now = datetime.now(timezone.utc)
    delta = random.randint(0, days_back * 24 * 60)  # Menit acak
    return now - timedelta(minutes=delta)

def idr(amount: float) -> str:
    return f"Rp {amount:,.0f}"


# ─────────────────────────────────────────────────────────────────────────────
# DATA DEFINITIONS
# ─────────────────────────────────────────────────────────────────────────────

OWNERS = [
    {
        "name": "Bu Sari Wijayanti",
        "email": "bos@dedemit.id",  # Akun utama demo
        "phone": "081234567890",
        "store_name": "Warung Nasi Bu Sari",
        "business_type": "warung",
        "city": "Surabaya",
        "password": "Password123!",
    },
    {
        "name": "Dewi Ratnasari",
        "email": "dewi.salon@dedemit.id",
        "phone": "082345678901",
        "store_name": "Salon Kecantikan Dewi",
        "business_type": "salon",
        "city": "Bandung",
        "password": "Password123!",
    },
    {
        "name": "Pak Jaya Kusuma",
        "email": "bengkel.jaya@dedemit.id",
        "phone": "083456789012",
        "store_name": "Bengkel Jaya Motor",
        "business_type": "bengkel",
        "city": "Yogyakarta",
        "password": "Password123!",
    },
]

ITEMS_BY_TYPE = {
    "warung": [
        {"name": "Nasi Goreng Spesial", "category": "Makanan", "type": "product", "price": 18000, "stock": 50, "unit": "porsi"},
        {"name": "Ayam Goreng Kremes", "category": "Makanan", "type": "product", "price": 22000, "stock": 30, "unit": "porsi"},
        {"name": "Mie Ayam Bakso", "category": "Makanan", "type": "product", "price": 16000, "stock": 40, "unit": "porsi"},
        {"name": "Es Teh Manis", "category": "Minuman", "type": "product", "price": 5000, "stock": 100, "unit": "gelas"},
        {"name": "Jus Alpukat", "category": "Minuman", "type": "product", "price": 12000, "stock": 20, "unit": "gelas"},
        {"name": "Catering Nasi Box", "category": "Katering", "type": "service", "price": 35000, "unit": "box"},
        {"name": "Pesan Antar Makanan", "category": "Jasa", "type": "service", "price": 10000, "unit": "order"},
        {"name": "Soto Ayam Komplit", "category": "Makanan", "type": "product", "price": 20000, "stock": 25, "unit": "porsi"},
        {"name": "Gado-Gado Betawi", "category": "Makanan", "type": "product", "price": 15000, "stock": 20, "unit": "porsi"},
        {"name": "Kopi Susu Signature", "category": "Minuman", "type": "product", "price": 14000, "stock": 50, "unit": "gelas"},
    ],
    "salon": [
        {"name": "Potong Rambut Wanita", "category": "Rambut", "type": "service", "price": 75000, "unit": "sesi"},
        {"name": "Potong Rambut Pria", "category": "Rambut", "type": "service", "price": 45000, "unit": "sesi"},
        {"name": "Creambath Premium", "category": "Rambut", "type": "service", "price": 120000, "unit": "sesi"},
        {"name": "Facial Glowing", "category": "Wajah", "type": "service", "price": 150000, "unit": "sesi"},
        {"name": "Manicure Pedicure", "category": "Kuku", "type": "service", "price": 85000, "unit": "sesi"},
        {"name": "Smoothing Rambut", "category": "Rambut", "type": "service", "price": 350000, "unit": "sesi"},
        {"name": "Warnai Rambut (per bagian)", "category": "Rambut", "type": "service", "price": 200000, "unit": "sesi"},
        {"name": "Lulur Badan Premium", "category": "Badan", "type": "service", "price": 180000, "unit": "sesi"},
        {"name": "Shampo & Blow", "category": "Rambut", "type": "service", "price": 50000, "unit": "sesi"},
        {"name": "Tata Rias Wisuda", "category": "Makeup", "type": "service", "price": 400000, "unit": "sesi"},
    ],
    "bengkel": [
        {"name": "Ganti Oli Mesin", "category": "Perawatan", "type": "service", "price": 85000, "unit": "servis"},
        {"name": "Servis Rem Depan Belakang", "category": "Rem", "type": "service", "price": 150000, "unit": "servis"},
        {"name": "Ganti Ban (per ban)", "category": "Ban", "type": "service", "price": 250000, "unit": "buah"},
        {"name": "Tune Up Motor", "category": "Mesin", "type": "service", "price": 200000, "unit": "servis"},
        {"name": "Busi NGK Iridium", "category": "Spare Part", "type": "product", "price": 45000, "stock": 20, "unit": "buah"},
        {"name": "Oli Mesin Yamalube 1L", "category": "Oli", "type": "product", "price": 65000, "stock": 50, "unit": "botol"},
        {"name": "Aki Kering GS", "category": "Aki", "type": "product", "price": 320000, "stock": 8, "unit": "buah"},
        {"name": "Servis Karburator", "category": "Mesin", "type": "service", "price": 120000, "unit": "servis"},
        {"name": "Ganti Rantai Set", "category": "Transmisi", "type": "service", "price": 180000, "unit": "servis"},
        {"name": "Cuci Motor Premium", "category": "Kebersihan", "type": "service", "price": 25000, "unit": "unit"},
    ],
}

CUSTOMERS_BY_TYPE = {
    "warung": [
        {"name": "Pak Budi Santoso", "phone": "087711223344", "email": "budi.santoso@email.com", "address": "Jl. Kenangan No. 12, Surabaya"},
        {"name": "Bu Endah Rahayu", "phone": "087622334455", "email": "endah.rahayu@email.com", "address": "Jl. Mawar No. 5, Surabaya"},
        {"name": "Mas Agus Setiawan", "phone": "087533445566", "email": "agus.setiawan@email.com", "address": "Jl. Melati No. 8, Sidoarjo"},
        {"name": "Mbak Rina Puspita", "phone": "087444556677", "email": "rina.puspita@email.com", "address": "Jl. Anggrek No. 15, Surabaya"},
        {"name": "Pak Hendra Wijaya", "phone": "087355667788", "email": "hendra.wijaya@email.com", "address": "Jl. Flamboyan No. 3, Gresik"},
        {"name": "Bu Maria Susanti", "phone": "087266778899", "email": "maria.susanti@email.com", "address": "Jl. Dahlia No. 20, Surabaya"},
        {"name": "Mas Rizky Pratama", "phone": "087177889900", "email": "rizky.pratama@email.com", "address": "Jl. Bougenville No. 7, Surabaya"},
        {"name": "Bu Fitri Handayani", "phone": "087088990011", "email": "fitri.handayani@email.com", "address": "Jl. Tulip No. 9, Malang"},
    ],
    "salon": [
        {"name": "Mbak Ayu Lestari", "phone": "088111222333", "email": "ayu.lestari@email.com", "address": "Jl. Cihampelas No. 45, Bandung"},
        {"name": "Bu Desi Ratnawati", "phone": "088222333444", "email": "desi.ratnawati@email.com", "address": "Jl. Dago No. 12, Bandung"},
        {"name": "Neng Sinta Permata", "phone": "088333444555", "email": "sinta.permata@email.com", "address": "Jl. Setiabudhi No. 88, Bandung"},
        {"name": "Bu Yuli Hartini", "phone": "088444555666", "email": "yuli.hartini@email.com", "address": "Jl. Sukajadi No. 23, Bandung"},
        {"name": "Mbak Dina Kusuma", "phone": "088555666777", "email": "dina.kusuma@email.com", "address": "Jl. Pasteur No. 15, Bandung"},
        {"name": "Bu Tini Wulandari", "phone": "088666777888", "email": "tini.wulandari@email.com", "address": "Jl. Buah Batu No. 34, Bandung"},
        {"name": "Neng Lia Anggraini", "phone": "088777888999", "email": "lia.anggraini@email.com", "address": "Jl. Gatot Subroto No. 67, Bandung"},
        {"name": "Bu Wati Subekti", "phone": "088888999000", "email": "wati.subekti@email.com", "address": "Jl. Malabar No. 11, Bandung"},
    ],
    "bengkel": [
        {"name": "Mas Doni Prasetyo", "phone": "089111222333", "email": "doni.prasetyo@email.com", "address": "Jl. Parangtritis No. 5, Yogyakarta"},
        {"name": "Pak Slamet Riyadi", "phone": "089222333444", "email": "slamet.riyadi@email.com", "address": "Jl. Malioboro No. 88, Yogyakarta"},
        {"name": "Mas Tono Susilo", "phone": "089333444555", "email": "tono.susilo@email.com", "address": "Jl. Kaliurang No. 12, Sleman"},
        {"name": "Pak Widodo Harjo", "phone": "089444555666", "email": "widodo.harjo@email.com", "address": "Jl. Bantul No. 34, Bantul"},
        {"name": "Mas Bambang Irawan", "phone": "089555666777", "email": "bambang.irawan@email.com", "address": "Jl. Solo No. 56, Yogyakarta"},
        {"name": "Pak Dwi Hartono", "phone": "089666777888", "email": "dwi.hartono@email.com", "address": "Jl. Magelang No. 78, Sleman"},
        {"name": "Mas Rudi Santosa", "phone": "089777888999", "email": "rudi.santosa@email.com", "address": "Jl. Wates No. 90, Kulon Progo"},
        {"name": "Pak Eko Wahyudi", "phone": "089888999000", "email": "eko.wahyudi@email.com", "address": "Jl. Wonosari No. 11, Gunung Kidul"},
    ],
}

EXPENSES_BY_TYPE = {
    "warung": [
        {"name": "Belanja Bahan Masak", "amount": 850000, "category": "Bahan Baku"},
        {"name": "Gas LPG 12kg", "amount": 200000, "category": "Utilitas"},
        {"name": "Plastik & Kemasan", "amount": 150000, "category": "Perlengkapan"},
        {"name": "Bayar Listrik", "amount": 350000, "category": "Utilitas"},
        {"name": "Gaji Karyawan", "amount": 1500000, "category": "SDM"},
    ],
    "salon": [
        {"name": "Beli Produk Perawatan", "amount": 1200000, "category": "Bahan Baku"},
        {"name": "Bayar Sewa Tempat", "amount": 2000000, "category": "Sewa"},
        {"name": "Produk Salon L'Oreal", "amount": 800000, "category": "Bahan Baku"},
        {"name": "Bayar Listrik & Air", "amount": 450000, "category": "Utilitas"},
        {"name": "Gaji Stylist", "amount": 2500000, "category": "SDM"},
    ],
    "bengkel": [
        {"name": "Beli Spare Parts Stok", "amount": 3500000, "category": "Inventaris"},
        {"name": "Bayar Sewa Bengkel", "amount": 1500000, "category": "Sewa"},
        {"name": "Oli Bulk Purchase", "amount": 2000000, "category": "Bahan Baku"},
        {"name": "Bayar Listrik", "amount": 600000, "category": "Utilitas"},
        {"name": "Gaji Mekanik", "amount": 3000000, "category": "SDM"},
    ],
}

ORDER_STATUSES = [
    ("completed", "paid", 0.40),
    ("confirmed", "paid", 0.25),
    ("pending", "unpaid", 0.15),
    ("processing", "unpaid", 0.10),
    ("completed", "paid", 0.05),
    ("cancelled", "unpaid", 0.05),
]


# ─────────────────────────────────────────────────────────────────────────────
# SEEDER LOGIC
# ─────────────────────────────────────────────────────────────────────────────
async def seed_database():
    """Seed seluruh database dengan data demo."""

    # Setup engine
    db_url = settings.database_url
    if db_url.startswith("postgresql://"):
        db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)

    engine = create_async_engine(db_url, echo=False)
    AsyncSession = async_sessionmaker(bind=engine, expire_on_commit=False, autocommit=False)

    print("\n" + "═" * 60)
    print("  👻 Dedemit OS — Demo Data Seeder")
    print("═" * 60)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Schema database siap\n")

    for owner_data in OWNERS:
        business_type = owner_data["business_type"]

        async with AsyncSession() as session:
            # ── 1. Cek apakah owner sudah ada ────────────────────────────
            from sqlalchemy.future import select
            existing = await session.execute(
                select(UserModel).where(UserModel.email == owner_data["email"])
            )
            existing_user = existing.scalars().first()

            if existing_user:
                print(f"⚠️  Owner '{owner_data['store_name']}' sudah ada, dilewati.")
                continue

            # ── 2. Buat Owner ─────────────────────────────────────────────
            owner = UserModel(
                name=owner_data["name"],
                email=owner_data["email"],
                phone=owner_data["phone"],
                store_name=owner_data["store_name"],
                business_type=business_type,
                city=owner_data["city"],
                hashed_password=hash_password(owner_data["password"]),
                is_active=True,
            )
            session.add(owner)
            await session.flush()  # Get owner.id

            print(f"\n🏪 Membuat toko: {owner.store_name} ({owner.email})")

            # ── 3. Buat 10 Items ──────────────────────────────────────────
            items_data = ITEMS_BY_TYPE[business_type]
            items = []
            for item_d in items_data:
                item = ProductServiceModel(
                    user_id=owner.id,
                    name=item_d["name"],
                    category=item_d["category"],
                    type=item_d["type"],
                    description=f"Produk/jasa unggulan dari {owner.store_name}.",
                    price=float(item_d["price"]),
                    stock=item_d.get("stock") if item_d["type"] == "product" else None,
                    unit=item_d.get("unit", "pcs"),
                    is_active=True,
                )
                session.add(item)
                items.append(item)
            await session.flush()
            print(f"   ✅ {len(items)} produk/jasa ditambahkan")

            # ── 4. Buat 8 Customers ───────────────────────────────────────
            customers_data = CUSTOMERS_BY_TYPE[business_type]
            customers = []
            for cust_d in customers_data:
                cust = CustomerModel(
                    user_id=owner.id,
                    name=cust_d["name"],
                    phone=cust_d["phone"],
                    email=cust_d["email"],
                    address=cust_d["address"],
                )
                session.add(cust)
                customers.append(cust)
            await session.flush()
            print(f"   ✅ {len(customers)} pelanggan ditambahkan")

            # ── 5. Buat 15 Orders (30 hari history) ──────────────────────
            total_revenue = 0.0
            for i in range(15):
                # Pilih status berdasarkan distribusi probabilitas
                rand = random.random()
                cumulative = 0
                chosen_status, chosen_payment_status, _ = ORDER_STATUSES[-1]
                for s, ps, prob in ORDER_STATUSES:
                    cumulative += prob
                    if rand <= cumulative:
                        chosen_status, chosen_payment_status = s, ps
                        break

                # Pilih 1-3 items acak
                order_items_list = random.sample(items, min(random.randint(1, 3), len(items)))
                items_json = []
                subtotal = 0.0
                for prod in order_items_list:
                    qty = random.randint(1, 3)
                    items_json.append({
                        "product_id": prod.id,
                        "qty": qty,
                        "price": prod.price,
                    })
                    subtotal += prod.price * qty

                discount = random.choice([0, 0, 0, 5000, 10000, 15000])
                total = max(0.0, subtotal - discount)
                customer = random.choice(customers)

                order_date = random_date(30)
                payment_methods = ["transfer", "cash", "midtrans", "qris"]

                order = OrderModel(
                    user_id=owner.id,
                    customer_id=customer.id,
                    items=items_json,
                    subtotal=subtotal,
                    discount=float(discount),
                    total=total,
                    status=chosen_status,
                    payment_method=random.choice(payment_methods),
                    payment_status=chosen_payment_status,
                    payment_token=f"snap-token-demo-{i:04d}",
                    notes=random.choice([
                        "Tolong bungkus rapi!",
                        "Urgent, butuh cepat.",
                        None, None, None,
                    ]),
                )
                # Patch created_at untuk historical data
                order.created_at = order_date

                session.add(order)

                if chosen_payment_status == "paid":
                    total_revenue += total

                # Notifikasi untuk order
                notif = NotificationModel(
                    user_id=owner.id,
                    type="order",
                    title="Pesanan Masuk" if chosen_status == "pending" else "Pembayaran Diterima",
                    message=f"Order {idr(total)} — Status: {chosen_status}",
                )
                session.add(notif)

            await session.flush()
            print(f"   ✅ 15 order dibuat (estimasi revenue: {idr(total_revenue)})")

            # ── 6. Buat 5 Expenses ────────────────────────────────────────
            expenses_data = EXPENSES_BY_TYPE[business_type]
            for exp_d in expenses_data:
                expense_date = random_date(30).date()
                expense = ExpenseModel(
                    user_id=owner.id,
                    description=exp_d["name"],
                    amount=float(exp_d["amount"]),
                    category=exp_d["category"],
                    date=expense_date,
                )
                session.add(expense)

            await session.flush()
            print(f"   ✅ 5 pengeluaran dicatat")

            # ── 7. Notifikasi Selamat Datang ──────────────────────────────
            welcome_notif = NotificationModel(
                user_id=owner.id,
                type="system",
                title="🎉 Selamat Datang di Dedemit OS!",
                message=(
                    f"Halo {owner.name}! Toko {owner.store_name} kamu sudah aktif. "
                    "Mulai kelola bisnis lebih cerdas dengan AI! 👻"
                ),
            )
            session.add(welcome_notif)

            await session.commit()
            print(f"   💾 Data {owner.store_name} berhasil disimpan!")

    print("\n" + "═" * 60)
    print("  🎉 Seeding selesai! Data demo siap digunakan.")
    print("═" * 60)
    print("\n  📝 Akun Demo:")
    for owner in OWNERS:
        print(f"     • {owner['store_name']}")
        print(f"       Email: {owner['email']}")
        print(f"       Password: {owner['password']}")
    print("\n  🚀 Akses dashboard: http://localhost:3000")
    print("  📚 API Docs: http://localhost:8000/docs\n")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(seed_database())
