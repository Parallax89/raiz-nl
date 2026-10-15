# Water in Monterrey / Nuevo León: open data inventory, context and data-crossing opportunities (as of 14-Oct-2026)

Method note: every endpoint marked "tested 2026-10-14" was called directly from a Linux server on that date (curl / WFS GetFeature), and the response was inspected. Figures marked "own aggregation" were computed by me from the raw public data. They are not official totals. Everything else comes from the linked web sources.

## 1. Master inventory: which datasets exist, and what are their URL, format, resolution, update frequency and access method?

### Takeaway
Four sources do most of the work. (1) CONAGUA's SINA GeoServer WFS is an undocumented but public bulk API. It serves REPDA concession points with holder names, aquifer availability, piezometry, RENAMECA water quality, treatment plants and more as GeoJSON. (2) The daily reservoir-levels HTML page of Agua y Drenaje (SADM). (3) SMN files: daily station data and the municipal drought-monitor Excel. (4) The four small SADM CSVs on the Nuevo León open-data portal (CKAN API). The CONAGUA daily reservoir JSON API covers 1995 to 23-Apr-2025 and then stops. 2025-2026 reservoir data therefore has to be scraped from SADM or news.

### Cited Findings

| # | Dataset | URL / access | Format | Spatial res. | Temporal coverage / update | Notes |
|---|---|---|---|---|---|---|
| 1 | SADM "Niveles de Presas" | [sadm.gob.mx niveles](https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles) | HTML (scrape) | 3 reservoirs (La Boca, Cerro Prieto, El Cuchillo) | Daily. Page showed "Fuente: Dirección de Operaciones, 12 de octubre de 2026" when tested 2026-10-14 | Volume (Mm³) and NAMO per dam, system total 925.539 of 1,458.1 Mm³. Presa Libertad not listed |
| 2 | CONAGUA SINA daily reservoir monitoring ("Monitoreo de las principales presas") | Viewer: [sinav30…/Presas/](https://sinav30.conagua.gob.mx:8080/Presas/). JSON: `https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/YYYY-MM-DD`. Last date: `https://sinav30.conagua.gob.mx:8080/SINA45/fechaMonitoreo/ultimo` | JSON (no auth) | 210 national dams, point lat/lon | Tested 2026-10-14: returns data for 1995-01-01, 2007-01-01, 2024-10-13 and 2025-04-20. Returns `[]` for every date from 2025-04-25 on. `fechaMonitoreo/ultimo` = 2025-04-23 | Fields: clavesih, nombreoficial, estado, municipio, lat, lon, uso, NAME/NAMO elevation & storage, elevacionactual, almacenaactual, llenano. NL keys: CCHNL, CPRNL, LBCNL, PSANL (Salinillas) |
| 3 | CONAGUA SINA GeoServer (bulk geodata) | WFS: `https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities` (also WMS/KML). Add `outputFormat=application/json&CQL_FILTER=…` | GeoJSON / GML / KML | Points & polygons | Varies by layer (see sections 3-8) | Tested 2026-10-14. ~150 layers, including m01 REPDA aprovechamientos, m02 RENAMECA, m06 aquifers/piezometry, m09 dams, m12 stations, m16 precipitation, m28 coverage, m29 WWTPs, m30 potabilizadoras, m31 drought, m46 flood-protection works, m48/m50 marginación/rezago |
| 4 | SIH (Sistema de Información Hidrológica) | [sih.conagua.gob.mx](https://sih.conagua.gob.mx/). Page lists public FTPs `ftp://presas:presas@…`, `ftp://hidros:hidros@…`, `ftp://climas:climas@sih.conagua.gob.mx`, plus `docs/Catalogo_Estaciones.xlsx`, `docs/precdia.asc` | FTP files, XLSX, KMZ | Station | Historical | FTP connections **timed out** from our server on 2026-10-14 (unverified). A Kaggle dataset was built from this FTP: [Kaggle conagua-presas](https://www.kaggle.com/datasets/edehoyos/conagua-presas/data) (storage, elevation, area, evaporation, precipitation) |
| 5 | SMN daily climatological station data | e.g. [dia19052.txt Monterrey (OBS)](https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/nl/dia19052.txt). Pattern `/Diarios/nl/dia{clave}.txt` | TXT (TSV) | Station | 1951-01-01 to 2026-10-09. File "Emisión 09/10/2026" | Columns: PRECIP, EVAP, TMAX, TMIN. Station 19052 "MONTERREY (OBS)", San Nicolás, OMM 76393, "OPERANDO" |
| 6 | Monitor de Sequía de México, municipal series | [MunicipiosSequia.xlsx](https://smn.conagua.gob.mx/tools/RESOURCES/Monitor%20de%20Sequia%20en%20Mexico/MunicipiosSequia.xlsx). Landing: [SMN MSM](https://smn.conagua.gob.mx/es/climatologia/monitor-de-sequia/monitor-de-sequia-en-mexico) | XLSX (2.1 MB) | Municipality (2,478 rows) | Columns from 2003-01-31 to 2026-09-30, currently biweekly | Category D0–D4 per municipality per date. Monterrey (19039) last value = D0 |
| 7 | SADM datasets on NL open-data portal | [catalogodatos.nl.gob.mx/organization/servicios-agua-y-drenaje](https://catalogodatos.nl.gob.mx/organization/servicios-agua-y-drenaje). CKAN API `…/api/3/action/package_search?fq=organization:servicios-agua-y-drenaje` | CSV + data dictionary | AMM aggregate / municipality | Metadata modified 2025-11-07. Monthly series Sep-2024 to Aug-2025 | 4 datasets: uso-de-agua, agua-reutilizada, fuentes-de-agua, infraestructura-de-agua (details in section 2) |
| 8 | REPDA single-title lookup | [app.conagua.gob.mx/ConsultaRepda.aspx](https://app.conagua.gob.mx/ConsultaRepda.aspx). Program page: [gob.mx REPDA](https://www.gob.mx/conagua/acciones-y-programas/registro-publico-de-derechos-de-agua-repda-55190) | Web form | Title | Live | One title or holder at a time. For bulk, use WFS layers m01 (section 4) |
| 9 | CONAGUA dam inventory (SISP) | [presas.conagua.gob.mx/inventario/](https://presas.conagua.gob.mx/inventario/) | Web app | Dam | — | Responds 200. Did not explore further |
| 10 | CONAGUA hydrological forecast | [app.conagua.gob.mx/spr/](https://app.conagua.gob.mx/spr/) | Web app | Basin (OC Río Bravo: Bajo/Medio/Alto Bravo, etc.) | — | "Pronóstico hidrológico" by basin |
| 11 | INEGI Censo 2020, AGEB/manzana for NL | [ageb_mza_urbana_19_cpv2020_csv.zip](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_19_cpv2020_csv.zip) (12.0 MB, tested 200). [Censo 2020](https://www.inegi.org.mx/programas/ccpv/2020/) | CSV | Block/AGEB | 2020 | Contains household water-availability variables (see section 9) |
| 12 | INEGI Censo Nacional de Gobiernos Municipales 2023 | [cngmd/2023](https://www.inegi.org.mx/programas/cngmd/2023/) | CSV/XLSX | Municipality | 2023 | Has a water/sanitation services module (see Gaps) |
| 13 | CHIRPS rainfall | [data.chc.ucsb.edu/products/CHIRPS-2.0](https://data.chc.ucsb.edu/products/CHIRPS-2.0/) | GeoTIFF/NetCDF | ~5 km | Daily, 1981–present | URL tested 200 |
| 14 | ERA5-Land | [CDS ERA5-Land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land) | NetCDF/GRIB (free account) | ~9 km | Hourly, 1950–present | URL tested 200 |
| 15 | JRC Global Surface Water | [global-surface-water.appspot.com](https://global-surface-water.appspot.com/). GEE: [JRC/GSW1_4](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater) | Raster / GEE | 30 m | 1984–2021 (v1.4) | URLs tested 200 |
| 16 | WRI Aqueduct 4.0 | [wri.org Aqueduct 4.0 data](https://www.wri.org/data/aqueduct-global-maps-40-data) | Shapefile/GDB/CSV | Sub-basin | Baseline + projections | URL tested 200 |
| 17 | HydroLAKES / DAHITI (altimetry) | [HydroLAKES](https://www.hydrosheds.org/products/hydrolakes), [DAHITI](https://dahiti.dgfi.tum.de/en/) | Shapefile / time series | Lake | — | URLs tested 200. Did not check whether DAHITI has El Cuchillo or Cerro Prieto |
| 18 | Instituto del Agua NL: transparency-request log | [catalogodatos.nl.gob.mx solicitudes IANL](https://catalogodatos.nl.gob.mx/dataset/7945215e-9b80-4078-9f22-ff1a5414cee8/resource/d5f4eb9b-89ce-4313-befd-06699eb8cc4b/download/2021-2025_solicitudes_ianl.csv) | CSV | — | 2021–2025, 301 requests | Metadata only (folio, dates, status). No request text and no answers |
| 19 | SADM PFiles (indicators, tariffs, board minutes, financials) | [pfiles.sadm.gob.mx/PFiles/indicadores](https://pfiles.sadm.gob.mx/PFiles/indicadores), [/tarifas](https://pfiles.sadm.gob.mx/PFiles/tarifas), [/actasdesesiones](https://pfiles.sadm.gob.mx/PFiles/actasdesesiones) | PDF only | — | Mixed | The indicator pages hold ~480 PDF links across 11 sections (idseccion 1–30). The page template says "Ultima Actualizacion 15-11-2018", but some documents are newer, e.g. [Doc 2912 cites "Agosto 2026"](https://pfiles.sadm.gob.mx/Pfiles/Uploads/Documentos/2912.pdf) |

- The SINA home page describes the dam module as daily volume for 210 dams with history since 2007. — [SINA](https://sinav30.conagua.gob.mx:8080/) (as summarized in search). Direct API tests show records back to at least 1995-01-01 (tested 2026-10-14).
- Existing open-source template: `raulastrga/sinagua` is a Sinaloa reservoir dashboard. It uses Node.js and Playwright to scrape CONAGUA, with daily-status, time-series and map views. — [GitHub sinagua](https://github.com/raulastrga/sinagua)

### Inferences
- The SINA PresasPG JSON stopped on 2025-04-23, but media still cite a CONAGUA "informe diario" in Oct-2026. CONAGUA probably still produces the daily report and the public API simply stopped being fed. A team needs a hybrid series: SINA API 1995 to Apr-2025, then a daily scraper of the SADM niveles page from now on. The gap from Apr-2025 to now can be backfilled from MVS/Milenio daily news articles.
- The SINA WFS is the single most valuable find. One GET per layer returns statewide GeoJSON with holder names and coordinates. Bulk REPDA, which many people assume needs transparency requests, is effectively available this way.

### Gaps
- Could not verify the SIH FTP contents because connections timed out from our network. Try from another network.
- Found no official documentation, terms of use or rate limits for the SINA WFS or PresasPG API. Both sit behind Incapsula. Plain GETs worked, but `/rest/fechamaxpresas` returned an Incapsula challenge page.

## 2. What does Servicios de Agua y Drenaje de Monterrey (SADM / AyD) publish: reservoir data, consumption by sector or colonia, tariffs, tomas, tandeos, leaks, infrastructure maps?

### Takeaway
SADM publishes very little machine-readable data. It offers (a) a daily HTML reservoir page, (b) four small aggregate CSVs on the state portal (per-capita consumption, non-revenue water, reuse volumes, source counts, trunk-main km), and (c) PDFs for indicators and tariffs. Nothing at colonia or sector-hidrométrico level is published. There are no network, tank or well maps, no leak logs and no structured outage data. Outage and tandeo information exists only as press releases, social media and news.

### Cited Findings
- **Open data (4 CSVs, CKAN, modified 2025-11-07):** fuentes de agua por municipio, uso de agua, agua reutilizada, infraestructura. — [NL catalog: SADM](https://catalogodatos.nl.gob.mx/organization/servicios-agua-y-drenaje)
- **uso_agua (monthly, Sep-2024 to Aug-2025, AMM aggregate):**
  - Billed consumption ranges 98.24 to 119.76 L/hab/día. Formula: (Volumen Facturado×1000)/(365×Habitantes).
  - "disponibilidad_agua" (total hydraulic capacity) is constant at 26.1.
  - **Agua no contabilizada ranges 41.11% to 48.25%.** Formula: (producido − facturado)/producido × 100, "Área Metropolitana y Zona Conurbada".
  - Source: [2024_2025_uso_agua.csv](https://catalogodatos.nl.gob.mx/dataset/ac8539c7-0c4b-4845-a53c-58f46c90cf7c/resource/81bed7a2-ed69-4ad6-93cb-d7e244084df1/download/2024_2025_uso_agua.csv) and its [dictionary](https://catalogodatos.nl.gob.mx/dataset/ac8539c7-0c4b-4845-a53c-58f46c90cf7c/resource/b4ed7b81-dd89-4566-b6ad-a5491e5fc314/download/diccionario_uso_agua.csv)
- **agua_reutilizada (m³/month):** treated water contracted for reuse is 5.25 to 5.92 million m³ per month. Treated water billed for reuse is 3.80 to 4.40 million m³ per month (Sep-2024 to Aug-2025). — [agua_reutilizada.csv](https://catalogodatos.nl.gob.mx/dataset/2f7dcf16-be70-4ce7-a92e-b9c3f4850016/resource/97f3b61c-8050-4a0b-9ee6-3033f82d0e1d/download/agua_reutilizada.csv)
- **fuentes_agua 2025:** 30 municipalities. Totals: 394 pozos, 26 presa entries, 7 galerías filtrantes, 6 manantiales, 3 ríos. Monterrey alone has 55 pozos and 2 presa entries. — [2025_fuentes_agua.csv](https://catalogodatos.nl.gob.mx/dataset/17ef0ad5-dc1a-4f22-83b9-66cf6845be93/resource/f93cda62-eae4-4aaf-9a44-f54afabb50b7/download/2025_fuentes_agua.csv)
- **infraestructura_agua 2025:** 20 rows of trunk infrastructure (alimentador/acueducto/anillo) from 12" to 100". Own aggregation: 3,144.8 km in total, including 1,505 km of 12" mains. Materials include asbesto-cemento. There is no geometry. — [2025_infraestructura_agua.csv](https://catalogodatos.nl.gob.mx/dataset/3a92b539-2135-4dd6-b8ac-9168da34a700/resource/5c9150ca-95a2-4dd6-a007-1ab07e1f5f5c/download/2025_infraestructura_agua.csv)
- **Daily reservoir page.** As of the 12-Oct-2026 reading:
  - La Boca 34.249 Mm³ (NAMO 35.0)
  - Cerro Prieto 244.474 Mm³ (NAMO 295.0)
  - El Cuchillo 646.816 Mm³ (NAMO 1,123.0)
  - Total 925.539 / 1,458.1 Mm³
  - The same page states supply is "Superficiales 60% / Subterráneas 40%". It also lists infrastructure history: the 70 km Anillo de Transferencia (1984), the 133 km Linares–Monterrey aqueduct from Cerro Prieto, and the 110 km El Cuchillo aqueduct (1993).
  - Source: [SADM Niveles de Presas](https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles)
- SADM's NAMO values differ from CONAGUA's: Cerro Prieto 295 vs 300 Mm³, La Boca 35.0 vs 36.78 Mm³. Media percentages use the CONAGUA denominators. — [SADM niveles](https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles) vs [SINA API 2024-10-13](https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/2024-10-13)
- **Sector split.** According to SADM data as summarized in the Plan Hídrico NL 2050, residential is 70% of water supplied, public supply 19%, and industry & commerce 11%. — [CONL: Plan Hídrico 2050](https://www.conl.mx/noticias/49) (via search summary; base year not verified)
- **Per-capita consumption by municipality** (Jan–Apr 2022 vs Jan–Apr 2023) was released as a state press bulletin, not as data. — [nl.gob.mx boletín](https://www.nl.gob.mx/es/boletines/ayd-presenta-cifras-de-consumo-diario-de-agua-por-habitante-en-nl)
- **Indicators and tariffs** exist only as PDFs on PFiles: 11 indicator sections and a tariff page with PDF links. — [PFiles indicadores](https://pfiles.sadm.gob.mx/PFiles/indicadores), [PFiles tarifas](https://pfiles.sadm.gob.mx/PFiles/tarifas)
- The SADM home page links to the PNT consulta pública, the state transparency portal, the Plan Maestro del Agua, and the Tec book "Agua para Monterrey, Ed. 2021". — [sadm.gob.mx](https://www.sadm.gob.mx/), [PNT consulta pública](https://consultapublicamx.plataformadetransparencia.org.mx/vut-web/faces/view/consultaPublica.xhtml#inicio), [transparencia.nl.gob.mx](https://transparencia.nl.gob.mx/site/bienvenida), [Plan Maestro del Agua](https://historico.nl.gob.mx/planmaestro-agua), [Libro Agua para Monterrey 2021 (Tec)](https://repositorio.tec.mx/handle/11285/642843)
- SADM says its Plan Maestro del Agua (presented May 2022, horizon 2050) is its guiding plan. A financing package had been "detenido" for three years. — [SADM Prensa](https://www.sadm.gob.mx/SADM/Prensa.jsp)
- **Water quality.** SADM states compliance monitoring under NOM-179-SSA1-2020 and NOM-127-SSA1-2021 but publishes no results. — [SADM Calidad del Agua](https://www.sadm.gob.mx/SADM/index.jsp?id_html=calidad)
- **Tandeos / outages in 2026** are known only through news:
  - Jul-2026: AyD and García agreed tandeos for 19 priority colonias, splitting García into two supply polygons. Director Eduardo Ortegón Williamson said about 290 colonias are affected. — [Enfoque Monterrey 7-Jul-2026](https://enfoquemonterrey.com.mx/2026/07/07/agua-y-drenaje-y-garcia-acuerdan-tandeos-para-asegurar-suministro-de-agua/)
  - 29-Apr-2026: a 48-inch main repair left Monterrey colonias without water for more than a day. — [Milenio 29-Apr-2026](https://www.milenio.com/comunidad/cortes-agua-monterrey-a-que-hora-restablecen-servicio-29-abril-2026)
- The CDMX open-data portal publishes bimonthly consumption at block level. This is a template format for what could be requested from SADM. — [datos.cdmx.gob.mx consumo-agua](https://datos.cdmx.gob.mx/dataset/consumo-agua)
- On concessions, one academic article says the data "no se cuenta con información de acceso público, se tiene que realizar solicitudes". — [Redalyc: Industrialización del agua y producción de cerveza en Monterrey](https://www.redalyc.org/journal/4217/421770657011/html/). This is partially contradicted by the SINA WFS REPDA layers (section 4).

### Inferences
- Non-revenue water of about 41–48% is a headline number for a hackathon. Nearly half of produced water is unbilled, from physical leaks plus commercial losses. Combined with the asbesto-cemento share of trunk mains, it supports a leak or renewal-prioritization project.
- Total hydraulic capacity of 26.1 is almost certainly m³/s (26,100 L/s). The dictionary says "capacidad hidráulica" without units, so verify before use.
- Colonia-level consumption, tomas by type, tariff revenue by sector and outage logs would need a PNT request to SADM. A hackathon team can draft and file one, but answers take about 10–20 business days.

### Gaps
- Did not find any past PNT request to SADM that released colonia-, sector- or toma-level data.
- Did not open SADM's SIPOT (Art. 70 LGTAIP) formats to see which tables are uploaded.
- No current number of tomas (connections) by type, no tariff table in machine-readable form, and no public leak/fuga log were found.
- The current total supply rate (L/s) for 2026 was not found in an official source.

## 3. Reservoirs (El Cuchillo, Cerro Prieto, La Boca, Presa Libertad/León): where do daily and historical levels come from, and is there an API?

### Takeaway
Historical daily storage for El Cuchillo, Cerro Prieto and La Boca can be pulled as JSON from CONAGUA SINA for 1995 to 23-Apr-2025. Current daily values come from SADM's niveles page or from daily news articles that quote CONAGUA's internal report. Presa Libertad/León is absent from every daily feed found.

### Cited Findings
- **API.** `GET https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/{YYYY-MM-DD}` returns all 210 principal dams for that date (≈121 KB JSON). Discovered from the viewer's JS: `urlApi="https://sinav30.conagua.gob.mx:8080/PresasPG"` and `rootApi=".../SINA45/"`. Other endpoints in the JS: `SINA45/PresasG/porPeriodoRHA/{period}/{rha}` and `SINA45/fechaMonitoreo/ultimo`. — [SINA Presas viewer](https://sinav30.conagua.gob.mx:8080/Presas/) (tested 2026-10-14)
- The latest date the API reports is 2025-04-23. Requests for 2025-04-25 through 2026-10-14 return empty arrays. — [SINA45 fechaMonitoreo/ultimo](https://sinav30.conagua.gob.mx:8080/SINA45/fechaMonitoreo/ultimo) (tested 2026-10-14)
- **Snapshot 2024-10-13 (after TS Alberto):** El Cuchillo 1,096.19 Mm³ (97.6% of NAMO 1,123.143), Cerro Prieto 334.063 Mm³ (111.4% of NAMO 300.0), La Boca 37.184 Mm³ (101.1% of NAMO 36.78). — [SINA API 2024-10-13](https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/2024-10-13)
- **Latest figures (CONAGUA daily report, cut 06:00 on 13-Oct-2026):**

  | Dam | % full | Storage | Extraction / notes |
  |---|---|---|---|
  | El Cuchillo | 57.66% | 647.627 Mm³ (+0.811 in 24 h) | 7.056 m³/s total: 4.234 to Cuchillo I–Monterrey, 2.685 to Cuchillo II–Monterrey, 0.137 to Acueducto China–Aldama–Arcabuz |
  | Cerro Prieto | 81.49% | 244.474 Mm³ | 3.906 m³/s |
  | La Boca | 93.36% | 34.337 Mm³ | 0.282 m³/s |
  | Total | — | 926.438 Mm³ | — |

  Source: [MVS 14-Oct-2026](https://mvsnoticias.com/nuevo-leon/2026/10/14/nivel-de-las-presas-en-nuevo-leon-hoy-miercoles-14-de-octubre-del-2026-749708.html)
- MVS runs a daily series "Nivel de las presas en Nuevo León HOY", which works as a scrapable proxy for the 2025–2026 gap. — e.g. [MVS 10-Oct-2026](https://mvsnoticias.com/nuevo-leon/2026/10/10/nivel-de-las-presas-en-nuevo-leon-hoy-sabado-10-de-octubre-del-2026-749300.html), [MVS 2-Oct-2026](https://mvsnoticias.com/nuevo-leon/2026/10/2/nivel-de-las-presas-en-nuevo-leon-hoy-viernes-2-de-octubre-del-2026-748296.html)
- El Cuchillo went from 51.30% (1-Oct-2026) to 52.89% (3-Oct-2026) with early-October rains. — [Milenio](https://www.milenio.com/comunidad/nivel-presas-nuevo-leon-aumento-lluvias-primer-frente-frio-2026)
- Static dam attributes for the 210 dams (NAME/NAMO, curtain height, first year of operation) are in WFS layer `Sina:m09_presasprincipales`. — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)
- The CONAGUA national principal-dam report has also been described as biweekly ("quincenal"), e.g. 40 of 210 dams below 50% in Jan-2026. — [UnoTV](https://www.unotv.com/nacional/presas-en-riesgo-conagua-reporta-niveles-criticos-en-40-embalses-del-pais/)
- Tamaulipas publishes weekly PDFs of storage in its main dams (source CONAGUA). They are useful for the shared Río Bravo / San Juan basin context. — [Tamaulipas 14-May-2026 PDF](https://www.tamaulipas.gob.mx/recursoshidraulicos/wp-content/uploads/sites/24/2026/05/almacenamiento-presas-y-embalses-14-05-2026.pdf)
- **Presa Libertad (renamed "Presa León" by the state):**
  - Design figures: NAME 307 Mm³, NAMO 221 Mm³, planned 1,600 L/s. — [ANEAS](https://www.aneas.com.mx/presa-libertad-seguridad-hidrica-nuevo-leon/)
  - Hydraulic closure was in July 2023. — [El Financiero 27-Jul-2023](https://www.elfinanciero.com.mx/monterrey/2023/07/27/inicia-operacion-presa-la-libertad-para-captar-agua/)
  - 6-Feb-2026: CONAGUA said it holds 35–40% of ordinary capacity, is "sin grietas ni fugas", and is ready for entrega-recepción, but no date had been set. It cited up to 4,000 L/s in emergencies and a cost of 5,600 mdp (+42% over budget, split 50/50 federal/state). — [88.9 Noticias](https://889noticias.mx/noticias/conagua-confirma-que-la-presa-leon-esta-lista-para-su-entrega/)
  - SADM gave a total cost of 7,895 mdp "incluyendo todas las partidas". It said water reaches the city via the Cerro Prieto aqueduct. The governor cited 27% filling at the time. — [SADM Prensa](https://www.sadm.gob.mx/SADM/Prensa.jsp)
  - Apr-2026: CONAGUA and the state held the first technical verification tour for entrega-recepción. Modifications were agreed, and the first filling was defined as an evaluation phase. — [MVS 24-Apr-2026](https://mvsnoticias.com/nuevo-leon/2026/4/24/revisan-presa-libertad-acuerdan-cambios-antes-de-su-entrega-730336.html)
  - Presa Libertad/León does not appear on SADM's niveles page, in the 13-Oct-2026 CONAGUA daily figures reported by MVS, or among the 210 dams in SINA. — [SADM niveles](https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles), [MVS 14-Oct-2026](https://mvsnoticias.com/nuevo-leon/2026/10/14/nivel-de-las-presas-en-nuevo-leon-hoy-miercoles-14-de-octubre-del-2026-749708.html)

### Inferences
- Nothing official publishes Presa Libertad's current storage, so satellite water-area time series (section 6) could fill that gap for the public.
- The extraction breakdown in the daily report (m³/s per aqueduct) lets a team track how much El Cuchillo II is actually used: 2.685 m³/s on 13-Oct-2026 against a 5 m³/s nominal capacity.

### Gaps
- Could not find where CONAGUA's daily NL report is published now (PDF, social media or an internal mailing to media). An OCRB (Organismo de Cuenca Río Bravo) channel is likely but unverified.
- No public reservoir elevation–area–volume curves were found for El Cuchillo, Cerro Prieto or Libertad. SINA gives only NAME/NAMO elevation and storage points.

## 4. Aquifers: availability (DOF), piezometric data and wells for AMM, Campo Buenos Aires, Campo Mina, etc.

### Takeaway
The official 2023 availability figures (DOF 9-Nov-2023, cut 30-Dec-2022) for all 23 NL aquifers can be downloaded as GeoJSON from SINA, along with piezometric well readings for 2000–2022. 13 of the 23 aquifers have negative availability, totalling about −381 hm³/yr. Four are formally SOBREEXPLOTADO, including the two well fields that supply most of Monterrey's groundwater: Campo Buenos Aires and Campo Mina.

### Cited Findings
- WFS layer `Sina:m06_acuiferos_disponibilidad` with filter `clvacuifero LIKE '19%' AND anio=2023` returns 23 NL aquifers with fechapub 2023-11-09 and fechacorte 2022-12-30. Fields: R (recharge), DNC, VCAS (concessioned), VEAS (extraction), DMA, situación, condición. Earlier vintages are included too (e.g. the 2018 publication with cut 2015). — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities) (tested 2026-10-14)
- Key 2023 values (hm³/yr):

  | Aquifer | R | DNC | VCAS | VEAS | DMA | Condición |
  |---|---|---|---|---|---|---|
  | Área Metropolitana de Monterrey (1906) | 143.7 | 45.8 | 100.77 | 110.29 | −12.39 | — |
  | Campo Buenos Aires (1907) | 57.0 | — | 62.83 | — | −5.91 | SOBREEXPLOTADO |
  | Campo Mina (1908) | 24.0 | — | 30.76 | — | −7.07 | SOBREEXPLOTADO |
  | Cañón del Huajuco (1911) | 26.8 | — | 28.69 | — | −2.19 | — |
  | Citrícola Sur | — | — | — | — | −88.86 | — |
  | Sabinas-Parás | — | — | — | — | −74.10 | — |
  | Navidad-Potosí-Raíces | — | — | — | — | −69.67 | — |
  | Citrícola Norte | — | — | — | — | −57.52 | — |
  | El Carmen-Salinas-Victoria | — | — | — | — | −39.17 | — |

  The other SOBREEXPLOTADO aquifers are Agualeguas-Ramones and Campo Cerritos. Own aggregation: 13 negative aquifers sum to −381.1 hm³. — same WFS layer
- This matches press reporting: 13 of 23 aquifers negative, a combined deficit of 381 Mm³, and 4 overexploited (Campo Cerritos, Campo Mina, Campo Buenos Aires, Agualeguas-Ramones). The same article reports:
  - Metro potable groundwater is 169 Mm³/yr: 28 Mm³ (17%) from the city aquifer and 141 Mm³ (>80%) from Campo Mina, Campo Buenos Aires and the Cañón del Huajuco tunnels.
  - Post-2022 wells are drilled 700–2,000 m deep at 18–30 million pesos each.
  - High-capacity recharge areas have shrunk 20% in 23 years, with 1,050 km² of urban sprawl.
  - REPDA shows 269 concessions granted in Galeana on closed aquifers from 2015 to 2026.

  Source: [MVS 28-Sep-2026](https://mvsnoticias.com/nuevo-leon/2026/9/28/los-acuiferos-que-sostienen-a-monterrey-operan-en-numeros-rojos-747715.html)
- Historical comparison: the 2009-era DOF availability agreement (REPDA cut 30-Sep-2008) listed deficits of 62.64 hm³ (AMM), 5.72 (Campo Buenos Aires) and 6.66 (Campo Mina). — [DOF nota 5200110](https://dof.gob.mx/nota_detalle_popup.php?codigo=5200110)
- **Piezometry:** `Sina:m06_vwpiezometria` filtered `clveestado='19'` returns 3,540 NL records for 2000–2022. Fields: numpozo, lat/lon, elevbrocal, elevestati, profnivest (static water depth). Records by aquifer: AMM 258, Campo Mina 88, Campo Buenos Aires 77, Cañón del Huajuco 127, Citrícola Norte 774, Citrícola Sur 678. — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities) (tested 2026-10-14)
- **SADM well concessions by aquifer** (REPDA cut 2023, own aggregation from `m01_vwaprovsbm`), in hm³/yr: Campo Buenos Aires 62.7, AMM 27.7, Cañón del Huajuco 27.1, Campo Mina 26.5, Citrícola Norte 7.6, Campo Topo Chico 2.8. SADM surface concessions total 405.9 hm³/yr. — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)
- A recharge-loss study (2023) by the Foro Permanente de Aguas Binacionales with Tec de Monterrey and Texas A&M found urban and agricultural expansion reducing Monterrey recharge zones. — [Binational Waters](https://www.binationalwaters.org/alerta-hidrica-en-monterrey-la-expansion-urbana-y-agricola-reducen-zonas-de-recarga-acuifera/)

### Inferences
- For the AMM aquifer, VEAS (110.29) exceeds VCAS (100.77) in the 2023 figures. That implies extraction outside registered concessions.
- SADM's Campo Buenos Aires concessions (62.7 hm³) alone use about 110% of that aquifer's total recharge (57 hm³). The well-field dependency is structural.
- Piezometry stops in 2022 and is sparse (≈10–30 wells per aquifer per year). That suits trend maps but not monitoring of post-2022 emergency wells.

### Gaps
- No well-by-well SADM extraction data (actual volumes, depths, locations of the 2022 emergency wells) was found as open data. This would need a PNT request to SADM or CONAGUA.
- Did not retrieve the DOF 9-Nov-2023 PDF itself. The WFS reproduces it, so check a few values against the DOF before publishing.

## 5. REPDA concessions for Nuevo León: how to download them in bulk, which fields exist, and what analyses compare industrial/brewery/bottler concessions with domestic supply?

### Takeaway
Bulk REPDA "aprovechamientos" for NL can be downloaded from the SINA WFS: 51,642 groundwater plus 1,369 surface records across four annual snapshots (REPDA cuts 2020–2023), with titular, título, uso, volume, municipality, aquifer, SCIAN sector and point geometry. In REPDA, industrial concessions are small next to agriculture and SADM's own public-urban titles. The 2022 public controversy relied on journalistic and academic REPDA analyses that mostly predate this data.

### Cited Findings
- **Layers:**
  - `Sina:m01_vwaprovsbm` (subterráneo): 1,555,175 national features, 51,642 for NL (`clvedo='19'`). Fields: titulo, numapro, titular, uso, grupouso, volsb (m³/yr), gastoma, municipio, clvacuifero/acuifero, sciansector, sciansubrama, usuario (persona física / productor rural / …), corterepda, Point geometry (EPSG:3857).
  - `Sina:m01_vwaprovspm` (superficial): 1,369 NL records, volsp.
  - Aggregates: `m01_totconcesiones*`, `m01_usoagrupado*`. Zonas federales: `m01_vwaprovzfm`.
  - Source: [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities) (tested 2026-10-14; NL groundwater download ≈35 MB GeoJSON in about 6 s)
- **Own aggregation, NL, REPDA cut 2023** (13,325 aprovechamientos, 10,154 títulos, 1,910.2 hm³/yr), in hm³/yr:

  | Use | Volume |
  |---|---|
  | Agrícola | 1,108.6 |
  | Público urbano | 561.3 |
  | Múltiples | 115.3 |
  | Industrial | 74.5 |
  | Acuacultura | 26.5 |
  | Servicios | 14.4 |
  | Pecuario | 7.3 |
  | Doméstico | 0.7 |

  SADM holds 303 aprovechamientos totalling 560.3 hm³ (405.9 of it surface). Cut 2020 is almost identical (1,901.4 hm³). — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)
- **Largest non-agricultural, non-public titulares (cut 2023; own aggregation summing aprovechamientos; name variants not merged):**

  | Titular | Uso | hm³/yr |
  |---|---|---|
  | Ternium México | Industrial | 9.73 (+2.07 under an alternate spelling) |
  | Asociación de Regantes Los Higueros | Múltiples | 9.50 |
  | Cervecería Cuauhtémoc Moctezuma | Industrial | 3.92 + 2.41 = 6.33 |
  | Industria del Álcali | Industrial | 4.46 |
  | CFE C.T. San Jerónimo | Múltiples | 2.36 |
  | Alfa Subsidiarias | Industrial | 2.28 |
  | Parque Fundidora | Múltiples | 2.24 |
  | Pemex TRI | Industrial | 1.92 |
  | Bebidas Mundiales | Industrial | 1.50 |
  | Bebidas Purificadas | Industrial | 1.40 |

  Source: [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)
- **Municipal profile (cut 2023, own aggregation)**, in hm³/yr:
  - Industrial concessions exceed public-urban ones in Apodaca (11.54 industrial vs <1.9 público urbano), San Pedro (10.27 vs 1.37) and García (7.79 vs <0.1).
  - San Nicolás: agricultural 24.67, industrial 13.00.
  - Monterrey: public-urban 33.52, industrial 11.67.
  - Source: same layer
- Infobae (2022), citing REPDA: Cervecería Cuauhtémoc Moctezuma has 5 concessions totalling 6,845,600 m³/yr. This is consistent with the ~6.3 hm³ computed above. — [Infobae 5-Aug-2022](https://www.infobae.com/america/mexico/2022/08/05/agua-que-gastan-las-cerveceras-anualmente-alcanzaria-para-abastecer-por-un-ano-a-la-poblacion-de-nuevo-leon/)
- La Jornada (2021) reported activists' analysis that five bottlers concentrate extraction in NL: Bebidas Arca, Bebidas Mundiales, Casa Guajardo, Compañía Topo Chico and Grupo Embotellador Noreste. — [La Jornada 28-Apr-2021](https://www.jornada.com.mx/notas/2021/04/28/estados/activistas-reportan-excesivo-uso-de-agua-en-industrias-de-nl/)
- El Heraldo (2022), citing the UAM study "Los Millonarios del Agua", reported 39,400 million liters/yr concessioned to Coca-Cola-family firms. That is a national figure, and the "38 veces" headline comparison looks dubious. — [El Heraldo 5-Aug-2022](https://heraldodemexico.com.mx/nacional/2022/8/5/compania-refresquera-usa-38-veces-mas-agua-que-todo-nuevo-leon-428115.html)
- UNAM IIEC: "Nuevo León: 12 multinacionales y 34 personas físicas acaparan el agua". — [LET IIEC UNAM](https://let.iiec.unam.mx/node/4301)
- Industrial extraction was about 1,600 L/s in Mar-2022. — [Wikipedia: Crisis del agua en NL 2022](https://es.wikipedia.org/wiki/Crisis_del_agua_en_Nuevo_Le%C3%B3n_de_2022) (citing El Universal)
- In Jul-2022 AMLO asked brewers and bottlers to "cede" water. CONAGUA negotiated industry cessions targeting 200 → 500 L/s for the Cerro Prieto aqueduct. — [La Jornada 19-Jul-2022](https://www.jornada.com.mx/notas/2022/07/19/estados/cedan-agua-insta-amlo-a-cerveceras-y-refresqueras-en-nl/) (target figure per search summary of [Izquierda Diario](https://www.izquierdadiario.es/Gobierno-pide-agua-a-concesionarios-en-Nuevo-Leon))
- Breweries and bottlers stayed in NL despite the federal "veto" on new northern expansions. — [Expansión 25-Aug-2022](https://expansion.mx/empresas/2022/08/25/cerveceras-refresqueras-se-quedan-nuevo-leon-crisis-hidrica)
- **Quinto Elemento Lab:** found no water-concession investigation. Their Monterrey work (with The Guardian) covers industrial air emissions and toxic waste, with data obtained through transparency requests. — [QEL: emisiones Monterrey](https://quintoelab.org/project/identifican-industrias-emisiones-contaminantes-monterrey), [QEL metodología](https://quintoelab.org/project/nota-metodologica-residuos-toxicos-monterrey-reportaje)

### Inferences
- REPDA understates real industrial use in the AMM. Many plants draw from SADM's network or buy treated water for reuse (5.3–5.9 Mm³/month contracted, section 2) instead of holding their own titles. A fair "industry vs households" analysis has to combine REPDA, SADM's sector split (≈11% industry & commerce) and reuse contracts.
- Volumes are concessioned, not measured. Fields also suggest that multi-well títulos may split or repeat volume per aprovechamiento. Validate totals by título before publishing.

### Gaps
- Could not confirm whether `volsb` is per aprovechamiento or a título total repeated across its wells.
- Found no 2024–2026 NGO or journalistic re-analysis of NL REPDA. Agua para Todos, FAMM and Mexicanos contra la Corrupción were not found to have NL-specific concession datasets in this search pass.
- Did not research recent federal water-law changes that might affect REPDA publication.

## 6. Drought and climate: Monitor de Sequía, SMN stations, CHIRPS/ERA5, GRACE

### Takeaway
Drought (municipal, 2003–2026) and long daily station records (Monterrey OBS since 1951) are directly downloadable and current to Sept/Oct 2026. Gridded rainfall (CHIRPS, ERA5-Land) is easy to add. No ready-made GRACE analysis for northeast Mexico turned up.

### Cited Findings
- Monitor de Sequía municipal XLSX: 2,478 municipalities × dated columns from 2003-01-31 to 2026-09-30. Monterrey (19039) last value is D0 (abnormally dry). Earlier 2026 columns show D1 and briefly D2. — [MunicipiosSequia.xlsx](https://smn.conagua.gob.mx/tools/RESOURCES/Monitor%20de%20Sequia%20en%20Mexico/MunicipiosSequia.xlsx) (tested 2026-10-14)
- SMN station 19052 "MONTERREY (OBS)" has a daily series from 1951-01-01 to 2026-10-09 (PRECIP, EVAP, TMAX, TMIN). The same URL pattern works for other NL stations. — [dia19052.txt](https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/nl/dia19052.txt)
- The SIH provides a station catalogue (`Catalogo_Estaciones.xlsx`), daily precipitation (`precdia.asc`) and climate/hydrometric FTPs. — [SIH](https://sih.conagua.gob.mx/)
- SINA WFS climate layers include `m16_PrecipitacionAnual`, `m16_PrecipitacionNormal`, `m12_estacionesclimatologicas`, `m12_estacioneshidrometricas` (812 stations with annual flows, 2020), `m31_amenazasequia` and `m31_mayorriesgosequia`. — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)
- 3-Feb-2022: NL was declared in extreme drought. — [Wikipedia 2022 crisis](https://es.wikipedia.org/wiki/Crisis_del_agua_en_Nuevo_Le%C3%B3n_de_2022)
- Tropical Storm Alberto (Jun-2024) was described as ending the NL drought. — [El Imparcial 21-Jun-2024](https://www.elimparcial.com/mexico/2024/06/21/tormenta-tropical-alberto-termina-con-la-sequia-nuevo-leon-el-estado-mas-beneficiado/)
- CHIRPS and ERA5-Land are available (URLs tested). — [CHIRPS](https://data.chc.ucsb.edu/products/CHIRPS-2.0/), [ERA5-Land](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-land)
- WRI Aqueduct 4.0 gives baseline and projected water stress by sub-basin. — [WRI Aqueduct 4.0](https://www.wri.org/data/aqueduct-global-maps-40-data)

### Inferences
- Drought categories (D0–D4) and reservoir storage can be lag-correlated over 2003–2025 to produce a simple "days of supply" early-warning model. The 2022 low point and the 2024 Alberto refill are the two calibration events.

### Gaps
- GRACE/GRACE-FO: the JPL mascon download page returned 404 (tested 2026-10-14). No published NE-Mexico groundwater-anomaly study was found in this pass. Use NASA PO.DAAC / GRACE Tellus directly.
- Did not verify whether SMN automatic stations (EMAs) or the NL SIMA air-quality network provide sub-daily rainfall downloads for the AMM.

## 7. Satellite water: JRC Global Surface Water and Sentinel-2/Landsat reservoir area for El Cuchillo and Cerro Prieto

### Takeaway
Satellite imagery has been used to show Cerro Prieto's 2022 collapse (NASA Landsat, and a Sentinel-1 SAR methods paper). No public, maintained Sentinel-2 or Landsat surface-area time series for El Cuchillo, Cerro Prieto or Presa Libertad turned up. That is an open niche for a hackathon.

### Cited Findings
- NASA Earth Observatory (Landsat 8) compared Cerro Prieto on 20-Jul-2015 and 7-Jul-2022. It reported the reservoir at 0.5% of its 393 Mm³ capacity in Jul-2022, with water no longer pumpable. — [NASA Earth Observatory: A Reservoir Runs Dry](https://earthobservatory.nasa.gov/images/150123/a-reservoir-runs-dry)
- NASA's 393 Mm³ "capacity" differs from CONAGUA's NAMO (300 Mm³) and SADM's (295 Mm³), probably because NAME is used. — [SINA API](https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/2024-10-13), [SADM niveles](https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles)
- A global Sentinel-1 SAR surface-water mapping paper (Remote Sensing of Environment, 2026) uses the drought-induced loss at Cerro Prieto as a case study. — [ScienceDirect S0034425726000969](https://www.sciencedirect.com/science/article/pii/S0034425726000969)
- JRC GSW: 30 m monthly water history 1984–2021, also in Earth Engine. — [JRC GSW explorer](https://global-surface-water.appspot.com/), [GEE JRC/GSW1_4](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater)
- Water Diplomat (Sep-2022): El Cuchillo was the only remaining surface supply, under 50%. Groundwater supplies about 40% of Monterrey's water on average. — [Water Diplomat](https://www.waterdiplomat.org/story/2022/09/water-levels-rise-again-slowly-monterreys-supply-dams)

### Inferences
- Pairing Sentinel-2 NDWI/MNDWI area (10 m, ~5-day revisit) with the SINA daily storage series (1995–2025) gives an empirical area–volume curve per reservoir. That curve can then (a) estimate storage for the Apr-2025 to present gap if needed and (b) **estimate Presa Libertad's fill**, which no official feed reports.

### Gaps
- Did not check whether DAHITI or Hydroweb have altimetry-based level series for El Cuchillo or Cerro Prieto. Hydroweb did not respond on 2026-10-14.
- No Sentinel-2 study specific to these reservoirs was found.

## 8. Flooding and stormwater: TS Alberto 2024, Hanna 2020, Río Santa Catarina, drenaje pluvial, risk atlases

### Takeaway
Flood data is weak. The state risk atlas dates from 2012, municipal atlases exist only as PDFs, and event impacts (Alberto 2024) exist only in news. SADM documents a 167 km pluvial network but publishes no geometry.

### Cited Findings
- **Alberto, Jun-2024:**
  - At least 4 deaths in NL, including a 15-year-old who drowned in the Río La Silla in Monterrey. — [Crónica](https://www.cronica.com.mx/nacional/tormenta-tropical-alberto-deja-4-muertos-nuevo-leon.html)
  - The Río Santa Catarina overflowed, around 20 road closures in Monterrey, and controlled releases from La Boca. — [Grupo Animal](https://grupoanimal.mx/estados/nuevo-leon-suspension-actividades-alberto-presa-la-boca), [La Razón](https://www.razon.com.mx/estados/paso-tormenta-alberto-deja-inundaciones-crecida-rios-581614)
  - Rainfall of 300–372 mm in Santa Catarina, Santiago and Monterrey was attributed to CONAGUA in news summaries. Treat as unverified until checked against SMN station data.
- **SADM pluvial drainage:** since 2002 SADM built 167 km of pluvial network for 3,041,641,109 MXN. Maintenance belongs to municipalities after handover (e.g. Santa Catarina, Guadalupe, Escobedo). Since 2007 SADM is the rector for pluvial-works design under the Plan Maestro de la Red de Drenaje Pluvial. — [SADM Drenaje Pluvial](https://www.sadm.gob.mx/SADM/index.jsp?id_html=drenaje)
- **Risk atlases:**
  - The latest state atlas dates from Jul-2012. The Secretaría de Movilidad y Planeación Urbana is responsible for updating it. — [HCNL GLPAN Jul-2024](https://www.hcnl.gob.mx/glpan/2024/07/atlas-de-riesgo-en-nuevo-leon.php)
  - Municipal PDFs: [San Pedro Garza García](https://aplicativos.sanpedro.gob.mx/Transparencia/Atlas/AtlasdeRiesgo.pdf), [García 2018](https://rmgir.proyectomesoamerica.org/AtlasMunPDF/2018/19018_GARCIA_2018.pdf)
- SINA WFS has flood/hazard-relevant layers: `m46_obrasdeproteccion`, `m18_ciclonestropicales`, `m18_trayectoriasciclones`, `m13_zonasfederales`, `m26_fenomenos*`. — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)

### Inferences
- A team could rebuild an Alberto flood footprint from Sentinel-1 SAR (cloud-penetrating) for 19–21 Jun 2024 and overlay INEGI blocks and SADM pluvial works. That would be a new public layer, since no official one exists.

### Gaps
- Did not research Hanna 2020 impacts, or whether the Atlas Nacional de Riesgos has downloadable NL flood layers. Its site did not respond on 2026-10-14.
- No official count of affected colonias or homes was found for Alberto 2024.

## 9. Water quality (RENAMECA) and inequality of access

### Takeaway
RENAMECA results for NL can be downloaded from the SINA WFS (2012–2022, 154 sites) with metal, nitrate, fluoride and coliform parameters and a traffic-light semáforo. Sampling collapsed after 2019. Data on inequality of access is mostly survey and press based. The best structured base is INEGI Censo 2020 at block level, combined with SINA's municipal coverage and marginación layers.

### Cited Findings
- **RENAMECA in NL** (WFS `m02_*`, filter `estado='NUEVO LEÓN'`):
  - Subterráneos: 241 sampling events at 39 sites, mostly Cadereyta, Monterrey and Linares.
  - Lóticos (rivers): 3,657 events at 104 sites.
  - Lénticos (reservoirs): 166 events at 11 sites, including Santiago (La Boca), China (El Cuchillo) and Linares (Cerro Prieto).
  - Events per year drop from about 500–590 lótico events per year in 2013–2018 to 91–92 in 2019–2020, 1 in 2021 and 18 in 2022.
  - `m02_subterraneosAnual` (36 NL records, 2020–2022) carries alcalinidad, conductividad, SDT, fluoruros, dureza, coliformes fecales, N-NO3, As, Cd, Cr, Hg, Pb, Mn, Fe, plus a semáforo and a contaminant list.
  - Source: [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities) (tested 2026-10-14)
- **Treatment plants:**
  - Potabilizadoras (`m30`): 85 NL records (12 plants × years 2017–2023), e.g. San Roque (Juárez) at 12,000 L/s capacity. This is the plant that receives El Cuchillo II water.
  - WWTPs (`m29`): 446 NL records (≈55–57 plants/yr).
  - Source: [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)
  - El Cuchillo II's first stage fed San Roque. — [Forbes México](https://forbes.com.mx/inauguran-por-completo-acueducto-el-cuchillo-ii-en-nuevo-leon/)
- **Municipal coverage (`m28_vwmunipobconaguaentubadam`):** NL census-based coverage for 1990–2020. In 2020 coverage was Monterrey 98.99%, Guadalupe 99.68%, García 99.61% and Juárez 99.59%. Nominal coverage hides intermittency. — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)
- **Cómo Vamos NL survey** (reported Apr-2023, about the 2022 crisis): average consecutive days without water were García up to 18, Juárez 6, Monterrey 5, Santiago 3, Santa Catarina 2 and San Pedro 1 (about 24 h). 30% said the cut schedule was not respected, and at least 3 in 10 received no pipas or bottled water. — [N+ 24-Apr-2023](https://www.nmas.com.mx/monterrey/falta-de-agua-en-nuevo-leon-municipio-de-garcia-el-mas-afectado-por-desabasto/)
- In 2022 SADM's director said 20–40% of the population had water 24 h a day and attributed this to location (elevation and pressure). — [Expansión 8-Jun-2022](https://politica.expansion.mx/estados/2022/06/08/nl-le-apuesta-a-las-lluvias-entre-el-20-y-40-de-poblacion-tiene-agua-24-horas)
- On 28-Jun-2022 the schedule failed in 288 of about 3,900 AMM colonias. — [Pie de Página](https://piedepagina.mx/la-hora-cero-de-monterrey/)
- García remained the 2026 hotspot, with about 290 colonias affected and tandeos in 19. — [Enfoque Monterrey 7-Jul-2026](https://enfoquemonterrey.com.mx/2026/07/07/agua-y-drenaje-y-garcia-acuerdan-tandeos-para-asegurar-suministro-de-agua/)
- SINA also serves marginación (`m48`), IDH (`m49`) and rezago social (`m50`) layers that can be joined by municipality. — [SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)

### Inferences
- The INEGI Censo 2020 AGEB/manzana file for NL (tested, 12 MB) includes household water variables: piped water inside the home, from the public network, and tinaco/cisterna ownership. Storage-tank ownership is a strong proxy for the ability to cope with tandeos. Crossing it with colonia-level tandeo or outage reports, scraped from news or AyD social posts, and with elevation (pressure zones) gives an "inequality of resilience" map.
- RENAMECA's post-2019 sampling collapse is itself a finding: monitoring decayed exactly as the crisis approached.

### Gaps
- Exact INEGI variable names (e.g. VPH_AGUADV, VPH_TINACO, VPH_CISTER) were not re-checked against the 2020 dictionary in this pass.
- No structured, georeferenced dataset of 2022 or 2026 outages by colonia was found. ADN40 published daily "lista de colonias sin agua" articles that could be scraped, e.g. [ADN40 15-May](https://www.adn40.mx/mexico/lista-completa-colonias-sin-agua-en-monterrey-15-mayo/) (year not verified).
- SADM's tap-water quality results (NOM-127) are not published.

## 10. Context for the team: the 2022 crisis, infrastructure since (El Cuchillo II, Presa Libertad), and the situation as of October 2026

### Takeaway
- In 2022 Monterrey came close to "día cero": Cerro Prieto fell to about 0.5–2%, La Boca to about 8–9%, and there was a deficit of more than 3,000 L/s.
- El Cuchillo II has run since late 2023, with up to 5,000 L/s capacity and 2.685 m³/s in use on 13-Oct-2026.
- Presa Libertad/León (221 Mm³ NAMO) was 35–40% full in Feb-2026 and still in entrega-recepción, with no published daily level.
- As of 13-Oct-2026 the three operating dams hold 926 Mm³ (El Cuchillo 57.7%, Cerro Prieto 81.5%, La Boca 93.4%).
- The groundwater side is structurally in deficit.
- Next-phase projects: the Pánuco/Monterrey VI aqueduct (MIA filed Sep-2026) and a 4 m raise of El Cuchillo (target 2029).

### Cited Findings
- **2022 timeline:**
  - 3-Feb: extreme drought declared.
  - March: CONAGUA warned of "día cero" within about 60 days.
  - 25-Mar: zonal tandeo began. — [Wikipedia 2022 crisis](https://es.wikipedia.org/wiki/Crisis_del_agua_en_Nuevo_Le%C3%B3n_de_2022)
  - April: supply window set at 4:00–10:00 am, which most homes did not receive. — [Pie de Página](https://piedepagina.mx/la-hora-cero-de-monterrey/)
  - June: El Cuchillo 45.45%, La Boca 8.22%, Cerro Prieto 2.06%. Pre-crisis shares of supply were El Cuchillo 35%, La Boca 15.5% and Cerro Prieto 12.5%. — [Informador 20-Jun-2022](https://www.informador.mx/mexico/Sequia-en-Nuevo-Leon-2022-Que-esta-pasando-con-el-agua-en-Monterrey-20220620-0128.html)
  - 28-Jun: CONAGUA reported a deficit of more than 3,000 L/s. El Cuchillo supplied 5,000 L/s, La Boca 0, Cerro Prieto 2,500 ("en riesgo de vaciarse") and other sources 260 L/s. — [La Jornada 28-Jun-2022](https://www.jornada.com.mx/noticia/2022/06/28/politica/deficit-de-mas-de-3-mil-litros-por-segundo-para-monterrey-conagua-1638)
  - Jul-2022: Cerro Prieto at 0.5%. — [NASA EO](https://earthobservatory.nasa.gov/images/150123/a-reservoir-runs-dry)
- **El Cuchillo II:** 93 km, 84" pipe, 5 pumping stations, up to 5,000 L/s. — [MVS 10-Sep-2026](https://mvsnoticias.com/nuevo-leon/2026/9/10/nuevo-leon-refuerza-seguridad-hidrica-con-el-cuchillo-ii-y-presa-leon-745437.html)
  - First stage on 13-Sep-2023 delivered 1,200 L/s to San Roque, rising to 2,200 L/s from 26-Oct with the second pump train, then full operation with five. — [Forbes México](https://forbes.com.mx/inauguran-por-completo-acueducto-el-cuchillo-ii-en-nuevo-leon/)
  - Inaugurated with AMLO in Dec-2023 at about 4,000 mdp over budget. — [Latinus 16-Dec-2023](https://latinus.us/portada/2023/12/16/amlo-samuel-garcia-inauguran-el-acueducto-el-cuchillo-ii-obra-que-costo-mil-millones-de-pesos-mas-de-lo-presupuestado-103614.html)
  - With the 1994 aqueduct, El Cuchillo can deliver up to about 10,000 L/s. — [El Universal](https://www.eluniversal.com.mx/estados/inauguran-amlo-y-samuel-garcia-acueducto-el-cuchillo-ii-dotara-de-agua-a-53-millones-de-habitantes/)
  - Actual use on 13-Oct-2026 was 2.685 m³/s. — [MVS 14-Oct-2026](https://mvsnoticias.com/nuevo-leon/2026/10/14/nivel-de-las-presas-en-nuevo-leon-hoy-miercoles-14-de-octubre-del-2026-749708.html)
- **Presa Libertad/León:** status, cost and fill as in section 3. — [88.9 Noticias 6-Feb-2026](https://889noticias.mx/noticias/conagua-confirma-que-la-presa-leon-esta-lista-para-su-entrega/), [MVS 24-Apr-2026](https://mvsnoticias.com/nuevo-leon/2026/4/24/revisan-presa-libertad-acuerdan-cambios-antes-de-su-entrega-730336.html). The state describes it as a 1,950 m × 52 m dam ("longest in Latin America"). — [MVS 10-Sep-2026](https://mvsnoticias.com/nuevo-leon/2026/9/10/nuevo-leon-refuerza-seguridad-hidrica-con-el-cuchillo-ii-y-presa-leon-745437.html)
- **SADM "Programa de Eficiencia Hídrica"** covers sectorization, telemetry, macro/micro-metering, pressure modulation and network renewal. The current director general is Eduardo Ortegón Williamson; the previous one was Juan Ignacio Barragán. — [MVS 10-Sep-2026](https://mvsnoticias.com/nuevo-leon/2026/9/10/nuevo-leon-refuerza-seguridad-hidrica-con-el-cuchillo-ii-y-presa-leon-745437.html)
- **El Cuchillo raise:** a 4 m curtain raise with an executive project and CONAGUA feasibility "visto bueno", though not yet approved. The governor claims capacity would go from 1,000 to 2,000 Mm³. Construction would take about 1.5 years, with a 2029 target. — [Publimetro 16-Aug-2026](https://www.publimetro.com.mx/nuevo-leon/2026/08/17/presa-el-cuchillo-pasara-de-grande-a-enorme-proyectan-duplicar-su-capacidad)
- **Pánuco / Monterrey VI:** SADM filed a regional MIA (Sep-2026) for an aqueduct from the Río Pánuco (Ébano, SLP). First stage 5,000 L/s, six sections. Estimated cost is 38,758.9 mdp (2024 pesos). There is opposition from SLP and environmental groups. — [Grupo Animal](https://grupoanimal.mx/estados/monterrey-vi-mega-acueducto-nuevo-leon-agua-rio-panuco) (date and cost per search summary; verify in the SEMARNAT Gaceta Ecológica)
- The FAMM Plan Hídrico NL 2050 (2018) is being updated, since the first version used data valid to 2015. — [Informe FAMM 2023](https://famm.mx/archivos/Informe_FAMM_2023_rev2.pdf). In 2026, Milenio criticised governments for choosing the costliest options in the plan. — [Milenio](https://www.milenio.com/comunidad/plan-hidrico-2050-nuevo-leon-proyectos-costosos-agua-monterrey-famm)
- CONAGUA said the NL→Tamaulipas transfer would not happen in 2025 for the first time in years. — [POSTA](https://www.posta.com.mx/nuevo-leon/no-habra-trasvase-de-agua-entre-nuevo-leon-y-tamaulipas-en-2025/vl2120145)

### Inferences
- The system is comfortable for now (≈64% of combined NAMO), but El Cuchillo's slide from ~98% in Oct-2024 to ~51% by 1-Oct-2026 shows how fast drawdown happens at about 7 m³/s of extraction.

### Gaps
- No official 2026 total supply figure (L/s by source) was found. A June-2024 figure of 17,228 L/s appeared in a search summary but was not verified.
- No confirmation was found that Presa Libertad has formally been handed over or is delivering water regularly as of Oct-2026.

## 11. Existing studies and dashboards, and the most valuable data-crossing opportunities

### Takeaway
Plenty of plans and reports exist: FAMM Plan Hídrico 2050, the Tec book, UANL observatory, HCNL analyses, NASA imagery. No public, live, open-data dashboard for Monterrey water was found that combines reservoirs, aquifers, concessions and access inequality. The SINA WFS, SADM's niveles page and SMN files are enough to build one.

### Cited Findings
- FAMM: Plan Hídrico NL 2050 (two years of studies, Monte Carlo demand scenarios, a 95% reliability target) and annual reports. — [CONL](https://www.conl.mx/noticias/49), [FAMM capítulos](https://famm.mx/capitulos.php), [Informe FAMM 2023](https://famm.mx/archivos/Informe_FAMM_2023_rev2.pdf), [HCNL dictamen Plan Hídrico 2050](https://www.hcnl.gob.mx/trabajo_legislativo/pdf/lxxv/PROYECTO%20DE%20DICTAMEN%20DEL%20EXPEDIENTE%2012485%20LXXV%20%20PLAN%20HIDRICO%20DE%20NL%202050%20ok.pdf)
- Tec de Monterrey, "Agua para Monterrey, Ed. 2021". — [repositorio.tec.mx](https://repositorio.tec.mx/handle/11285/642843)
- UANL IINSO observatory water diagnosis. — [observatorio.iinso.uanl.mx](http://observatorio.iinso.uanl.mx/index.php/diagnostico/diagnostico-01/diagnostico-0101?start=2)
- HCNL (PAN group) analysis of the water crisis (Mar-2023). — [HCNL GLPAN](https://www.hcnl.gob.mx/glpan/2023/03/analisis-de-la-crisis-de-agua.php)
- Cómo Vamos NL. — [comovamosnl.org](https://comovamosnl.org/)
- Wikipedia overview: [Urban water management in Monterrey](https://en.wikipedia.org/wiki/Urban_water_management_in_Monterrey)
- Reusable code and data: [sinagua (Sinaloa dam dashboard)](https://github.com/raulastrga/sinagua), [Kaggle CONAGUA presas](https://www.kaggle.com/datasets/edehoyos/conagua-presas/data)

### Inferences (ranked data-crossing opportunities)
1. **"Who drinks from the overexploited aquifers?"** Join REPDA aprovechamiento points (titular, uso, volume; WFS m01) to the 2023 availability table (m06) and piezometric trends (m06_vwpiezometria). Map concessions in Campo Buenos Aires, Campo Mina, AMM and Citrícola by user type. This is the first open, reproducible answer to the 2022 industry-vs-people debate, with the caveat that REPDA volumes are concessioned rather than measured and that SADM sells to industry.
2. **Reservoir early-warning / days-of-supply:**
   - History: SINA daily storage 1995 to Apr-2025.
   - Current: a daily scraper of SADM niveles plus MVS daily articles.
   - Drivers: SMN station 19052 or CHIRPS rainfall, and municipal drought categories.
   - Use the daily extraction rates (m³/s per aqueduct) to project depletion.
3. **Presa Libertad satellite tracker:** Sentinel-2 NDWI area time series, plus an area–volume curve calibrated on El Cuchillo and Cerro Prieto against SINA storage. This fills the only major reservoir with no public level data.
4. **Inequality of resilience:**
   - Household storage: INEGI 2020 AGEB/manzana (tinaco/cisterna/agua entubada).
   - Hydraulics: elevation/DEM as a pressure-zone proxy.
   - Service failures: García and colonia tandeo/outage reports from news and AyD posts.
   - Survey and socio-economic context: Cómo Vamos survey figures and SINA marginación layers.
   - This targets the García vs San Pedro gap (18 days vs 1 day without water in 2022).
5. **Leak and renewal prioritization:** non-revenue water of 41–48% (monthly), asbesto-cemento trunk-main km by diameter, and geolocated burst and repair news (e.g. the Apr-2026 48" main). Pair with a PNT request for sector-level production vs billing.
6. **Reuse and circular water:** SADM treated-water reuse contracts (5.3–5.9 Mm³/month), WWTP capacity and flow (m29), and industrial REPDA titles. Estimate how much industrial groundwater could be substituted.
7. **Flood layer for Alberto 2024:** Sentinel-1 flood extent, SADM's 167 km pluvial network (PNT for geometry), SINA protection works (m46), and INEGI blocks.
8. **Water-quality decay audit:** the RENAMECA sampling collapse after 2019, crossed with the semáforo results for metals and nitrates in AMM wells.

### Gaps
- Could not find a 2024–2026 Cómo Vamos NL water-specific survey release, or any Tec/UANL live dashboard.
- Agua para Todos, Mexicanos contra la Corrupción and Animal Político NL water-concession pieces were not found in this pass. They are worth a targeted follow-up.
