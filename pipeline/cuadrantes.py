"""Cuadrantes prioritarios dentro de cada zona (lo que una brigada puede trabajar).

Sierra (zonas de agua): cuadrantes de 250 m en una ventana de 5 km alrededor de cada zona.
  Entran si hubo fuego (detección satelital 2016-2025 en el cuadrante o registro de incendio en bosque
  de CONAGUA a menos de 1.5 km), si es zona de bosque o matorral (ESA WorldCover), si la pendiente media
  es de 35° o menos (Copernicus DEM 30 m) y si drena a una presa de abastecimiento o recarga un acuífero
  de la zona metropolitana. Se ordenan por:
    50 % verdor perdido: NDVI de Sentinel-2 (temporada seca 2026) contra el bosque vecino sin fuego
         (percentil 90 de los cuadrantes con más de 50 % de copa y sin evidencia de fuego);
    30 % acceso: distancia al camino o brecha más cercana (OpenStreetMap);
    20 % pendiente: más suave, más fácil de plantar.

Ciudad (municipios del reto 3): cuadrantes de 500 m a menos de 3 km de cada estación del SIMA,
  sólo urbanos (40 % o más construido según WorldCover) y fuera de zonas industriales (OpenStreetMap). Se ordenan por:
    35 % calor de superficie (Landsat 8/9, verano 2026); 35 % falta de vegetación (NDVI);
    30 % gente: superficie construida y escuelas, guarderías, hospitales y clínicas (OpenStreetMap).

Todo lo consultado queda en investigacion/fuentes/cuadrantes/ y investigacion/fuentes/osm/: al volver a
correr no se descarga nada. Salida: web/data/cuadrantes.geojson.

Uso: python pipeline/cuadrantes.py
"""
import csv
import json
import math
import time
from pathlib import Path

import numpy as np
import requests

REPO = Path(__file__).resolve().parents[1]
FUENTES = REPO / "investigacion" / "fuentes"
CACHE = FUENTES / "cuadrantes"
OSM = FUENTES / "osm"
SALIDA = REPO / "web" / "data" / "cuadrantes.geojson"
CACHE.mkdir(parents=True, exist_ok=True)
OSM.mkdir(parents=True, exist_ok=True)
CATALOGO = "https://planetarycomputer.microsoft.com/api/stac/v1"
UA = {"User-Agent": "RaizNL-hackathon/0.1 (https://github.com/c7b/raiz-nl)"}
BOSQUE = ("bosque", "pino", "encino", "oyamel", "táscate", "tascate")

SIERRA = dict(lado_m=250, ventana_m=5000, por_zona=4, separacion_m=500)
CIUDAD = dict(lado_m=500, ventana_m=6000, por_zona=3, separacion_m=1000)


# ---------------- malla local ----------------
def malla(lat, lon, lado_m, ventana_m):
    n = int(ventana_m // lado_m)
    dlat = lado_m / 111_000
    dlon = lado_m / (111_000 * math.cos(math.radians(lat)))
    return dict(n=n, dlat=dlat, dlon=dlon, lat0=lat - n / 2 * dlat, lon0=lon - n / 2 * dlon,
                bounds=(lon - n / 2 * dlon, lat - n / 2 * dlat, lon + n / 2 * dlon, lat + n / 2 * dlat))


def indice(g, lat, lon):
    i = np.floor((np.asarray(lat) - g["lat0"]) / g["dlat"]).astype(int)
    j = np.floor((np.asarray(lon) - g["lon0"]) / g["dlon"]).astype(int)
    ok = (i >= 0) & (i < g["n"]) & (j >= 0) & (j < g["n"])
    return i, j, ok


def centro_celda(g, i, j):
    return g["lat0"] + (i + 0.5) * g["dlat"], g["lon0"] + (j + 0.5) * g["dlon"]


# ---------------- lectura de rásters (Planetary Computer, sin cuenta) ----------------
def _cliente():
    import planetary_computer as pc
    from pystac_client import Client
    return Client.open(CATALOGO, modifier=pc.sign_inplace)


def _pixeles(href, bounds):
    """Valores y lon/lat de cada píxel del recuadro."""
    import rasterio
    from rasterio.warp import transform as reproyecta, transform_bounds
    from rasterio.windows import from_bounds
    with rasterio.open(href) as src:
        b = transform_bounds("EPSG:4326", src.crs, *bounds)
        win = from_bounds(*b, src.transform)
        arr = src.read(1, window=win, boundless=True, fill_value=0).astype("float64")
        tr, crs = src.window_transform(win), src.crs
    h, w = arr.shape
    cols, rows = np.meshgrid(np.arange(w) + 0.5, np.arange(h) + 0.5)
    xs = tr.c + cols * tr.a + rows * tr.b
    ys = tr.f + cols * tr.d + rows * tr.e
    if crs.to_epsg() != 4326:
        lon, lat = reproyecta(crs, "EPSG:4326", xs.ravel(), ys.ravel())
        lon, lat = np.array(lon).reshape(h, w), np.array(lat).reshape(h, w)
    else:
        lon, lat = xs, ys
    return arr, lon, lat, tr


def _media(g, valores, lon, lat, valido):
    i, j, ok = indice(g, lat, lon)
    ok &= valido
    idx = (i * g["n"] + j)[ok]
    suma = np.bincount(idx, weights=valores[ok], minlength=g["n"] ** 2)
    cuenta = np.bincount(idx, minlength=g["n"] ** 2)
    return suma, cuenta


def ndvi(cat, g, temporada="2026-02-01/2026-05-31"):
    items = sorted(cat.search(collections=["sentinel-2-l2a"], bbox=g["bounds"], datetime=temporada,
                              query={"eo:cloud_cover": {"lt": 15}}).items(),
                   key=lambda it: it.properties["eo:cloud_cover"])[:3]
    capas = []
    for it in items:
        rojo, lon, lat, _ = _pixeles(it.assets["B04"].href, g["bounds"])
        nir, _, _, _ = _pixeles(it.assets["B08"].href, g["bounds"])
        ok = (rojo > 0) & (nir > 0)
        nd = np.where(ok, (nir - rojo) / np.maximum(nir + rojo, 1), 0)
        s, c = _media(g, nd, lon, lat, ok)
        capas.append(np.where(c > 0, s / np.maximum(c, 1), np.nan))
    return np.nanmedian(np.vstack(capas), axis=0) if capas else np.full(g["n"] ** 2, np.nan)


def pendiente(cat, g):
    suma = np.zeros(g["n"] ** 2)
    cuenta = np.zeros(g["n"] ** 2)
    for it in cat.search(collections=["cop-dem-glo-30"], bbox=g["bounds"]).items():
        z, lon, lat, tr = _pixeles(it.assets["data"].href, g["bounds"])
        lat_c = float(np.mean(lat))
        dy = abs(tr.e) * 111_000
        dx = abs(tr.a) * 111_000 * math.cos(math.radians(lat_c))
        gy, gx = np.gradient(z, dy, dx)
        p = np.degrees(np.arctan(np.hypot(gx, gy)))
        s, c = _media(g, p, lon, lat, z > 0)
        suma += s
        cuenta += c
    return np.where(cuenta > 0, suma / np.maximum(cuenta, 1), np.nan)


def cobertura(cat, g, clases):
    """Fracción del cuadrante en cada clase de ESA WorldCover 2021."""
    total = np.zeros(g["n"] ** 2)
    por_clase = {k: np.zeros(g["n"] ** 2) for k in clases}
    for it in cat.search(collections=["esa-worldcover"], bbox=g["bounds"]).items():
        m, lon, lat, _ = _pixeles(it.assets["map"].href, g["bounds"])
        _, c = _media(g, np.ones_like(m), lon, lat, m > 0)
        total += c
        for k in clases:
            s, _ = _media(g, (m == k).astype(float), lon, lat, m > 0)
            por_clase[k] += s
    return {k: np.where(total > 0, v / np.maximum(total, 1), np.nan) for k, v in por_clase.items()}


def temperatura(cat, g, temporada="2026-06-01/2026-08-31"):
    items = sorted(cat.search(collections=["landsat-c2-l2"], bbox=g["bounds"], datetime=temporada,
                              query={"eo:cloud_cover": {"lt": 10}, "platform": {"in": ["landsat-8", "landsat-9"]}}).items(),
                   key=lambda it: it.properties["eo:cloud_cover"])[:2]
    capas = []
    for it in items:
        dn, lon, lat, _ = _pixeles(it.assets["lwir11"].href, g["bounds"])
        ok = dn > 0
        c_ = dn * 0.00341802 + 149.0 - 273.15
        s, c = _media(g, c_, lon, lat, ok)
        capas.append(np.where(c > 0, s / np.maximum(c, 1), np.nan))
    return np.nanmean(np.vstack(capas), axis=0) if capas else np.full(g["n"] ** 2, np.nan)


# ---------------- OpenStreetMap ----------------
def overpass(nombre, bounds, consulta):
    archivo = OSM / f"{nombre}.json"
    if archivo.exists():
        return json.loads(archivo.read_text())
    w, s, e, n = bounds
    q = f"[out:json][timeout:90];({consulta.format(bbox=f'{s},{w},{n},{e}')};);out geom;"
    for intento in range(4):
        r = requests.post("https://overpass-api.de/api/interpreter", data={"data": q}, headers=UA, timeout=120)
        if r.status_code == 200:
            archivo.write_text(r.text)
            return r.json()
        print(f"    Overpass respondió {r.status_code}: {r.text[:120]}"); time.sleep(10 * (intento + 1))
    r.raise_for_status()


def distancia_a_caminos(osm, g, lat_ref):
    """Distancia (m) del centro de cada cuadrante al camino o brecha más cercana."""
    from shapely.geometry import LineString, Point
    from shapely.ops import unary_union
    kx = 111_000 * math.cos(math.radians(lat_ref))
    lineas = [LineString([((p["lon"] - g["lon0"]) * kx, (p["lat"] - g["lat0"]) * 111_000) for p in el["geometry"]])
              for el in osm["elements"] if el["type"] == "way" and "highway" in el.get("tags", {}) and len(el.get("geometry", [])) > 1]
    red = unary_union(lineas) if lineas else None
    salida = np.full(g["n"] ** 2, np.nan)
    for k in range(g["n"] ** 2):
        i, j = divmod(k, g["n"])
        la, lo = centro_celda(g, i, j)
        if red is not None:
            salida[k] = red.distance(Point((lo - g["lon0"]) * kx, (la - g["lat0"]) * 111_000))
    return salida


def lugares(osm):
    return [(el["tags"]["name"], el["lat"], el["lon"]) for el in osm["elements"]
            if el["type"] == "node" and "place" in el.get("tags", {}) and "name" in el["tags"]]


def mas_cercano(lista, lat, lon, max_m):
    mejor = None
    for nombre, la, lo in lista:
        d = math.hypot((la - lat) * 111_000, (lo - lon) * 111_000 * math.cos(math.radians(lat)))
        if d <= max_m and (mejor is None or d < mejor[1]):
            mejor = (nombre, d)
    return mejor


MUNICIPIOS = {"Benito Juárez": "Juárez"}   # así nombra OpenStreetMap al municipio de Juárez, N.L.


def plural(n, uno, varios):
    return f"{n} {uno if n == 1 else varios}"


def nominatim(lat, lon, zoom=16):
    r = requests.get("https://nominatim.openstreetmap.org/reverse", headers=UA, timeout=30,
                     params=dict(lat=lat, lon=lon, format="jsonv2", zoom=zoom, addressdetails=1, **{"accept-language": "es"}))
    time.sleep(1.1)   # política de uso: una consulta por segundo
    a = r.json().get("address", {}) if r.ok else {}
    colonia = a.get("neighbourhood") or a.get("suburb") or a.get("quarter") or a.get("residential")
    municipio = a.get("city") or a.get("town") or a.get("municipality") or a.get("county")
    return colonia, MUNICIPIOS.get(municipio, municipio)


# ---------------- utilidades ----------------
def lista_corta(filas, n, sep_m):
    elegidos = []
    for f in sorted(filas, key=lambda f: -f["score"]):
        if all(math.hypot((f["lat"] - e["lat"]) * 111_000,
                          (f["lon"] - e["lon"]) * 111_000 * math.cos(math.radians(f["lat"]))) >= sep_m for e in elegidos):
            elegidos.append(f)
        if len(elegidos) == n:
            break
    return elegidos


def poligono(g, i, j):
    la, lo = g["lat0"] + i * g["dlat"], g["lon0"] + j * g["dlon"]
    return {"type": "Polygon", "coordinates": [[[lo, la], [lo + g["dlon"], la], [lo + g["dlon"], la + g["dlat"]],
                                                [lo, la + g["dlat"]], [lo, la]]]}


def norm(v):
    v = np.asarray(v, float)
    lo, hi = np.nanmin(v), np.nanmax(v)
    return (v - lo) / (hi - lo) if hi > lo else np.zeros_like(v)


def r(x, d=2):
    return None if x is None or (isinstance(x, float) and math.isnan(x)) else round(float(x), d)


# ---------------- sierra ----------------
def tabla_sierra(z, cat):
    archivo = CACHE / f"{z['id']}.json"
    if archivo.exists():
        return json.loads(archivo.read_text())
    la, lo = z["centro"]
    g = malla(la, lo, SIERRA["lado_m"], SIERRA["ventana_m"])
    print(f"  {z['id']}: verdor, pendiente, cobertura y caminos…")
    nd = ndvi(cat, g)
    pend = pendiente(cat, g)
    cob = cobertura(cat, g, [10, 20])
    osm = overpass(z["id"], g["bounds"], 'way["highway"]({bbox});node["place"]({bbox})')
    dist = distancia_a_caminos(osm, g, la)
    filas = []
    for k in range(g["n"] ** 2):
        i, j = divmod(k, g["n"])
        cla, clo = centro_celda(g, i, j)
        filas.append(dict(i=i, j=j, lat=cla, lon=clo, ndvi=r(nd[k], 3), pendiente=r(pend[k], 1),
                          arbol=r(cob[10][k], 3), matorral=r(cob[20][k], 3), camino_m=r(dist[k], 0)))
    tabla = dict(zona=z["id"], malla=g, lugares=lugares(osm), cuadrantes=filas)
    archivo.write_text(json.dumps(tabla))
    return tabla


def sierra(zonas, cat):
    from shapely.geometry import Point, shape
    from shapely.ops import unary_union
    cuencas = unary_union([shape(f["geometry"]) for f in json.loads((REPO / "web/data/cuencas.geojson").read_text())["features"]])
    acu_zmm = unary_union([shape(f["geometry"]) for f in json.loads((REPO / "web/data/acuiferos.geojson").read_text())["features"]
                           if f["properties"]["zmm"]])
    det = [(float(d["latitude"]), float(d["longitude"])) for d in
           csv.DictReader(open(FUENTES / "firms" / "viirs_vegetacion_2016_2025_zonas_agua.csv"))]
    sina = [(float(f["properties"]["x"]), float(f["properties"]["y"])) for f in
            json.loads((FUENTES / "sina" / "incendios_nl.json").read_text())["features"]
            if any(b in (f["properties"]["tipoveget"] or "").encode("latin-1", "ignore").decode("utf-8", "ignore").lower()
                   for b in BOSQUE) or any(b in (f["properties"]["tipoveget"] or "").lower() for b in BOSQUE)]
    salida = []
    for z in zonas:
        t = tabla_sierra(z, cat)
        g = t["malla"]
        dets = np.zeros(g["n"] ** 2, int)
        if det:
            i, j, ok = indice(g, [d[0] for d in det], [d[1] for d in det])
            np.add.at(dets, (i * g["n"] + j)[ok], 1)
        filas = []
        for f, nd in zip(t["cuadrantes"], dets):
            cerca_sina = any(math.hypot((a - f["lat"]) * 111_000, (b - f["lon"]) * 111_000 * math.cos(math.radians(a))) <= 1500
                             for a, b in sina)
            f.update(detecciones=int(nd), fuego=bool(nd > 0 or cerca_sina))
            filas.append(f)
        sano = [f["ndvi"] for f in filas if f["ndvi"] is not None and (f["arbol"] or 0) >= 0.5 and not f["fuego"]]
        ref = float(np.percentile(sano, 90)) if len(sano) >= 5 else float(np.nanpercentile(
            [f["ndvi"] for f in filas if f["ndvi"] is not None], 90))
        candidatos = []
        for f in filas:
            if f["ndvi"] is None or f["pendiente"] is None or not f["fuego"] or f["pendiente"] > 35:
                continue
            if (f["arbol"] or 0) + (f["matorral"] or 0) < 0.3:
                continue
            pt = Point(f["lon"], f["lat"])
            if not (cuencas.contains(pt) or acu_zmm.contains(pt)):
                continue
            rec = f["ndvi"] / ref if ref > 0 else 1
            perdido = min(1, max(0, 1 - rec) / 0.5)
            acceso = 0 if f["camino_m"] is None else min(1, max(0, 1 - (f["camino_m"] - 500) / 2500))
            suave = min(1, max(0, 1 - (f["pendiente"] - 15) / 20))
            f.update(recuperacion=rec, score=0.5 * perdido + 0.3 * acceso + 0.2 * suave)
            candidatos.append(f)
        elegidos = lista_corta(candidatos, SIERRA["por_zona"], SIERRA["separacion_m"])
        print(f"  {z['id']}: {len(candidatos)} cuadrantes candidatos, bosque vecino NDVI {ref:.2f}, elegidos {len(elegidos)}")
        for k, f in enumerate(elegidos, 1):
            cerca = mas_cercano(t["lugares"], f["lat"], f["lon"], 4000)
            lugar = f"cerca de {cerca[0]}" if cerca else z["nombre"].split("·")[-1].strip().replace("una ladera quemada ", "")
            razones = [f"Verdor {f['ndvi']:.2f} contra {ref:.2f} del bosque vecino sin fuego: "
                       f"{100 * min(f['recuperacion'], 1):.0f} % recuperado",
                       (f"{plural(f['detecciones'], 'detección', 'detecciones')} de fuego por satélite entre 2016 y 2025" if f["detecciones"]
                        else "Registro de incendio en bosque de CONAGUA a menos de 1.5 km"),
                       f"Pendiente media {f['pendiente']:.0f}°",
                       (f"A {f['camino_m']:.0f} m del camino o brecha más cercana" if f["camino_m"] is not None
                        else "Sin camino registrado en OpenStreetMap a menos de 2.5 km")]
            salida.append(dict(type="Feature", geometry=poligono(g, f["i"], f["j"]), properties=dict(
                id=f"{z['id']}-C{k}", zona_id=z["id"], objetivo="agua", rank=k, score=round(100 * f["score"], 1),
                nombre=f"Cuadrante {k} · {lugar}", municipio=z["municipio"], area_ha=round(SIERRA["lado_m"] ** 2 / 10_000, 2),
                centro=[round(f["lat"], 5), round(f["lon"], 5)], razones=razones,
                metricas=dict(ndvi=f["ndvi"], ndvi_bosque_vecino=round(ref, 3),
                              recuperacion_pct=round(100 * min(f["recuperacion"], 1)), pendiente_grados=f["pendiente"],
                              distancia_camino_m=f["camino_m"], detecciones=f["detecciones"],
                              copa_pct=round(100 * (f["arbol"] or 0))))))
    return salida


# ---------------- ciudad ----------------
def tabla_ciudad(z, cat):
    archivo = CACHE / f"{z['id']}.json"
    if archivo.exists():
        return json.loads(archivo.read_text())
    la, lo = z["centro"]
    g = malla(la, lo, CIUDAD["lado_m"], CIUDAD["ventana_m"])
    print(f"  {z['id']}: calor, verdor, construido y escuelas…")
    nd = ndvi(cat, g)
    tc = temperatura(cat, g)
    cob = cobertura(cat, g, [50])
    osm = overpass(z["id"], g["bounds"], 'nwr["amenity"~"^(school|kindergarten|hospital|clinic)$"]({bbox})')
    pts = []
    for el in osm["elements"]:
        if el["type"] == "node":
            pts.append((el["lat"], el["lon"]))
        elif el.get("bounds"):
            b = el["bounds"]
            pts.append(((b["minlat"] + b["maxlat"]) / 2, (b["minlon"] + b["maxlon"]) / 2))
    esc = np.zeros(g["n"] ** 2, int)
    if pts:
        i, j, ok = indice(g, [p[0] for p in pts], [p[1] for p in pts])
        np.add.at(esc, (i * g["n"] + j)[ok], 1)
    filas = []
    for k in range(g["n"] ** 2):
        i, j = divmod(k, g["n"])
        cla, clo = centro_celda(g, i, j)
        filas.append(dict(i=i, j=j, lat=cla, lon=clo, ndvi=r(nd[k], 3), temp=r(tc[k], 1),
                          construido=r(cob[50][k], 3), escuelas=int(esc[k])))
    tabla = dict(zona=z["id"], malla=g, cuadrantes=filas, nombres={})
    archivo.write_text(json.dumps(tabla))
    return tabla


def zonas_industriales(z, g):
    """Polígonos de uso industrial de OpenStreetMap: ahí no vive gente, aunque haga calor."""
    from shapely.geometry import Polygon
    osm = overpass(f"{z['id']}_industrial", g["bounds"], 'way["landuse"="industrial"]({bbox})')
    return [Polygon([(p["lon"], p["lat"]) for p in el["geometry"]]) for el in osm["elements"]
            if el["type"] == "way" and len(el.get("geometry", [])) >= 4]


def ciudad(zonas, cat):
    from shapely.geometry import Point
    salida = []
    for z in zonas:
        t = tabla_ciudad(z, cat)
        g = t["malla"]
        industria = zonas_industriales(z, g)
        urb = [f for f in t["cuadrantes"] if (f["construido"] or 0) >= 0.4 and f["ndvi"] is not None and f["temp"] is not None
               and not any(poly.contains(Point(f["lon"], f["lat"])) for poly in industria)]
        if not urb:
            continue
        calor = norm([f["temp"] for f in urb])
        sin_veg = 1 - norm([f["ndvi"] for f in urb])
        gente = 0.5 * norm([f["construido"] for f in urb]) + 0.5 * norm([f["escuelas"] for f in urb])
        for f, a, b, c in zip(urb, calor, sin_veg, gente):
            f["score"] = 0.35 * a + 0.35 * b + 0.30 * c
        elegidos = lista_corta(urb, CIUDAD["por_zona"], CIUDAD["separacion_m"])
        cambio = False
        for k, f in enumerate(elegidos, 1):
            clave = f"{f['i']},{f['j']}"
            if clave not in t["nombres"]:
                t["nombres"][clave] = nominatim(f["lat"], f["lon"])
                cambio = True
            if not t["nombres"][clave][0] and clave + "z14" not in t["nombres"]:
                t["nombres"][clave + "z14"] = nominatim(f["lat"], f["lon"], zoom=14)   # barrio o sector, más amplio
                cambio = True
            colonia, municipio = t["nombres"][clave]
            colonia = colonia or (t["nombres"].get(clave + "z14") or [None])[0]
            municipio = MUNICIPIOS.get(municipio, municipio)
            municipio = municipio or z["municipio"]
            nombre = colonia or f"Cuadrante {k} de {municipio}"
            temp_med = float(np.nanmedian([u["temp"] for u in urb]))
            razones = [f"Superficie a {f['temp']:.0f} °C en verano de 2026 ({f['temp'] - temp_med:+.1f} °C contra la mediana urbana de la zona)",
                       f"Verdor {f['ndvi']:.2f}: casi sin vegetación" if f["ndvi"] < 0.2 else f"Verdor {f['ndvi']:.2f}",
                       f"{100 * f['construido']:.0f} % construido",
                       (f"{plural(f['escuelas'], 'escuela, guardería o clínica', 'escuelas, guarderías o clínicas')} en el cuadrante" if f["escuelas"]
                        else "Sin escuelas ni clínicas registradas en el cuadrante")]
            salida.append(dict(type="Feature", geometry=poligono(g, f["i"], f["j"]), properties=dict(
                id=f"{z['id']}-C{k}", zona_id=z["id"], objetivo="aire", rank=k, score=round(100 * f["score"], 1),
                nombre=nombre, municipio=municipio, area_ha=round(CIUDAD["lado_m"] ** 2 / 10_000, 1),
                centro=[round(f["lat"], 5), round(f["lon"], 5)], razones=razones,
                metricas=dict(temp_superficie_c=f["temp"], ndvi=f["ndvi"], construido_pct=round(100 * f["construido"]),
                              escuelas_clinicas=f["escuelas"]))))
        if cambio:
            (CACHE / f"{z['id']}.json").write_text(json.dumps(t))
        print(f"  {z['id']}: {len(urb)} cuadrantes urbanos fuera de zona industrial ({len(industria)} polígonos industriales), elegidos {len(elegidos)}")
    return salida


def main():
    import sys
    zonas = [f["properties"] for f in json.loads((REPO / "web/data/zonas.geojson").read_text())["features"]]
    falta = any(not (CACHE / f"{z['id']}.json").exists() for z in zonas if "estación" in " ".join(z["razones"]) or z["objetivo"] == "agua")
    cat = _cliente() if falta else None
    partes = sys.argv[1:] or ["sierra", "ciudad"]
    feats = []
    if "sierra" in partes:
        print("Sierra")
        feats += sierra([z for z in zonas if z["objetivo"] == "agua"], cat)
    if "ciudad" in partes:
        print("Ciudad")
        feats += ciudad([z for z in zonas if z["objetivo"] == "aire" and "estación" in z["nombre"]], cat)
    previo = json.loads(SALIDA.read_text())["features"] if SALIDA.exists() else []
    hechos = {f["properties"]["objetivo"] for f in feats}
    feats = [f for f in previo if f["properties"]["objetivo"] not in hechos] + feats
    SALIDA.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, ensure_ascii=False, separators=(",", ":")))
    print(f"→ web/data/cuadrantes.geojson: {len(feats)} cuadrantes")


if __name__ == "__main__":
    main()
