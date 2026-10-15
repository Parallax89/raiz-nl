"""Verdor actual (NDVI de Sentinel-2) de una celda: ¿la cicatriz se regeneró sola?

Usa el catálogo abierto de Microsoft Planetary Computer (no pide cuenta para leer).
Para cada celda toma hasta 3 escenas de la temporada seca (febrero a mayo) con menos de 15 %
de nubes, calcula el NDVI medio de la celda en cada una y se queda con la mediana.
"""
import json
import statistics
from pathlib import Path

import numpy as np
import planetary_computer
import rasterio
from pystac_client import Client
from rasterio.warp import transform_bounds
from rasterio.windows import from_bounds

CACHE = Path(__file__).resolve().parent / "raw" / "ndvi_cache.json"
CATALOGO = "https://planetarycomputer.microsoft.com/api/stac/v1"


def _lee(href, bounds):
    with rasterio.open(href) as src:
        b = transform_bounds("EPSG:4326", src.crs, *bounds)
        return src.read(1, window=from_bounds(*b, src.transform), boundless=True, fill_value=0).astype("float32")


def ndvi_celda(bounds, temporada="2026-02-01/2026-05-31"):
    """bounds = (lon_min, lat_min, lon_max, lat_max). Devuelve (ndvi, n_escenas)."""
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    clave = f"{bounds}|{temporada}"
    if clave in cache:
        return tuple(cache[clave])
    cat = Client.open(CATALOGO, modifier=planetary_computer.sign_inplace)
    items = list(cat.search(collections=["sentinel-2-l2a"], bbox=bounds, datetime=temporada,
                            query={"eo:cloud_cover": {"lt": 15}}).items())
    items.sort(key=lambda it: it.properties["eo:cloud_cover"])
    valores = []
    for it in items[:3]:
        try:
            rojo, nir = _lee(it.assets["B04"].href, bounds), _lee(it.assets["B08"].href, bounds)
        except Exception:
            continue
        ok = (rojo > 0) & (nir > 0)
        if ok.sum() < 100:
            continue
        nd = (nir[ok] - rojo[ok]) / (nir[ok] + rojo[ok])
        valores.append(float(np.nanmean(nd)))
    resultado = (round(statistics.median(valores), 3) if valores else None, len(valores))
    cache[clave] = resultado
    CACHE.write_text(json.dumps(cache))
    return resultado


if __name__ == "__main__":
    # Prueba: celda de Ciénega de González (Santiago)
    print(ndvi_celda((-100.24, 25.36, -100.22, 25.38)))
