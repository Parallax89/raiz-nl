# Pipeline

Baja fuentes abiertas y escribe `web/data/` siguiendo el contrato del README raíz.

Pendiente (v0 de hoy):

1. `fetch.py`: descarga incendios, cuencas, acuíferos, ANP y presas del GeoServer SINA de CONAGUA (endpoints en
   `docs/FUENTES.md`) y los guarda en `pipeline/raw/` (ignorado por git).
2. `build.py`: arma la malla de celdas de ~2 km, calcula `score` de agua y aire, y escribe `zonas.geojson`,
   `incendios.geojson`, `presas.geojson`, `estaciones.geojson`, `cuencas.geojson` y `resumen.json`.

`sima_estaciones.csv` trae las 14 estaciones del SIMA con coordenadas.
