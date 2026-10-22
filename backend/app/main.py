from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.database import engine

app = FastAPI(title="CRUD de productos")


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