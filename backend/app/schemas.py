from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = Field(default=None, max_length=500)
    precio: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    cantidad: int = Field(default=0, ge=0)


class ProductoCrear(ProductoBase):
    """Datos para crear un producto."""


class ProductoActualizar(ProductoBase):
    """Datos para editar un producto (se envía el producto completo)."""


class ProductoLeer(ProductoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)