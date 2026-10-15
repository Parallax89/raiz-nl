import os
import sys
import tempfile
from pathlib import Path

_tmp = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{_tmp}/prueba.db"
os.environ["BOT_ENABLED"] = "false"
os.environ["OPERATOR_TOKEN"] = "tok"
os.environ["FICHAS_PATH"] = f"{_tmp}/no_existe.json"   # siembra desde el GeoJSON del portal
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def client():
    from app.main import app
    from app.db import SessionLocal
    from app.seed import sembrar
    with TestClient(app) as c:
        with SessionLocal() as db:
            sembrar(db, reset=True)
        yield c
