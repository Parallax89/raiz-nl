# Plan · Raíz NL

## 1. ¿La idea es pertinente?

**Sí, y es de las pocas que conecta dos retos con una sola acción ciudadana.** Lo que la hace fuerte:

- **Une agua y aire con datos reales.** Hay registros públicos de incendios, cuencas, acuíferos en déficit, presas
  y estaciones de aire (ver [FUENTES.md](FUENTES.md)).
- **Le da a la gente una forma concreta de participar.** No es solo un mapa para expertos.
- **Encaja con el evento.** Es un build day de Grok/X, y publicar en X es parte natural del flujo.
- **Llena un hueco que el gobierno deja abierto.** El estado dice que plantó un millón de árboles, pero no publica
  dónde. Raíz NL muestra dónde y por qué.

## 2. Qué hay que corregir (para que el jurado no la tumbe)

| # | Riesgo en la idea original | Corrección |
|---|---|---|
| 1 | "Reforestar mejora la calidad del aire de la ciudad" | Un árbol no limpia el aire de toda la ZMM. El PM10 de Monterrey viene de pedreras, industria, refinería, tráfico y **suelo desnudo**. Prometemos menos **exposición local**: cubrir suelo desnudo (menos polvo), barreras verdes junto a vialidades y zonas industriales, y sombra donde la gente respira peor (escuelas, paradas). |
| 2 | Especies | Sólo nativas y de bajas emisiones de COV (las de mucho isopreno, como el eucalipto, empeoran el ozono). Pronatura define la paleta: encino, mezquite, ébano, anacahuita, palo blanco… |
| 3 | "Reforestar cicatrices de incendio" | Después de un incendio, a veces conviene más la regeneración natural más **obras de suelo** (barreras de piedra o de material vegetal muerto), que es justo lo que propone el reto 1 y que infiltra desde el primer día. Se dona "árbol" **u** "obra de suelo". |
| 4 | El ciudadano escoge el punto exacto | Escoge una **zona priorizada**. La organización ejecutora asigna el sitio exacto, porque en la sierra hay pendiente, acceso, tenencia de la tierra y permisos. |
| 5 | Máscara "donde no se construye" | Hay que excluir zona urbana, cuerpos de agua, agricultura activa y predios sin permiso. En las ANP (Cumbres, Cerro de la Silla) se coordina con CONANP y con Parques y Vida Silvestre. |
| 6 | Confianza | Cada donación pasa por estos estados: **comprometida → plantada → viva al año**. Se verifica con foto geolocalizada y NDVI satelital ("tu árbol visto desde el espacio"). Sin trazabilidad, los portales de donación mueren. |
| 7 | Publicar en X | MVP: **web intent**, es decir, el ciudadano publica desde su cuenta y se etiqueta sólo si quiere. Después, una cuenta oficial publicaría por API, pero eso implica costo de API, consentimiento y moderación. Nunca se publica un nombre sin opt-in. |
| 8 | Dinero | El MVP no tiene pagos. En producción el dinero lo recibe una **donataria autorizada** (p. ej. Pronatura), que emite recibos deducibles; nosotros no tocamos dinero. |
| 9 | Promesa de impacto | El índice es **potencial relativo** (así lo advierte el reto 1): no prometemos m³ infiltrados ni µg/m³ reducidos. |

## 3. Cómo se prioriza (v0 de hoy → v1)

**Agua (reto 1).** Celdas de ~2 km, fuera de zona urbana.

- **v0:**
  - incendios forestales en NL de 2005 a 2023 (registro de CONAGUA/CONAFOR, 666 registros), ponderados por hectáreas y antigüedad;
  - si la celda drena a una presa que abastece a la ZMM;
  - si está sobre un acuífero en déficit (13 de 23 en NL).
- **v1:** agregar pendiente (DEM), NDVI en época seca, área quemada satelital (MODIS MCD64A1 / FIRMS), suelo y
  el código de infiltración de Pronatura en Earth Engine.

**Aire (reto 3).** Celdas de ~2 km en la ZMM y su periferia.

- **v0:** contaminación de la estación SIMA más cercana (PM10/PM2.5) por la distancia, en las zonas que se señalaron
  (Pesquería, Cadereyta, Juárez, Santa Catarina, García).
- **v1:** NO₂/SO₂/CO de Sentinel-5P por estación (`gee/reto3_s5p_sima.js`), histórico de SINAICA, vegetación y suelo
  desnudo (NDVI), población del Censo 2020 por AGEB, escuelas y paradas.

## 4. Plan de trabajo

### Hoy (build day)

| Bloque | Responsable | Entregable |
|---|---|---|
| Portal | front | `web/` con flujo completo sobre datos de ejemplo: elegir objetivo, mapa, zona, donar, publicar en X |
| Datos agua | datos 1 | `pipeline/` → `zonas.geojson` (agua), `incendios.geojson`, `cuencas.geojson`, `presas.geojson` |
| Datos aire | datos 2 | `zonas.geojson` (aire), `estaciones.geojson`; correr `gee/reto3_s5p_sima.js` si da tiempo |
| Dashboard | integrante del dashboard | Consumir el mismo contrato de datos (README) |
| Pitch | pitch | 3 min: problema (2022 + aire), qué hace, demo en vivo, publicar en X, qué sigue |

### Demo (guion de 60 s)

1. "¿Para qué quieres tu árbol?" → **Agua**.
2. El mapa enciende las cicatrices de incendio que drenan a El Cuchillo. Se abre la zona #1 con sus razones.
3. Donar → **Publicar en X** en vivo.
4. Cambiar a **Aire** → Pesquería y Cadereyta.
5. Cerrar con el dashboard: incendios, hectáreas y donaciones por objetivo.

### Después del hackatón

1. Alianza con Pronatura Noreste (ejecutora y donataria) y con Parques y Vida Silvestre NL.
2. Pipeline v1 con Earth Engine y SINAICA.
3. Backend de donaciones con estados y fotos, y verificación con NDVI a 12 meses.
4. Cuenta oficial en X con publicación automática (con opt-in).
