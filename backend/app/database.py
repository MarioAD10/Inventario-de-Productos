import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Carga el .env de la raíz del proyecto 
load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

DATABASE_URL = os.environ["DATABASE_URL"]

# El engine es el puente hacia PostgreSQL
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Cada petición abrirá una sesión para hablar con la base
SessionLocal = sessionmaker(bind=engine, autoflush=False)