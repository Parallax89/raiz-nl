# Pipeline

Escribe `web/data/` siguiendo el contrato del README raíz.

```bash
pip install requests shapely pyshp pystac-client planetary-computer rasterio numpy
python pipeline/sinaica.py     # 12 meses de PM10 y PM2.5 por estación (≈5 min; guarda en investigacion/fuentes/sinaica/)
python pipeline/build.py       # zonas, incendios, cuencas, presas, estaciones, acuíferos, colonias, indicadores y resumen
python pipeline/cuadrantes.py  # cuadrantes de plantación dentro de cada zona (con caché: segundos)
cd backend && python -m app.seed --reset   # para que la API tome las zonas nuevas
```

Todo lo necesario para reconstruir `web/data/` sin internet ya está en `investigacion/fuentes/` (capas de CONAGUA en `sina/`, cuenca de La Boca en `hydrobasins/`, verdor ya medido en `sentinel2/`, promedios y serie mensual de PM en `sinaica/`). Si falta algo, lo descarga a `pipeline/raw/` (ignorado por git): capas de CONAGUA SINA (el GeoServer pide un
`User-Agent` de navegador), HydroBASINS nivel 12 y las escenas de Sentinel-2 que se consultan. Usa lo que ya está en
`investigacion/fuentes/`: incendios de CONAGUA 2005-2023, detecciones VIIRS 2024-2025 (`firms/`), presas, índice
urbano de MIDE Monterrey y promedios de SINAICA (`sinaica/`).

## Reglas

**Agua (8 zonas, celdas de ~2 km).**
- Sólo cuentan incendios en **bosque** (pino, encino, oyamel, táscate): en matorral y pastizal no se reforesta con
  árboles. Las celdas que sólo tienen detección satelital deben estar arriba de 1,000 m (franja de bosque).
- Fuego: hectáreas de CONAGUA con peso que se reduce a la mitad cada 5 años (60 %) y detecciones satelitales
  2024-2025 (40 %), en escala logarítmica. +10 % si además está sobre un acuífero sin disponibilidad.
- Destino del agua: cuenca de **La Boca** (trazada con HydroBASINS nivel 12), cuencas oficiales del DOF
  «Río San Juan 1» (hasta **El Cuchillo**) y «Río Pablillo 1 y 2» (hasta **Cerro Prieto**), o un acuífero que
  surte a la zona metropolitana. Sin ninguno, fuera.
- Fuera también: pendiente media mayor a 35°, valle metropolitano debajo de 800 m y cualquier sitio debajo de 500 m.
- **Regeneración** (verdor NDVI de Sentinel-2 en la temporada seca de 2026, mediana de hasta 3 escenas con menos de
  15 % de nubes): 0.55 o más, la prioridad baja a la mitad (probablemente se regenera sola); menos de 0.35, sube 25 %
  (suelo descubierto). Los cortes son supuestos de trabajo.
- Zonas separadas al menos 8 km. Lo que no entra y por qué: `docs/sitios_descartados.md`.

**Aire (8 zonas).**
- 5 municipios del reto 3 (Juárez, Santa Catarina, Cadereyta, García, Pesquería) alrededor de su estación del SIMA,
  ordenados por PM10 y PM2.5 medidos en 12 meses (SINAICA, datos crudos).
- 3 colonias de Monterrey con más PM2.5 estimado, menos copa arbórea, más calor y más gente (MIDE Monterrey 2022;
  35 / 30 / 20 / 15 %). Su puntaje es de otra escala: se listan después de los municipios medidos.

**Cuadrantes de plantación (`pipeline/cuadrantes.py` → `web/data/cuadrantes.geojson`).**
- Sierra: cuadrantes de 250 m (6.25 ha) en una ventana de 5 km alrededor de cada zona de agua. Entran si hubo fuego
  (detección satelital 2016-2025 o incendio en bosque de CONAGUA a menos de 1.5 km), si hay bosque o matorral
  (ESA WorldCover), pendiente media de 35° o menos (Copernicus DEM 30 m) y si drenan a una presa o recargan un
  acuífero de la zona metropolitana. Orden: 50 % verdor perdido contra el bosque vecino sin fuego (NDVI de
  Sentinel-2, temporada seca 2026), 30 % acceso (distancia a camino o brecha, OpenStreetMap), 20 % pendiente.
  4 por zona, separados al menos 500 m.
- Ciudad: cuadrantes de 500 m a menos de 3 km de cada estación del SIMA de los municipios del reto 3, urbanos (40 %
  o más construido) y fuera de zonas industriales. Orden: 35 % calor de superficie (Landsat, verano 2026), 35 % falta
  de vegetación, 30 % gente (construido y escuelas, guarderías, hospitales y clínicas). 3 por estación, separados
  al menos 1 km; nombre de colonia por OpenStreetMap.
- Hallazgo: el bosque vecino sin fuego marca NDVI de 0.31 a 0.49 en temporada seca, así que el corte de 0.55 que
  usa `build.py` para «se regenera sola» es alto para esta sierra.

## Limitaciones conocidas

- La subcuenca de nivel 12 que contiene la cortina de La Boca (159 km²) incluye algo de terreno aguas abajo de la
  presa: un sitio justo al norte de la cortina podría marcarse como «aporta a La Boca» cuando aporta directo a
  El Cuchillo (que de todos modos recibe ambos).
- Cada incendio de CONAGUA es un punto (su registro), no el polígono de la cicatriz: el verdor se mide en la celda
  de 2 km donde cae ese punto. El polígono real requiere severidad de quema con imágenes de antes y después.
- SINAICA entrega datos crudos (no validados). La estación SURESTE (Guadalupe) no está en la consulta.
- PM2.5 por colonia sólo existe para el municipio de Monterrey (MIDE); para los demás municipios se usa la estación.
- Cuadrantes: no se conoce la tenencia de la tierra; dos cuadrantes urbanos sin nombre de colonia (Juárez C1 y el C3
  de la estación de Pesquería, que cae en Apodaca) pueden ser zona industrial no mapeada: revisar antes de plantar.
