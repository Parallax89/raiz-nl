"""Siembra la tabla de zonas.

Orden de preferencia:
1. backend/data/fichas.json (fichas curadas a mano, fase 1 del Contexto).
2. web/data/zonas.geojson (lo que escribe el pipeline): así mapa y API comparten id y nombre.
3. web/data/mock/zonas.geojson, marcado como mock.

Uso: python -m app.seed --reset
"""
import argparse
import json
import re
from pathlib import Path

from sqlalchemy import delete

from .db import Base, SessionLocal, engine
from .models import Donacion, Publicacion, Zona
from .settings import settings

OPERADOR = "Por definir (Pronatura Noreste, municipio o ejido)"
RE_PRESA = re.compile(r"presa\s+(El Cuchillo|La Boca|Cerro Prieto)", re.I)
RE_ACUIFERO = re.compile(r"acuífero en déficit:\s*([^;.,]+)", re.I)
RE_ESTACION = re.compile(r"estación\s+([A-ZÁÉÍÓÚÑ0-9 ]+?)(?:\)|$|\s*·|,)")


def _titulo_estacion(nombre: str) -> str:
    return " ".join(p.capitalize() if not p.isdigit() else p for p in nombre.strip().split())


def ficha_desde_feature(f: dict, mock: bool) -> dict:
    p = f["properties"]
    razones = p.get("razones") or []
    todo = " ; ".join([p.get("nombre", "")] + razones)
    nombre = p["nombre"]
    corto = nombre.split("·", 1)[-1].split("→", 1)[0].strip()
    presa = RE_PRESA.search(todo)
    acuifero = RE_ACUIFERO.search(todo)
    estacion = RE_ESTACION.search(todo)
    centro = p.get("centro") or [None, None]
    ficha = dict(
        id=p["id"], objetivo=p["objetivo"], nombre=nombre, municipio=p.get("municipio", ""),
        razon=("; ".join(razones) + ".") if razones else "", operador=OPERADOR,
        arboles_caben=int(p.get("arboles_caben") or settings.cupo_por_zona), mock=mock,
        lat=centro[0], lon=centro[1],
        presa_destino=(presa.group(1) if presa and p["objetivo"] == "agua" else None),
        acuifero_destino=(acuifero.group(1).strip() if acuifero and p["objetivo"] == "agua" else None),
        estacion_sima=(estacion.group(1).strip() if estacion and p["objetivo"] == "aire" else None),
    )
    if p["objetivo"] == "agua":
        ficha["nombre_texto"] = corto
        if not ficha["presa_destino"] and not ficha["acuifero_destino"]:
            ficha["descartada"] = True
            ficha["motivo_descarte"] = "No aporta a una presa de abastecimiento ni a un acuífero identificado"
    else:
        est = ficha["estacion_sima"]
        ficha["nombre_texto"] = f"los alrededores de la estación {_titulo_estacion(est)} del SIMA" if est else corto
    return ficha


def cargar_fichas() -> list[dict]:
    curadas = Path(settings.fichas_path)
    if curadas.exists():
        return json.loads(curadas.read_text())
    for ruta, mock in [(settings.zonas_geojson, False), (settings.zonas_geojson_mock, True)]:
        if Path(ruta).exists():
            fc = json.loads(Path(ruta).read_text())
            return [ficha_desde_feature(f, mock) for f in fc["features"]]
    raise FileNotFoundError("No hay fichas ni zonas.geojson para sembrar")


def sembrar(db, reset=False):
    if reset:
        db.execute(delete(Publicacion))
        db.execute(delete(Donacion))
        db.execute(delete(Zona))
    if db.query(Zona).count():
        return 0
    fichas = cargar_fichas()
    for f in fichas:
        db.add(Zona(**{k: v for k, v in f.items() if hasattr(Zona, k)}))
    db.commit()
    return len(fichas)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--reset", action="store_true", help="borra zonas y donaciones y vuelve a sembrar")
    a = ap.parse_args()
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        n = sembrar(db, reset=a.reset)
        print(f"{n} zonas sembradas" if n else "La tabla ya tenía zonas (usa --reset para volver a sembrar)")
