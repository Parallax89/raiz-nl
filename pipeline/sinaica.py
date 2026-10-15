"""Promedios de 12 meses de PM10 y PM2.5 por estación del SIMA, desde SINAICA (INECC).

SINAICA no tiene API documentada: se llama igual que su página de datos
(POST a /pags/datGrafs.php, datos crudos, un mes por consulta). Guarda la respuesta
cruda en pipeline/raw/sinaica/ y el resumen en investigacion/fuentes/sinaica/.

Uso: python pipeline/sinaica.py
"""
import csv
import json
import re
import statistics
import time
from datetime import date, timedelta
from pathlib import Path

import requests

REPO = Path(__file__).resolve().parents[1]
RAW = REPO / "pipeline" / "raw" / "sinaica"
RAW.mkdir(parents=True, exist_ok=True)
SALIDA = REPO / "investigacion" / "fuentes" / "sinaica" / "pm_estaciones_12m.csv"
UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36 Chrome/126 Safari/537.36",
      "Referer": "https://sinaica.inecc.gob.mx/data.php"}
# id de SINAICA → nombre de la estación en pipeline/sima_estaciones.csv
ESTACIONES = {139: "SUROESTE", 140: "NOROESTE", 141: "CENTRO", 142: "NORESTE", 144: "NORTE", 145: "NOROESTE 2",
              146: "NORESTE 2", 147: "SURESTE 2", 148: "SUROESTE 2", 424: "SURESTE 3", 425: "NORTE 2", 426: "SUR",
              446: "ESTE"}
PARAMETROS = {"PM10": "PM10", "PM2.5": "PM2.5"}


def mes(estacion, param, inicio):
    archivo = RAW / f"{estacion}_{param}_{inicio}.json"
    if archivo.exists():
        return json.loads(archivo.read_text())
    r = requests.post("https://sinaica.inecc.gob.mx/pags/datGrafs.php", headers=UA, timeout=60,
                      data=dict(estacionId=estacion, param=param, fechaIni=inicio, rango=4, tipoDatos="A", datoBase=0))
    r.raise_for_status()
    m = re.search(r"var dat = (\[.*?\]);", r.text, re.S)
    datos = json.loads(m.group(1)) if m else []
    archivo.write_text(json.dumps(datos))
    time.sleep(0.3)
    return datos


def main():
    hoy = date.today()
    inicios = [(hoy - timedelta(days=30 * k)).isoformat() for k in range(12, 0, -1)]
    filas = []
    for est, nombre in ESTACIONES.items():
        fila = dict(sinaica_id=est, estacion=nombre, desde=inicios[0], hasta=hoy.isoformat())
        for clave, param in PARAMETROS.items():
            vals = [d["valor"] for i in inicios for d in mes(est, param, i)
                    if isinstance(d.get("valor"), (int, float)) and d["valor"] >= 0]
            fila[f"{clave.lower().replace('.', '')}_media"] = round(statistics.mean(vals), 1) if vals else None
            fila[f"{clave.lower().replace('.', '')}_horas"] = len(vals)
        filas.append(fila)
        print(f"  {nombre:11s} PM10 {fila['pm10_media']} ({fila['pm10_horas']} h) · PM2.5 {fila['pm25_media']} ({fila['pm25_horas']} h)")
    with open(SALIDA, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0]))
        w.writeheader()
        w.writerows(filas)
    print(f"→ {SALIDA.relative_to(REPO)}")


if __name__ == "__main__":
    main()
