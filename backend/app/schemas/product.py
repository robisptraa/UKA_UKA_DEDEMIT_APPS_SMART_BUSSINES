# Mengimpor skema Item sebagai alias Product demi menjaga kompatibilitas impor lama
from app.schemas.item import ItemResponse as ProductResponse
from app.schemas.item import ItemCreate as ProductCreate
from app.schemas.item import ItemUpdate as ProductUpdate
