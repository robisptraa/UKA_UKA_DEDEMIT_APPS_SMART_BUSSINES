from app.database import Base
from app.models.user import UserModel
from app.models.product_service import ProductServiceModel
from app.models.customer import CustomerModel
from app.models.order import OrderModel
from app.models.payment_proof import PaymentProofModel
from app.models.expense import ExpenseModel
from app.models.stock_movement import StockMovementModel
from app.models.notification import NotificationModel

# Ekspor semua model agar terdeteksi secara otomatis (autogenerate) oleh Alembic
__all__ = [
    "Base",
    "UserModel",
    "ProductServiceModel",
    "CustomerModel",
    "OrderModel",
    "PaymentProofModel",
    "ExpenseModel",
    "StockMovementModel",
    "NotificationModel"
]
