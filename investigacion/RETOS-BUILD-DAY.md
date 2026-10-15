# Grok Monterrey Build Day · 14-oct-2026 — retos ambientales (Pronatura Noreste)

Fuente: deck de Antonio Hernández Ramírez (Pronatura Noreste), `fuentes/build-day/retos-ambientales-v2.pdf`,
bajado de https://retos-ambientales-build-day.aileenvl375305.chatgpt.site/. Catálogo general de datos:
`reports/Datos abiertos Nuevo León hackatón.md`.

Marcas: [V] verificado hoy desde el box · [C] conocimiento previo, probar.

## Reto 1 · Infiltración — ¿dónde restaurar suelos en partes altas?

Entregable sugerido: índice de prioridad alta/media/baja (humedad, vegetación, pendiente, suelo, incendios) o
cartera de obras (barreras de piedra / material vegetal). El índice es potencial relativo, no volumen infiltrado.

| Capa | Fuente | Estado |
|---|---|---|
| Código base de infiltración | GEE de Pronatura: code.earthengine.google.com/caf8eb767fa5c6a7fbbd73aab7dd2b85 | Requiere abrirlo con cuenta Google; desde el box no se ve el código |
| Distritos de riego | SharePoint de Pronatura | **Pide login de Pronatura** — pedírselo a los organizadores |
| Pendiente | Copernicus DEM GLO-30 (`COPERNICUS/DEM/GLO30`) o INEGI CEM | [C] |
| Vegetación | Sentinel-2 NDVI, Dynamic World; USV CONAGUA `Sina:m32_usv` | [V] capa SINA existe |
| Incendios | CONAGUA `Sina:m32_incendiosforhist`; FIRMS; MODIS `MODIS/061/MCD64A1` | [V] capa SINA existe, [C] resto |
| Suelo | INEGI Edafología Serie II; SoilGrids / grupos hidrológicos HYSOGs250m (GEE community) | [C] |
| Humedad | SMAP (`NASA/SMAP/...`, ~9 km), ERA5-Land | [C] |
| Cuencas | `Sina:m00_cuencas`, `Sina:m05_cuencas_disponibilidad`; HydroBASINS | [V] capas SINA existen |
| ANP | `Sina:m32_vwanp` (Cumbres, Cerro de la Silla) | [V] capa SINA existe |
| Lluvia | CHIRPS diario | [V] descarga |
| Contexto | Declaratoria de sequía 2022 (`fuentes/build-day/declaratoria-sequia-2022.pdf`); análisis HCNL 2023 | [V] bajado |

Cuencas que importan: Río San Juan arriba de El Cuchillo, Río Pablillo (Cerro Prieto), Río Ramos (La Boca).

## Reto 2 · El Cuchillo — ¿qué cambia aguas abajo cuando se libera agua?

Opción A: cronología (fecha, volumen, ruta, destino, motivo). Opción B: NDWI/MNDWI + NDVI/EVI antes/después en DR 026
y Texas. Coincidir en el tiempo no es causalidad (lluvia, ciclo agrícola, otras presas).

| Capa | Fuente | Estado |
|---|---|---|
| Almacenamiento diario El Cuchillo, Marte R. Gómez, Falcón, La Amistad, Cerro Prieto, La Boca | API CONAGUA `PresasPG/presas/reporte/AAAA-MM-DD`; claves `CCHNL`, `MRGTP`, `CILAFLCMX`, `CILAAMSMX`, `CPRNL`, `LBCNL` | [V] — serie 2020→23-abr-2025 en `fuentes/build-day/presas_san_juan_bravo_2020_2025.csv` |
| Firma de liberación | Caída en CCHNL + subida en MRGTP en los mismos días = trasvase | [V] Trasvase 2022 visible: del 22-nov al 15-dic-2022 El Cuchillo bajó 755.5→555.1 Mm³ (−200.4, justo lo acordado) y Marte R. Gómez subió 387.6→595.6 (+208). Desde ene-2023 Marte R. Gómez baja (595.6→451.1 al 22-feb) = consumo del DR 026. Otras ventanas con la misma firma: ene-2020, ene-2021, jun–sep-2024 (Alberto: lluvia, no necesariamente liberación) |
| Liberación dic-2025 | Fuera de la API (congelada abr-2025): SADM niveles + notas diarias MVS; La Jornada 22-dic-2025; SRE 12-dic-2025 | [V] SADM vivo |
| Estadística agrícola por distrito | `Sina:m07_agricoladrnumcultivos` (sembrada, cosechada, producción, valor por DR y año agrícola) | [V] |
| Agua y cultivos | Sentinel-2 (`COPERNICUS/S2_SR_HARMONIZED` + Cloud Score+) MNDWI/NDVI; Sentinel-1 si hay nubes | [C] |
| Lado Texas | USDA CropScape (CDL anual), Water Data for Texas (Falcón/Amistad), IBWC contabilidad del Tratado de 1944 | [C] |

## Reto 3 · Aire de la ZMM — ¿subió o bajó la contaminación en esta administración?

SO₂, NO₂ y CO de Sentinel-5P, ≥3 km alrededor de cada estación SIMA, ~5 años desde el inicio de la
administración (4-oct-2021) y línea base para comparar el año restante. S5P = columna, no concentración en suelo.

| Capa | Fuente | Estado |
|---|---|---|
| Estaciones SIMA (14, con coordenadas) | Extraídas del mapa oficial → `fuentes/build-day/sima_estaciones.csv` | [V] |
| Script listo para pegar en GEE | `fuentes/build-day/reto3_s5p_sima.js` (mensual 2018-07→2026-09, CSV estación × contaminante × mes) | Sintaxis OK, **no ejecutado** |
| Bandas S5P | `tropospheric_NO2_column_number_density`, `SO2_column_number_density`, `CO_column_number_density` | [V] catálogo GEE |
| Validación en suelo | SINAICA vía `rsinaica` (15 estaciones horarias); JSON vivo `aire.nl.gob.mx/SIMA2017reportes/api_conc.php` | [V] |

Trampas: un buffer de 3 km es menor que el píxel nativo de S5P (~5.5×3.5 km; CO ~7 km), así que estaciones vecinas
comparten píxeles. SO₂ es ruidoso fuera de la refinería de Cadereyta (SURESTE 3). NO₂ tiene estacionalidad fuerte:
comparar mismos meses año contra año, no promedios crudos. 2020 trae el bajón COVID (antes de la administración).
Controlar viento/lluvia con ERA5-Land.
