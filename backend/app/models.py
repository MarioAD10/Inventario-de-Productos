from decimal import Decimal

from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Clase base de la que heredan todos los modelos."""


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    descripcion: Mapped[str | None] = mapped_column(String(500), default=None)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    cantidad: Mapped[int] = mapped_column(Integer, default=0)