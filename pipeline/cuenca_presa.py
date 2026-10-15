"""Cuenca aguas arriba de una presa con HydroBASINS nivel 12 (HydroSHEDS, WWF).

Se ubica la subcuenca que contiene la cortina y se suman todas las que drenan hacia ella
(campo NEXT_DOWN). El error es del tamaño de una subcuenca de nivel 12 (decenas de km²).
"""
import json
from pathlib import Path

import shapefile
from shapely.geometry import Point, mapping, shape
from shapely.ops import unary_union

RAW = Path(__file__).resolve().parent / "raw"
ZIP = RAW / "hybas_na_lev12.zip"
URL = "https://data.hydrosheds.org/file/HydroBASINS/standard/hybas_na_lev12_v1c.zip"
CAJA = (-101.5, 24.0, -99.0, 26.5)


def cuenca(nombre, lon, lat):
    salida = RAW / f"cuenca_{nombre}.geojson"
    if salida.exists():
        return shape(json.loads(salida.read_text())["geometry"])
    if not ZIP.exists():
        import requests
        ZIP.write_bytes(requests.get(URL, timeout=600).content)
    r = shapefile.Reader(str(ZIP))
    campos = [f[0] for f in r.fields[1:]]
    i_id, i_down = campos.index("HYBAS_ID"), campos.index("NEXT_DOWN")
    geoms, abajo = {}, {}
    for sr in r.iterShapeRecords():
        x0, y0, x1, y1 = sr.shape.bbox
        if x1 < CAJA[0] or x0 > CAJA[2] or y1 < CAJA[1] or y0 > CAJA[3]:
            continue
        hid = sr.record[i_id]
        geoms[hid] = shape(sr.shape.__geo_interface__)
        abajo[hid] = sr.record[i_down]
    pt = Point(lon, lat)
    origen = next(h for h, g in geoms.items() if g.contains(pt))
    arriba = {}
    for h, d in abajo.items():
        arriba.setdefault(d, []).append(h)
    pila, dentro = [origen], set()
    while pila:
        h = pila.pop()
        if h not in dentro:
            dentro.add(h)
            pila += arriba.get(h, [])
    poligono = unary_union([geoms[h] for h in dentro])
    salida.write_text(json.dumps({"type": "Feature", "properties": {"subcuencas": len(dentro)},
                                  "geometry": mapping(poligono)}))
    return poligono


if __name__ == "__main__":
    g = cuenca("la_boca", -100.128056, 25.428056)
    print(f"La Boca: {g.area * 111 * 111 * 0.9:.0f} km² aprox., límites {tuple(round(x, 3) for x in g.bounds)}")
