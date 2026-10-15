# Fuentes de datos

Verificadas en vivo el 14-oct-2026 salvo donde se indica. Todas son públicas y no necesitan llave.

## Agua / reto 1

| Dato | Endpoint | Notas |
|---|---|---|
| Incendios forestales históricos (NL: 666 registros, 2005–2023) | `https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&version=2.0.0&request=GetFeature&outputFormat=application/json&typeNames=Sina:m32_incendiosforhist&CQL_FILTER=entidad LIKE 'Nuevo Le%'` | Geometría en EPSG:3857. **Ojo:** el campo `x` trae la latitud y `y` la longitud. Superficie en `totalha`. Los textos vienen con doble codificación UTF-8 (`JesÃºs`). |
| Cuencas | `typeNames=Sina:m00_cuencas` (757 cuencas) y `Sina:m05_cuencas_disponibilidad` (disponibilidad DOF 2023) | MultiPolygon |
| Acuíferos y disponibilidad | `typeNames=Sina:m06_acuiferos_disponibilidad`, `CQL_FILTER=clvacuifero LIKE '19%'` | 13 de 23 acuíferos de NL en déficit |
| Áreas naturales protegidas | `typeNames=Sina:m32_vwanp` | Cumbres de Monterrey, Cerro de la Silla… |
| Uso de suelo y vegetación | `typeNames=Sina:m32_usv` | Para la máscara urbana / agrícola |
| Presas (catálogo) | `typeNames=Sina:m09_presasprincipales` | |
| Almacenamiento diario de presas (1995 → 23-abr-2025) | `https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/AAAA-MM-DD` | Claves `CCHNL` (El Cuchillo), `CPRNL` (Cerro Prieto), `LBCNL` (La Boca), `MRGTP` (Marte R. Gómez). La API dejó de actualizarse en abr-2025. |
| Niveles de presas hoy | `https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles` | HTML (scraping) |
| Código base de infiltración (Pronatura) | `https://code.earthengine.google.com/caf8eb767fa5c6a7fbbd73aab7dd2b85` | Se abre con cuenta de Google |
| Distritos de riego (Pronatura) | SharePoint de Pronatura | Pide login: hay que pedirlo a los organizadores |

## Aire / reto 3

| Dato | Endpoint | Notas |
|---|---|---|
| Estaciones SIMA (14, con coordenadas) | `pipeline/sima_estaciones.csv` | Sacadas del mapa oficial `aire.nl.gob.mx/airemapbing/airebing_icars_alt.php` |
| SIMA en vivo | `https://aire.nl.gob.mx/SIMA2017reportes/api_conc.php` (también `api_indice.php`, `api_meteo.php`) | JSON sin documentar; por defecto devuelve una estación |
| Histórico horario por estación | SINAICA (`sinaica.inecc.gob.mx`), paquete R `rsinaica` | IDs: 139 Santa Catarina, 140 San Bernabé, 141 Obispado, 142 San Nicolás, 144 Escobedo, 145 García, 146 Apodaca, 147 Juárez, 148 San Pedro, 424 Cadereyta, 425 UANL, 426 Pueblo Serena, 446 Pesquería, 479 Misión San Juan |
| Sentinel-5P NO₂/SO₂/CO | `gee/reto3_s5p_sima.js` (Earth Engine) | Columna atmosférica, no concentración en suelo. **Script sin probar.** |
| Calor, PM2.5, NO₂ y copa arbórea por colonia (sólo municipio de Monterrey) | `https://mide.monterrey.gob.mx/geoserver/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=geonode:uesi_mty2022&outputFormat=application/json` | 1,141 colonias |
| Escuelas, paradas, choques (Monterrey) | MIDE: `geonode:escuelas_monterrey_sep`, `geonode:paradas_transporte`, `geonode:incidentes_viales` | |

## Contexto

- Retos del build day: deck de Pronatura Noreste ("Retos ambientales para construir con IA").
- Reporte completo de datos abiertos de NL: está en el workspace del equipo y se puede compartir aparte.
