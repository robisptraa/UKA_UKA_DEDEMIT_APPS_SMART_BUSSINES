from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.config import settings

# Konfigurasi URL database asinkron
db_url = settings.database_url
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif db_url.startswith("postgresql://"):
    db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)

# Membuat engine asinkron untuk PostgreSQL menggunakan driver asyncpg
engine = create_async_engine(
    db_url,
    pool_pre_ping=True, # Memvalidasi koneksi sebelum digunakan
    echo=False,         # Set ke True jika ingin log SQL query lengkap
)

# Membuat sessionmaker asinkron untuk memproduksi AsyncSession
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)

# Base class untuk mendefinisikan model database SQLAlchemy
Base = declarative_base()

# Dependency FastAPI untuk mendapatkan session database asinkron per request
async def get_async_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
