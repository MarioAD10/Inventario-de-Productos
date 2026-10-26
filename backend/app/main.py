from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from pathlib import Path
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine
from app.models import Producto
from app.schemas import ProductoActualizar, ProductoCrear, ProductoLeer

app = FastAPI(title="CRUD de productos")


def get_db():
    """Abre una sesión por petición y la cierra al terminar."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/health/db")
def health_db():
    try:
        with engine.connect() as conn:
            version = conn.execute(text("SELECT version()")).scalar()
        return {"status": "ok", "database": version}
    except Exception:
        raise HTTPException(status_code=503, detail="No se pudo conectar a la base de datos")


def obtener_o_404(db: Session, producto_id: int) -> Producto:
    producto = db.get(Producto, producto_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@app.get("/productos", response_model=list[ProductoLeer])
def listar_productos(db: DbSession):
    return db.scalars(select(Producto).order_by(Producto.id)).all()


@app.post("/productos", response_model=ProductoLeer, status_code=status.HTTP_201_CREATED)
def crear_producto(datos: ProductoCrear, db: DbSession):
    producto = Producto(**datos.model_dump())
    db.add(producto)
    db.commit()
    db.refresh(producto)
    return producto


@app.get("/productos/{producto_id}", response_model=ProductoLeer)
def leer_producto(producto_id: int, db: DbSession):
    return obtener_o_404(db, producto_id)


@app.put("/productos/{producto_id}", response_model=ProductoLeer)
def editar_producto(producto_id: int, datos: ProductoActualizar, db: DbSession):
    producto = obtener_o_404(db, producto_id)
    for campo, valor in datos.model_dump().items():
        setattr(producto, campo, valor)
    db.commit()
    db.refresh(producto)
    return producto


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_producto(producto_id: int, db: DbSession):
    producto = obtener_o_404(db, producto_id)
    db.delete(producto)
    db.commit()

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{ruta:path}", include_in_schema=False)
    def frontend(ruta: str):
        archivo = (STATIC_DIR / ruta).resolve()
        if ruta and archivo.is_file() and STATIC_DIR.resolve() in archivo.parents:
            return FileResponse(archivo)
        return FileResponse(STATIC_DIR / "index.html")