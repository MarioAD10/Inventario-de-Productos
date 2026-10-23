import os
from pathlib import Path

import pytest
from dotenv import load_dotenv
from sqlalchemy.engine import make_url

load_dotenv(Path(__file__).resolve().parent.parent.parent / ".env")

test_url = os.environ.get("TEST_DATABASE_URL")
if not test_url:
    test_url = (
        make_url(os.environ["DATABASE_URL"])
        .set(database="crud_test")
        .render_as_string(hide_password=False)
    )


assert make_url(test_url).database.endswith("_test"), "La BD de pruebas debe terminar en _test"


os.environ["DATABASE_URL"] = test_url

from fastapi.testclient import TestClient  

from app.database import engine  
from app.main import app  
from app.models import Base 


@pytest.fixture(autouse=True)
def tablas_limpias():
    """Antes de cada prueba, recrea las tablas vacías."""
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)