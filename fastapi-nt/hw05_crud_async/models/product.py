from sqlalchemy import String, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column

from db.base import Base

class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str | None ] = mapped_column(String(1000), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(10,2), nullable=False)
    stock: Mapped[int] = mapped_column(Integer, default=0)


    
    