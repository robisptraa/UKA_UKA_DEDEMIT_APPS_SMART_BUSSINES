"""
Dedemit OS — pytest Integration Test Fixtures
Menyediakan async test client, in-memory SQLite database, dan test user factories.
"""
import asyncio
import pytest
import pytest_asyncio
from typing import AsyncGenerator, Generator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy import StaticPool

# Override environment SEBELUM import app
import os
os.environ["ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["JWT_SECRET"] = "test_jwt_secret_for_integration_tests_only"
os.environ["REDIS_URL"] = ""  # Disable Redis di test
os.environ["MIDTRANS_SERVER_KEY"] = "test-server-key"
os.environ["TELEGRAM_BOT_TOKEN"] = ""

from app.main import app
from app.database import Base, get_async_db


# ─────────────────────────────────────────────────────────────────────────────
# SQLite In-Memory Engine untuk isolasi test yang cepat
# ─────────────────────────────────────────────────────────────────────────────
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False,
)

TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# ─────────────────────────────────────────────────────────────────────────────
# Session-scoped event loop untuk semua async tests
# ─────────────────────────────────────────────────────────────────────────────
@pytest.fixture(scope="session")
def event_loop():
    """Override default event loop dengan session-scoped loop."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


# ─────────────────────────────────────────────────────────────────────────────
# Setup/Teardown Database per test session
# ─────────────────────────────────────────────────────────────────────────────
@pytest_asyncio.fixture
async def setup_test_db():
    """Buat semua tabel di in-memory database sebelum tests, hapus setelah selesai."""
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# ─────────────────────────────────────────────────────────────────────────────
# DB Session Override — ganti dependency FastAPI dengan test session
# ─────────────────────────────────────────────────────────────────────────────
@pytest_asyncio.fixture
async def db_session(setup_test_db) -> AsyncGenerator[AsyncSession, None]:
    """Async database session untuk setiap test dengan rollback otomatis."""
    async with TestingSessionLocal() as session:
        yield session
        await session.rollback()


# ─────────────────────────────────────────────────────────────────────────────
# HTTP Test Client
# ─────────────────────────────────────────────────────────────────────────────
@pytest_asyncio.fixture
async def client(db_session) -> AsyncGenerator[AsyncClient, None]:
    """AsyncClient yang terhubung ke FastAPI app dengan DB override."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_async_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


# ─────────────────────────────────────────────────────────────────────────────
# Helper Fixtures: Registered & Logged-in Users
# ─────────────────────────────────────────────────────────────────────────────
@pytest_asyncio.fixture
async def registered_user(client: AsyncClient) -> dict:
    """Mendaftarkan dan mengembalikan data pengguna baru."""
    user_data = {
        "name": "Budi Test",
        "email": f"budi.test.{os.getpid()}@dedemit.id",
        "phone": "081234567890",
        "store_name": "Warung Test Budi",
        "business_type": "warung",
        "city": "Jakarta",
        "password": "TestPassword123!",
    }
    resp = await client.post("/api/v1/auth/register", json=user_data)
    assert resp.status_code == 201, f"Register gagal: {resp.text}"
    return {**user_data, "id": resp.json()["id"]}


@pytest_asyncio.fixture
async def auth_headers(client: AsyncClient, registered_user: dict) -> dict:
    """Login dan kembalikan Authorization header untuk user yang sudah terdaftar."""
    resp = await client.post("/api/v1/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"],
    })
    assert resp.status_code == 200, f"Login gagal: {resp.text}"
    # TokenResponse menggunakan alias_generator → accessToken (camelCase)
    token = resp.json()["accessToken"]
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def sample_item(client: AsyncClient, auth_headers: dict) -> dict:
    """Membuat satu item sample dan mengembalikan data-nya."""
    item_data = {
        "name": "Baju Thrift Vintage Keren",
        "category": "Pakaian",
        "type": "product",
        "description": "Baju vintage kondisi sangat bagus, bahan katun premium.",
        "price": 85000.0,
        "stock": 10,
        "unit": "pcs",
        "is_active": True,
    }
    resp = await client.post("/api/v1/items", json=item_data, headers=auth_headers)
    assert resp.status_code == 201, f"Create item gagal: {resp.text}"
    return resp.json()


@pytest_asyncio.fixture
async def sample_customer(client: AsyncClient, auth_headers: dict) -> dict:
    """Membuat satu pelanggan sample."""
    customer_data = {
        "name": "Pelanggan Test",
        "phone": "087654321098",
        "email": "pelanggan@test.com",
        "address": "Jl. Test No. 1, Jakarta",
    }
    resp = await client.post("/api/v1/customers", json=customer_data, headers=auth_headers)
    assert resp.status_code == 201, f"Create customer gagal: {resp.text}"
    return resp.json()
