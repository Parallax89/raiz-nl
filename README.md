# Raíz NL

**Dona un árbol donde más rinde: para el agua o para el aire de Monterrey.**

Grok Monterrey Build Day · 14-oct-2026 · combina los retos 1 (infiltración / reforestación en la sierra) y
3 (calidad del aire en la ZMM) de Pronatura Noreste.

## Qué hace

1. El ciudadano elige para qué quiere su árbol: **💧 Agua** o **🌬️ Aire**.
2. Un mapa le muestra las **zonas priorizadas** para ese objetivo, con el porqué de cada una.
   - **Agua:** cicatrices de incendio en la sierra que drenan hacia las presas (El Cuchillo, Cerro Prieto, La Boca)
     o que recargan acuíferos en déficit, fuera de zona urbana.
   - **Aire:** zonas de la ZMM donde la gente respira peor (Pesquería, Cadereyta, Juárez, Santa Catarina, García…)
     y hay poca cobertura vegetal o suelo desnudo que levanta polvo.
3. Escoge una zona y dona (en el MVP es un compromiso, sin pagos).
4. Ve el texto exacto de la publicación (por ejemplo, *"Donaron un árbol para restaurar Los Cuartones, cuenca que
   aporta a El Cuchillo."*), decide si se etiqueta y da su visto bueno. Con la API, la cuenta del proyecto lo
   publica; sin API, lo publica desde su propia cuenta. Nunca se promete "mejorar el suministro de agua": el árbol no
   mete litros a la presa (ver [docs/Contexto_Arbol.md](docs/Contexto_Arbol.md)).

La evaluación de la idea, las correcciones y el plan de trabajo están en **[docs/PLAN.md](docs/PLAN.md)**. El API de donaciones (zonas con cupo, textos canónicos, bot de X) está en **[backend/](backend/README.md)** y su plan en **[docs/BACKEND.md](docs/BACKEND.md)**.

## Estructura

```
web/        Portal estático (Leaflet, sin build). Lee web/data/*.geojson; si no existen usa web/data/mock/.
pipeline/   Scripts que bajan fuentes abiertas y calculan las zonas → escriben web/data/.
gee/        Scripts de Google Earth Engine (Sentinel-5P por estación SIMA; infiltración/NDVI pendiente).
docs/       Plan, contrato de datos y fuentes.
```

## Correr local

```bash
python3 -m http.server 8000 --directory web
# abrir http://localhost:8000 (portal) y http://localhost:8000/mapa.html (mapa e indicadores)
```

## Contrato de datos (lo que el pipeline escribe y el portal/dashboard lee)

| Archivo | Geometría | Propiedades |
|---|---|---|
| `web/data/zonas.geojson` | Polygon (celdas ~2 km) | `id` (`AG-01`/`AI-01`), `objetivo` (`agua`/`aire`), `rank`, `score` 0–100, `nombre`, `municipio`, `razones` [texto], `metricas` {num}, `centro` [lat, lon] |
| `web/data/incendios.geojson` | Point | `anio`, `fecha`, `municipio`, `ha`, `tipoveget` |
| `web/data/presas.geojson` | Point | `clavesih`, `nombre`, `almacenamiento_mm3`, `llenado_pct`, `fecha` |
| `web/data/estaciones.geojson` | Point | `estacion`, `municipio`, `pm10`, `pm25`, `periodo` |
| `web/data/cuencas.geojson` | Polygon | `cuenca`, `presa_destino` |
| `web/data/acuiferos.geojson` | Polygon | `clave`, `nombre`, `situacion` (Con/Sin Disponibilidad), `deficit_hm3`, `disponible_hm3`, `zmm`, `publicacion` |
| `web/data/colonias_mty.geojson` | Polygon | `nombre`, `pm25`, `copa_pct`, `isla_calor_c`, `poblacion` (sólo municipio de Monterrey, MIDE 2022) |
| `web/data/indicadores.json` | — | Conteos para `web/mapa.html`: incendios por fuente y vegetación, acuíferos, aire, presas, zonas |
| `web/data/resumen.json` | — | `generado`, `incendios_total`, `ha_quemadas_total`, `periodo_incendios`, `zonas_agua`, `zonas_aire`, `fuentes` [{`nombre`, `url`, `fecha`}] |

Si el dashboard de otro integrante consume estos mismos archivos, todo queda conectado.

## Fuentes (verificadas el 14-oct-2026)

Detalle y endpoints en [docs/FUENTES.md](docs/FUENTES.md).

## Cómo subir cambios

Sin PRs ni revisiones: `git pull`, cambias, `git commit`, `git push` a `main`. Cada push a `main` se publica solo en
producción (GitHub Pages, workflow `.github/workflows/deploy.yml`) en 1–2 minutos.

