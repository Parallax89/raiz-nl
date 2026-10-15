# Open data from the Nuevo León government and the AMM municipalities, plus the October 2026 hackathon

Research date: 2026-10-14. Unless a line says otherwise, every portal and API below was fetched live from the Jarvis VPS that day: HTTP status, CKAN/GeoNode/WFS API calls, CSV headers and feature counts. Some "last updated" values come from the APIs' own `metadata_modified`/`last_updated` fields, so they can differ from the real data period. Where both are known, both are given.

---

## 1. Does Nuevo León have an official open data portal, what does it host, are there APIs, and is it maintained in 2025-2026?

### Takeaway
Yes. The real portal is **datosabiertos.nl.gob.mx**. It is a front page over a **CKAN 2.10.4** catalog at **catalogodatos.nl.gob.mx**, and the full CKAN Action API is open with no key. On 2026-10-14 the API returned **132 public datasets**, which is far below the "368 datasets" in the October 2025 press release. Almost every resource is a CSV with a data dictionary. Location detail is mostly at the municipality level, with a few lat/lon point datasets. The catalog is actively maintained: many resources were uploaded between Sept and Oct 2026. Watch out for **datos.nl.gob.mx**: it is NOT the open data portal but the Secretaría de Economía's economic statistics site.

### Cited Findings
**Portal and API facts**
- The front end is https://datosabiertos.nl.gob.mx/ (title "Datos Abiertos NL"). Its links point to the catalog at http://catalogodatos.nl.gob.mx/dataset/ and to /group/ and /organization/. The footer says it is supported by the "Subsecretaría de Tecnologías" — [datosabiertos.nl.gob.mx](https://datosabiertos.nl.gob.mx/)
- The catalog runs CKAN 2.10.4 (`status_show` returns ckan_version 2.10.4, site_url https://catalogodatos.nl.gob.mx). The open API endpoints are `https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000`, `package_show?id=<name>`, `organization_list` and `group_list` — [CKAN status_show](https://catalogodatos.nl.gob.mx/api/3/action/status_show)
- Gotcha: `https://datosabiertos.nl.gob.mx/api/3/...` returns 404 (nginx), so API calls must use the **catalogodatos** host — [404 check](https://datosabiertos.nl.gob.mx/api/3/action/package_list)
- On 2026-10-14 `package_search` reported **count = 132** datasets. Resource formats: 129 CSV, 3 ".CSV", 1 XLSX, 1 JSON, 1 TXT. The `organization_list` call returned only 25 organizations, but the datasets themselves belong to roughly 80 distinct agencies — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000&sort=metadata_modified%20desc)
- 16 thematic groups. Counts as returned by group_list (a dataset can sit in several groups): Asistencia Social 19, Infraestructura 16, Administración 14, Educación 14, Atención Ciudadana 11, Perspectiva de Género 11, Transparencia 10, **Medio Ambiente 9**, Participación 8, Turismo 8, **Movilidad y Transporte 7**, Cultura 6, Deportes 5, **Salud 5**, **Seguridad 5**, Agroalimentario 3 — [group_list](https://catalogodatos.nl.gob.mx/api/3/action/group_list?all_fields=true)
- Licenses: per-dataset `license_id` is **odc-by** (109 datasets) or **cc-by** (20). The "CC BY-NC-SA 4.0" notice in the portal footer applies to the VÍA design system ("© 2024 de la Subsecretaría de Tecnologías bajo licencia CC BY-NC-SA 4.0"), not to the data — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000); [portal footer](https://datosabiertos.nl.gob.mx/)
- History: Governor Samuel García launched the portal in August 2024 under the Plan de Acción Local de Gobierno Abierto 2022-2024, with 17 datasets in 5 categories — [El Financiero](https://elfinanciero.com.mx/monterrey/2024/08/14/transparenta-samuel-garcia-informacion-de-su-gobierno-presenta-portal-de-datos-abiertos/); [Posta](https://www.posta.com.mx/nuevo-leon/presenta-estado-el-portal-de-datos-abiertos-del-gobierno-de-nuevo-leon/vl1602780)
- A state communiqué dated 28 Oct 2025 claimed 25 categories, **368 datasets** and more than 1,000 downloadable files, plus a technical committee and an "OX" award — [nl.gob.mx docx](https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/Contralor%C3%ADa%20y%20Transparencia%20Gubernamental/Noticias/20251028_01_nl_gobiernoabierto_rendicioncuentas.docx). This conflicts with the **132** the public API returns today; see the Inferences.
- Maintenance: dataset `metadata_modified` dates run from 2025-10-13 to **2026-10-14**. About 28 datasets carry a 2026-10-14 timestamp (for example consulta general, salud mental, estadística penitenciaria and 070). Some resources really are fresh: consulta general CSV parts 18-21 were uploaded 2026-10-13, salud mental 2025-2026 on 2026-10-08, and the 2022-2024 nacimientos files on 2026-10-13 — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000&sort=metadata_modified%20desc)
- Example of an update lag: the 070 dataset's metadata says "Periodo de actualización: Mensual; Siguiente actualización: julio 2026", yet its newest resources are June 2026, uploaded 2026-07-08 — [package_show atenciones070](https://catalogodatos.nl.gob.mx/api/3/action/package_show?id=atenciones070)
- **datos.nl.gob.mx** is "DATA NUEVO LEÓN | Datos económicos de Nuevo León", a WordPress statistics service of the **Secretaría de Economía**. It covers IMSS employment and wages to Sept 2026, ENOE unemployment to Q2 2026, ITAEE to Q1 2026, exports, Censo Económico 2024 and Encuesta Intercensal 2025 infographics by municipality, and offers a monthly PDF "Ficha" (Sept 2026). It is not a CKAN and has no API (`/api/3/...` returns a WP 404) — [datos.nl.gob.mx](https://datos.nl.gob.mx/)
- `https://www.nl.gob.mx/datos-abiertos` redirects to the **Contrataciones Abiertas** page (`/es/datosabiertos-contrataciones-abiertas`) — [nl.gob.mx redirect](https://www.nl.gob.mx/es/datosabiertos-contrataciones-abiertas)
- **OCDS public procurement API is live.** `https://api-ocds.nl.gob.mx/api/releases` returns paginated OCDS 1.1 JSON. The newest release seen is dated 2026-10-09 (ocid prefix `ocds-k3ufh7`). Publisher: Secretaría de Administración. License: `https://datos.gob.mx/libreusomx` — [OCDS API](https://api-ocds.nl.gob.mx/api/releases); [single release](https://api-ocds.nl.gob.mx/api/releases/673d316c7e60f2c8230bcf15)

**State CKAN inventory most useful for a hackathon.** Dataset pages are `https://catalogodatos.nl.gob.mx/dataset/<slug>`. Columns come from the CSV headers. The "Updated" column is the newest resource upload date. Every row is sourced from [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000) plus a direct CSV fetch.

| Slug / name | Agency | Format | Spatial grain | Time / updated | Key columns and gotchas |
|---|---|---|---|---|---|
| `consulta-general-y-especialidades` | Secretaría de Salud | 43 CSV parts | per consultation; `municipio_unidad_medica` | 2024-2026; parts uploaded 2026-10-13 | fecha_consulta, edad, sexo, peso, altura, institucion, ICD group/disease. Very large and split into parts. Location is the clinic's municipality, not the patient's home. |
| `salud-mental`, `salud-bucal`, `planificacion-familiar` | Secretaría de Salud | CSV | per consultation, by municipality | 2024-2026 (salud mental 2025-26 uploaded 2026-10-08) | Same schema as consulta general |
| `nacimientos-registrados-en-unidades-hospitalarias-...` | Servicios de Salud NL OPD | CSV, one per year | per birth, by municipality and hospital name | 2022-2025 | fecha/hora, edad_gestacional, peso, talla, sexo, ICD anomalies, resolución, nombre_unidad, municipio |
| `estadistica-penitenciaria` (+ `-de-ingresos`, `-egresos`) | Secretaría de Seguridad | monthly CSV (9 resources) | per inmate record; state/municipality of origin | 2024 to Dec 2025 (Dec 2025 uploaded 2026-01-14) | centro_penitenciario, delito_homologado, estatus_juridico, sexo, rango_edad, etnia, escolaridad. The only crime-type data on the portal: no incidence and no geolocation. |
| `atenciones070` | Sistema de Atención Ciudadana 070 | CSV (32; two halves per month) | per citizen request, by municipality | to June 2026 (uploaded 2026-07-08) | Folio, date, canal, categoría, servicio, subtipo, dependencia responsable, municipio. No coordinates. |
| `rutas-empresas` and `2024_2025_tpe_publico_setme` | Instituto de Movilidad y Accesibilidad (IMA) | CSV | per bus route | 2024-2025, Sept-2025 period | modalidad_SETME, nombre_ruta, units, concesionario, tarifa, horario, **pasajeros_periodo, km, cumplimiento, IPK**, tiempo_recorrido |
| `paradas` (IMA) | IMA | CSV | per route | Sept 2025 | **Gotcha:** `georeferencia` holds **Google My Maps links**, not coordinates |
| `paradas-oficiales-stc-metrorrey` | Metrorrey | CSV | **stop points with lat/lon** | 2024-2025 (uploaded 2025-11-12) | periodo, modalidad, tipo_servicio, nombre_ruta, latitud, longitud, ubicación |
| `unidades-de-transporte-publico`, `unidades-del-stcm`, `rutas-por-empresa-stc-metrorrey` | IMA / Metrorrey | CSV | per vehicle / route | 2024-2025 | plate, fuel type, capacity, age, insurer |
| `fuentes-de-agua`, `uso-de-agua`, `agua-reutilizada`, `infraestructura-de-agua` | Servicios de Agua y Drenaje de Monterrey (SADM) | CSV | municipality (fuentes) or AMM-wide monthly totals | from Sept 2024; **last update 2025-11-07, about 11 months stale** | uso: consumo promedio, disponibilidad, **agua_no_contabilizada (%)**; infraestructura: pipe km by diameter and material, **no geometry** |
| `residuos-solidos-urbanos` | SIMEPRODE | CSV | municipality × month | 2025-2026 (uploaded 2026-05-06) | periodo, mes, municipio, rsu_ingresados |
| `denuncias-de-maltrato-animal-2026` (+ 2025) | Secretaría de Medio Ambiente | quarterly CSV | per complaint, by municipality | T1-T2 2026 | tipo_denuncia, monto_sancion, aseguramiento |
| `diagnosticos-comunitarios-2024` | Secretaría de Participación Ciudadana | CSV | **colonia + lat/lon** | 2024-2025 quarterly | assembly attendance, demographics, family types, values survey |
| `sitios-de-internet-gratuitos-conectatenl` | Secretaría de Administración | CSV | **lat/lon**, colonia, CP | 2024, 2025 | free-WiFi sites with upload/download speeds and max users |
| `licencias-de-alcoholes-2026` | Secretaría de Finanzas y Tesorería | CSV | street address and municipality (geocodable) | 2026 (uploaded 2026-05-21) | número, domicilio, nombre_comercial, giro, fecha, anuencia municipal, estatus |
| `directorio-de-parques-osetur-nuevo-leon` / `visitantes-a-parques-nuevo-leon` | OSETUR | CSV | **lat/lon** per park | 2026 | horarios, tarifa, capacidad, visitantes |
| `listado-de-escuelas` (Escuelas TCJA), `planteles-educativos`, `listado-de-telebachillerato` | Secretaría de Educación | CSV | address and municipality; **CCT key** | 2025 | No coordinates. Join on CCT to the SEP/INEGI school catalogs. |
| `contratos-smpu` | Secretaría de Movilidad y Planeación Urbana | CSV | **Coordenadas** field per public work | uploaded 2026-06-29 | Licitación, Contrato, Obra, Empresa, Ubicación, Coordenadas, Monto |
| `contrataciones-abiertas-direccion-general-compro-nuevo-leon` | Secretaría de Administración | JSON plus about 90 links to the OCDS API | per procurement process | Nov 2024 onward | Use the API directly (see above) |
| `indicadores-de-desempeno-del-gobierno-del-estado-de-nuevo-leon` | Secretaría Técnica | CSV | state | PED 2022-2027 indicators; IAG 2020-2025 | Goals, frequency and source of each state KPI |
| `base-de-datos-de-entrega-de-acciones-de-vivienda` and other Instituto de la Vivienda datasets | IVNL | CSV | municipality | 2025-2026 | beneficiaries by sex and program |
| Hambre Cero, Jefas de Familia, Discapacidad, Impulso a Cuidadoras beneficiaries | Secretaría de Igualdad e Inclusión | CSV | municipality (not checked per file) | uploaded Feb 2026 | social program coverage |
| `licencias-de-caza-deportiva-por-municipio-2026` | Parques y Vida Silvestre NL | CSV | municipality | 2026 | the only Parques y Vida Silvestre dataset |
| `produccion-agricola-2022-2024`, `pib-agroindustrial-...` | Desarrollo Regional y Agropecuario | CSV | state / municipality | 2022-2024 | |

### Inferences
- The gap between the 368 datasets claimed in Oct 2025 and the 132 the API returns likely means the press figure counted something else (resources, or private/draft datasets), or that some datasets were removed. A team should trust the API count.
- The state portal is strong on **administrative microdata** (health consultations, births, 070 requests, transit operations) at the **municipality level**. It is weak on **geospatial** data (few lat/lon datasets, no polygons) and has **no** air quality, crime incidence or cadastre data. For anything spatial in the AMM, pair it with Monterrey's MIDE GeoNode (section 2).
- The best cross-agency join keys on the state portal are `municipio` (normalize spelling and accents), CCT for schools, and lat/lon in the few point datasets.

### Gaps
- I could not tell whether the 368 datasets include private or harvested ones; `package_search` with no authentication shows 132.
- I did not verify a per-file municipality column for every social program dataset.

---

## 2. What do Monterrey, San Pedro Garza García and the other AMM municipalities publish?

### Takeaway
**Monterrey is the standout.** Its old CKAN at datos.monterrey.gob.mx is dead, but **MIDE (mide.monterrey.gob.mx)** is a public **GeoNode** with **125 downloadable vector layers** over an open **WFS**. These include 444,948 geolocated traffic incidents since 2017, about 320k citizen reports, predio-level land use (363k polygons), flood zones, construction permits, transit routes and stops, and a colonia-level heat-island / PM2.5 / tree-canopy index. **San Pedro**'s CKAN still works but is stale (last change June 2025). **Escobedo** and **Santa Catarina** publish small XLSX sets (Escobedo's were updated May 2026). **Guadalupe**'s zoning and risk-atlas layers sit on a public, undocumented GeoServer. **Apodaca** publishes its risk atlas only as PDFs.

### Cited Findings
**Monterrey: MIDE GeoNode (recommended primary source)**
- `https://mide.monterrey.gob.mx` is a GeoNode/MapStore instance. The open REST API `https://mide.monterrey.gob.mx/api/v2/resources?page_size=200` returned **175 resources**: 125 vector datasets, 18 maps, 16 documents, 12 geostories and 4 dashboards. Every dataset carries the `download_resourcebase` permission for anonymous users — [MIDE API](https://mide.monterrey.gob.mx/api/v2/resources?page_size=200)
- WFS endpoint: `https://mide.monterrey.gob.mx/geoserver/ows`. GetCapabilities returns 200 (457 KB). Example download: `https://mide.monterrey.gob.mx/geoserver/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=geonode:incidentes_viales&outputFormat=application/json` — [MIDE WFS caps](https://mide.monterrey.gob.mx/geoserver/ows?service=WFS&version=2.0.0&request=GetCapabilities)
- Key layers, with feature counts from WFS `resultType=hits` and `last_updated` from the API — [MIDE API](https://mide.monterrey.gob.mx/api/v2/resources?page_size=200); [MIDE WFS](https://mide.monterrey.gob.mx/geoserver/ows):
  - `geonode:incidentes_viales`: **444,948 points**, from 2017-01-01. Fields: fecha, hora, folio, lat/lon, calle, cruce, colonia, sentido, vehicle types. Layer updated 2025-03-14.
  - `geonode:reportes_ciudadanos`: **240,843 rows**, updated 2026-07-28. Fields: folio, fecha_hora_recepcion, categoría, descripción, secretaría, departamento, factibilidad, estatus, fecha_resolucion. **Gotcha: geometry is null** in the sample (no coordinates), and dates mix formats (`12/9/2025` vs `8/23/25`).
  - `geonode:reportes_ciudadanos_mty`: **79,413 rows** (2025, for example "Luminaria Apagada"). Updated 2025-10-17, also without geometry.
  - `geonode:reportes_911_violencia_genero_...`: **10,000 points** from 2017. Fields: fecha, municipio, colonia, descripcion_tipo, corporación, hora, cierre, lat/lon, vía de recepción. The round 10,000 may be a cap or sample.
  - `geonode:uso_suelo`: **363,368 polygons**, roughly predio level. Fields: delegación, distrito, calle, colonia, tipo (use), tipo_tenencia, clave_zonificacion_secundaria, fecha_digitalizacion (from 2007).
  - `geonode:uesi_mty2022` ("Climate data"): **1,141 colonia polygons** with population, **NO2, PM2.5, tree canopy/cover, UHI (day/night), NDBI**. Updated 2026-05-02. Excellent for crossing data.
  - `geonode:colonias_2022`: 1,143 colonia polygons.
  - `geonode:permisos_de_construccion_2026`: 811 points (expediente, giro, propietario, delegación, trámite, niveles, m²). Updated 2026-09-14. There is also an older `permisos_construccion` layer (2026-05-08).
  - `geonode:zonas_inundacion` (62 polygons), `puntos_inundacion`, `area_deslizamientos`, `falla_volteo`, `rios_arroyos`, `drenaje_pluvial`, `amortiguamiento_pluvial`, `tanques_almacenamiento`, `red_agua`, `geologia`, `vegetacion`, `area_natural_protegida`, `corredores_biologicos`. Most were updated 2025-07-09.
  - Mobility: `rutas_transporte` (**4,044 route lines** with grupo, modalidad, subsistema, tipo_unidad, longitud), `paradas_transporte`, `regio_ruta_` (7 lines), `paradas_ruta_a` through `_g`, `lineas_transporte_masivo`, `sistema_transporte_publico`, `ciclovias` (2026-09-29), `biciestacionamientos_26`, `vias_peatonal_`, plus World Cup layers (`zona_baja_velocidad`, `zona_sin_vehiculos`, `puntos_estacionamiento_l`, all updated 2026-10-13/14).
  - Urban planning: `zonificacion_primaria`, `zonificacion_secundaria_giros_compatibilidad`, `densidades`, `corredores_urbanos`, `distritos`, `delegaciones`, `alineamientos_viales`, `licencias_casinos`, `bd_obras_publicas` (2026-05-08), `calles_intervenidas`, `banquetas`.
  - Social and services: `centrosdesalud`, `escuelas_monterrey_sep`, `bibliotecas_municipales`, `unidades_deportivas`, `centros_atencion_sistemas_dif`, `reportes_maltrato_nna`, `prevencion_trabajo_infantil_26`, `puntos_wifi`, `puntos_reciclaje`, `rutas_recoleccionbasura`, `semaforos`, `huertos_urbanos`, `ediciones_adopta` (Adopta un Árbol: 13 planting events with species and counts).
  - Security: `totems_emergencia` (CAIE), `centros_de_mando`, `poligonos_operativos`, `cortes_circulacion_`.
- Documents on MIDE: **Informe Estadístico de Siniestros de Tránsito 2025** (doc 21619, 2026-09-28) and 2024/2023/2019-2022 editions; the Inventario Municipal de Emisiones GEI; the Programa Estatal de Cambio Climático NL — [MIDE API](https://mide.monterrey.gob.mx/api/v2/resources?page_size=200)
- **The old portal is dead.** `datos.monterrey.gob.mx` now serves the generic Quasar SPA of monterrey.gob.mx (build 2025-08-19), and old CKAN links such as `.../dataset/67b3e7a7-.../download/reporte-anual-de-datos-abiertos-2022-2.pdf` return a 1 KB HTML shell instead of the file — [datos.monterrey.gob.mx](https://datos.monterrey.gob.mx/); search result for the old link: [old CKAN URL](https://datos.monterrey.gob.mx/dataset/67b3e7a7-fe3a-44e3-8962-6ec8fa24b7cb/resource/8058f460-46dd-45a5-8ab4-eb1600545897/download/reporte-anual-de-datos-abiertos-2022-2.pdf)
- The SPA bundle references `https://ows.monterrey.gob.mx/pub/wms`, but that host **does not resolve in DNS** (checked 2026-10-14) — [datos.monterrey.gob.mx JS bundle](https://datos.monterrey.gob.mx/assets/index.8f76c916.js)
- Monterrey's data governance rules: "Lineamiento de Criterios, Estándares y Operación de Gestión de Datos y Apertura de Datos" (SIGA) — [monterrey.gob.mx PDF](https://monterrey.gob.mx/pdf/new/Lineamientos/SIGA/L_SIG_GGD_09_Ver_02_Lineamiento_de_Criterios_Estandares_y_Operacion_de_Gestion_de_Datos_y_Apertura_de_Datos.pdf)
- **Atlas de Riesgo, Monterrey:** the atlas in force dates from **2009**. In 2024 the city council approved a public consultation for a new "Atlas de Peligros y Riesgos" — [Dictamen de Cabildo 2024](https://monterrey.gob.mx/pdf/dictamenes_cabildo/2024/Dictamen_mediante_el_cual_se_aprueba_la_Consulta_P%C3%BAblica_para_la_Expedici%C3%B3n_del_Atlas_de_Peligros_y_Riesgos_de_la_Ciudad_de_Monterrey..pdf). MIDE has a "Riesgos y Vulnerabilidad" map (updated 2026-08-19) built on the hazard layers listed above — [MIDE API](https://mide.monterrey.gob.mx/api/v2/resources?page_size=200)
- **Regio Ruta** is Monterrey's free municipal bus. It started in July 2025 and has 7 routes. With ITDP, Ualabee and Google, the city published static GTFS and then **real-time GTFS to Google Maps in June 2026** — [ITDP technical note, Jun 2026](https://mexico.itdp.org/wp-content/uploads/2026/06/GTFS-Nota-tecnica-eventos-masivos-Jun-2026-.pdf)

**San Pedro Garza García**
- `https://datos.sanpedro.gob.mx` runs **CKAN 2.7.6** (an old version) and has an open API. It holds **12 datasets**, all CC-BY-4.0 — [San Pedro CKAN status](https://datos.sanpedro.gob.mx/api/3/action/status_show); [package_search](https://datos.sanpedro.gob.mx/api/3/action/package_search?rows=100)
- Datasets and freshness — [package_search](https://datos.sanpedro.gob.mx/api/3/action/package_search?rows=100):
  - `permisos-de-construccion-autorizaciones-de-acciones-urbanas`: CSV; metadata 2025-06-17, resources 2024-09-10.
  - `informe-de-permisos-de-eventos-publicos` and `informe-de-permisos-en-via-publica`: 16 CSVs each, from 2023; updated 2024-10-17.
  - `construccion-rehabilitacion-calles`, `-banquetas`, `-infraestructura-ciclista`: 2024-09-10. **Gotcha:** one "CSV" resource is actually an Apple `.numbers` file (`2.-bd-calles-siop_sspma-bd-calles.numbers`).
  - `reportes-de-atencion-ciudadana`: **2023 only**.
  - `justicia-civica`: 11 monthly CSVs, 2023.
  - `infraestructura-ciclista-existente`: **GeoJSON/KMZ/KML**, 2023-04-25.
  - COVID-era purchases, donations and food-aid beneficiaries (2020-2022).
- `transparencia.sanpedro.gob.mx` showed "Sitio en Mantenimiento" on 2026-10-14 — [transparencia.sanpedro.gob.mx](https://transparencia.sanpedro.gob.mx/)
- `datosabiertos.sanpedro.gob.mx` returns HTTP 500 — [datosabiertos.sanpedro.gob.mx](https://datosabiertos.sanpedro.gob.mx/)
- For background only, San Pedro used the GOAT accessibility tool (Plan4Better) in a 2021 pilot for its pedestrian master plan — [plan4better](https://plan4better.de/de/references/san-pedro-garza-garcia-mexico)

**General Escobedo**
- `https://escobedo.gob.mx/?p=datosabiertos` lists XLSX files under `./transparencia/datosabiertos/`. **PERMISOS DE CONSTRUCCIÓN** (`permisos_de_construccion_202605.xlsx`), **OBRAS PÚBLICAS** (`obras_publicas_202605.xlsx`) and **REPORTES DE ATENCIÓN CIUDADANA** (`reportes_atencion_ciduadana_202605.xlsx`) are all marked "actualización May,2026". Infraestructura ciclista, banquetas and calles are 2024-09. There is also a Plan de Acción Climática PDF (Nov 2025) and a listado de indemnizaciones PDF — [Escobedo datos abiertos](https://escobedo.gob.mx/?p=datosabiertos)
- The reportes XLSX downloaded fine on 2026-10-14 (HTTP 200, 770 KB, real xlsx MIME type) — [file](https://escobedo.gob.mx/transparencia/datosabiertos/reportes_atencion_ciduadana_202605.xlsx)
- Escobedo's "Georeferencia" page only embeds Google My Maps (desarrollo urbano, inspección) — [Escobedo georef](https://escobedo.gob.mx/?p=georef)

**Santa Catarina**
- **Gotcha:** the domain is **stacatarina.gob.mx**; `santacatarina.gob.mx` does not resolve. Its datos abiertos page offers XLSX and PDF files for banquetas, calles pavimentadas and infraestructura ciclista (`assets/BD-Calles_05.xlsx`, `BD-Infraestructura_ciclista_05.xlsx`, `BD-Banquetas.xlsx`) — [Santa Catarina datos abiertos](https://www.stacatarina.gob.mx/da/datosabiertos.html)

**Guadalupe**
- `https://visorurbano.guadalupe.gob.mx/` is a Leaflet viewer built by Proaxis on the **Programa Municipal de Desarrollo Urbano Guadalupe Visión 2040**, in force since 24 Nov 2023 — [Visor Guadalupe](https://visorurbano.guadalupe.gob.mx/)
- Its JavaScript calls a **public GeoServer**, `https://geoserver.visormetropolitano.com/geoserver`. WFS GetCapabilities lists **30 `gpe:` layers**: zonificación primaria/secundaria (`gpe_zonprimA_v7`, `gpe_zonsec_v4`), `gpe_densidades_v7`, `gpe_corredores`, `gpe_distritos`, `gpe_estructura_vial`, `gpe_terrenos_v3`, `gpe_poligonosactuacion`, `gpe_limitenuevo2`, and what look like **risk-atlas layers** (`ar08_amoniaco`, `ar08_expendios`, `ar08_zonapeligro`, `ar08_zonaresguardo`, `ar10_peligro`, `ar11_peligro`, `a11_vulne`, `gpe_ar01` through `gpe_ar07`). The rest are GeoServer demo layers — [visormetropolitano WFS caps](https://geoserver.visormetropolitano.com/geoserver/ows?service=WFS&version=2.0.0&request=GetCapabilities); [geovisor.js](https://visorurbano.guadalupe.gob.mx/geovisor.js)

**Apodaca**
- The Atlas de Riesgo page offers **PDFs only**: `Atlas_Riesgos.pdf`, plus `inundacion.pdf`, `peligros.pdf` and an Acuerdo, all uploaded 2025/02. There is also a "Transparencia Proactiva" page and a link to `visor.kukaku.com.mx` — [Apodaca atlas](https://apodaca.gob.mx/atlas-riesgo/); [Apodaca home](https://apodaca.gob.mx/)

**San Nicolás de los Garza**
- The homepage links to `pagina.sanicolas.gob.mx/MapaInteractivo` (a citizen-request and work-order map UI), to `consulta.sanicolas.gob.mx/Atlas/` (whose page title is "**Centro Meteorológico** · San Nicolás de los Garza") and to `transparencia.sn.gob.mx` — [San Nicolás home](https://sanicolas.gob.mx/sitio_oficial_pc); [Atlas/Centro Meteorológico](https://consulta.sanicolas.gob.mx/Atlas/)

**García, Juárez:** I found no datos abiertos, geoportal or atlas links on their homepages ([garcia.gob.mx](https://garcia.gob.mx/), [juarez-nl.gob.mx](https://juarez-nl.gob.mx/)), which leaves SIPOT on the Plataforma Nacional de Transparencia.

**Shared framework:** COTAI's "Datos Abiertos NL" joint declaration was signed by AMM municipalities including Apodaca, Escobedo, Guadalupe and San Nicolás — [COTAI DANL_DC_AMM.pdf](https://cotai.org.mx/descargas/DANL_DC_AMM.pdf)

### Inferences
- San Pedro, Escobedo and Santa Catarina publish the same handful of datasets (banquetas, calles, infraestructura ciclista, permisos de construcción, reportes de atención ciudadana). That looks like the minimum set from the COTAI "Datos Abiertos NL" agreement. It allows a **cross-municipality comparison** of construction permits, citizen reports and street works, but formats and periods differ (San Pedro 2023-24, Escobedo May 2026).
- For a 24-48 h project, **MIDE (Monterrey)** is the only municipal source that is large, geolocated, recent and API-accessible. Strong crosses:
  - uesi_mty2022 (heat island / PM2.5 / tree canopy by colonia) × colonias × Adopta un Árbol × parks.
  - incidentes_viales × ciclovías × the World Cup low-speed zones.
  - uso_suelo / permisos × flood zones.
  - Reportes ciudadanos × colonia, after geocoding, since the reportes layers have no coordinates.
- The Guadalupe GeoServer is technically open but undocumented, and its layer names are cryptic. Treat it as a bonus source and check the attribute meanings against the PMDU 2040 document.

### Gaps
- I did not find MIDE's data license. The GeoNode API shows anonymous download permission, but no license per layer was checked.
- I could not confirm whether `reportes_911_violencia_genero` is capped at 10,000 rows.
- The Regio Ruta GTFS feed URL was not found. It is published "on Google Maps" per ITDP, and the MobilityData catalog (3,530 feeds) has **no** Monterrey or Nuevo León feed — [Mobility Database catalog CSV](https://share.mobilitydata.org/catalogs-csv). A team would have to ask the municipality or ITDP/Ualabee for the files, or rebuild the routes from MIDE's `regio_ruta_` and `paradas_ruta_*` layers.
- I did not fully explore San Pedro's geoportal or PDU zoning layers (no portal found), Monterrey's PDU 2013-2025 official text, or the municipal 072/"MTY Reporta" APIs beyond the MIDE layers.
- I did not open the Apodaca `visor.kukaku.com.mx` or the San Nicolás meteorological site to check for downloadable data.

---

## 3. State agencies: what data does each expose, and how?

### Takeaway
Only a few agencies have machine-readable feeds. **SIMA** (air quality) has a live hourly web map but no public bulk download. **SADM** dam levels are HTML only, updated about every two days. The **Fiscalía**'s statistics site blocks non-browser and datacenter clients (HTTP 403). The **IRCNL** cadastre has only a JavaScript viewer and paid procedures. Mobility data is split between IMA/Metrorrey CSVs on the state CKAN and Monterrey's MIDE layers. **No public GTFS download was found for Metrorrey, TransMetro or Ecovía.**

### Cited Findings
**Air quality: SIMA (Secretaría de Medio Ambiente)**
- `https://aire.nl.gob.mx/` is the official site, with the live map `map_calidad.html` and `icars2020/map_calidad_icars.php`. The map PHP showed "Fecha y Hora del Reporte de Calidad del Aire: miércoles, 14 de octubre de 2026 a las 17:00 hrs", so it is **live and hourly**. It is labeled "datos en tiempo real NO VALIDADA del Índice de Aire y Salud" and carried a note about a transmission failure at the **Santa Catarina** station — [SIMA map PHP](https://aire.nl.gob.mx/SIMA2017phpgoogle/mapaSimaprbBing_icars_alt_ns_copy.php); [ICARS map](https://aire.nl.gob.mx/icars2020/map_calidad_icars.php)
- `SIMA2017reportes/ReporteDiariosimaIcars.php` has a DataTables table with "csvHtml5/excelHtml5" export buttons, but the static HTML contained only headers (Parámetro, Fecha y Hora, Valor, Unidad, Concentración Máxima, Norma). Data loads dynamically, so a team would have to scrape with a headless browser — [SIMA daily report](http://aire.nl.gob.mx/SIMA2017reportes/ReporteDiariosimaIcars.php)
- Downloadable reports are **stale PDFs**. Monthly reports stop around 2018 (`docs/reportes/mensuales/..._2018.pdf`) and municipal reports date from 2009-2015 — [rep_mensual](https://aire.nl.gob.mx/rep_mensual.html); [rep_mun](https://aire.nl.gob.mx/rep_mun.html)
- Network size: **15 stations × 6 criteria pollutants** (PM2.5, PM10, NO2, SO2, CO, O3), per Cómo Vamos NL's Oct 2025-Sep 2026 station-validity index — [CVNL GitHub README](https://github.com/EvaluacionInvestigacion-CVNL/indice-monitoreo-estaciones-gcv)
- Historical hourly SIMA data circulates as Excel files (`BD 2020.xlsx` through `BD 2025.xlsx`) given to Tec de Monterrey students, and the README says they are **not uploaded to GitHub**. Several student repos analyze SIMA data — [reto-sima-multivariados](https://github.com/Leo-issacs/reto-sima-multivariados); [danielnzlz01/SIMA](https://github.com/danielnzlz01/SIMA)
- The Secretaría de Medio Ambiente reported for H1 2026 that PM10 averaged 42.22 µg/m³ (vs 53.56 in 2025) and PM2.5 16.26 µg/m³ (vs 21.21) — [nl.gob.mx communiqué docx](https://nl.gob.mx/sites/default/files/repositorio/Dependencias/Secretar%C3%ADa%20de%20Medio%20Ambiente/Noticias/20260813_01_reduccion_nl_particulascontaminantes.docx)
- National fallback: SINAICA (INECC) is online (HTTP 200) — [SINAICA](https://sinaica.inecc.gob.mx/)

**Water: SADM (Servicios de Agua y Drenaje de Monterrey)**
- The "Niveles de Presas" page reported, as of **12 Oct 2026** (Dirección de Operaciones):
  - La Boca: 34.249 of 35.0 Mm³
  - Cerro Prieto: 244.474 of 295.0 Mm³
  - El Cuchillo: 646.816 of 1,123.0 Mm³
  - Total: 925.539 of 1,458.1 Mm³
  - Supply split: 60% surface, 40% groundwater
  - **HTML only**, so scrape it. — [SADM niveles](https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles)
- SADM also has an "Indicadores" section (management reports, POAs) — [SADM indicadores](https://pfiles.sadm.gob.mx/PFiles/indicadores)
- SADM's datasets on the state CKAN (water sources, use, reuse, pipe infrastructure) were last updated 2025-11-07 — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)

**Mobility: IMA (Instituto de Movilidad y Accesibilidad) and Metrorrey**
- `ima.nl.gob.mx` returned **HTTP 502**, and `nl.gob.mx/es/ima` returned 404 (2026-10-14) — [ima.nl.gob.mx](https://ima.nl.gob.mx/)
- `metrorrey.gob.mx` and `www.metrorrey.gob.mx` **do not resolve in DNS**. Metrorrey now lives at `https://www.nl.gob.mx/es/metrorrey`, which links a network map ("mapa-red-metrorrey") but no data files — [nl.gob.mx/metrorrey](https://www.nl.gob.mx/es/metrorrey)
- IMA and Metrorrey CSVs on the state CKAN cover routes, operators, passengers per period, IPK, units and stops (Metrorrey stops have lat/lon). See section 1 — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)
- Ridership: according to INEGI as reported by Líder Empresarial (May 2026), the metro area carried 12.3 million passengers in Feb 2026, 7.8 million of them on Metrorrey. TransMetro now integrates Ecovía — [Líder Empresarial](https://www.liderempresarial.com/como-crecio-el-transporte-publico-en-monterrey/)
- GitHub has no repos for "metrorrey gtfs" or "monterrey gtfs" (API search, 0 results on 2026-10-14). There are two 2026 repos analyzing the state CKAN mobility data — [chavaxlr12-boop stops coverage repo](https://github.com/chavaxlr12-boop/Cobertura-de-Paradas-Oficiales-por-Ruta-Septiembre-2025-)

**Security: Fiscalía General de Justicia and Secretaría de Seguridad**
- `fiscalianl.gob.mx` and `/estadisticas/` return **HTTP 403** to curl (even with a browser User-Agent) and to WebFetch — [fiscalianl.gob.mx/estadisticas](https://fiscalianl.gob.mx/estadisticas/)
- The press cites the Fiscalía's monthly statistics "Por Municipio", for example for Jan 2022 and May 2024 — [Milenio](https://www.milenio.com/politica/comunidad/leon-15-municipios-acumulan-91-25-delitos-enero-2022); [Milenio May 2024](https://www.milenio.com/politica/comunidad/nuevo-leon-cierra-mayo-2024-delitos-semaforo-delictivo)
- The state CKAN has only **penitentiary** statistics from Secretaría de Seguridad (monthly to Dec 2025) — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)
- Point-level security data comes from Monterrey's MIDE: 911 gender-violence reports (lat/lon, from 2017), traffic incidents (444,948 points), CAIE totems, command centers and operational polygons — [MIDE API](https://mide.monterrey.gob.mx/api/v2/resources?page_size=200)
- Consejo Nuevo León runs an **Observatorio de Seguridad y Justicia** (crime, prevention, policing, justice and security spending). Its latest finding was for Q2 2026, published 28 Jul 2026 — [conl.mx/observatorio](https://conl.mx/observatorio/)

**Protección Civil / Atlas de Riesgo**
- `www.nl.gob.mx/es/proteccioncivil` returned **403 "Acceso denegado"** and `pc.nl.gob.mx` did not respond — [nl.gob.mx PC](https://www.nl.gob.mx/es/proteccioncivil)
- In September 2026 a state deputy asked all **51 municipalities** to update their risk atlases urgently, which indicates the municipal atlases are outdated — [HCNL, Sept 2026](https://www.hcnl.gob.mx/glindependiente/2026/09/pide-rocio-montalvo-a-los-51-municipios-actualizar-atlas-de-riesgo-e-informar-estado-de-corporacione.php)
- Usable hazard layers at municipal level: Monterrey MIDE (flood zones and points, landslides, faults), the Guadalupe GeoServer (ar* layers), and Apodaca's atlas PDFs (section 2).

**Cadastre: Instituto Registral y Catastral (IRCNL)**
- The site is `https://ircnl.gob.mx/`; `irc.nl.gob.mx` does not resolve. Its map viewer `https://visor.ircnl.gob.mx` is a **Blazor WebAssembly** app (a 1 KB shell that showed "An unhandled error has occurred" to curl). Procedures run through `tramites.ircnl.gob.mx` (ModernizacionCatastral.aspx) — [ircnl.gob.mx](https://ircnl.gob.mx/); [visor.ircnl.gob.mx](https://visor.ircnl.gob.mx)
- The 2024 catastral modernization included a new aerial survey (200 km² photogrammetric flight) and a multipurpose cadastral cartography contract — [IRCNL modernization PDF](https://ircnl.gob.mx/media/2024/05/Proyecto-de-modernizacion-catastral-mayo-2024.pdf); [IRCNL June 2024](https://ircnl.gob.mx/media/2024/06/Evidencia-difusion-junio.pdf)
- On the state CKAN, IRCNL publishes only "Atenciones Ciudadanas" and transparency-request statistics — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)

**Salud, Economía, Planeación, Parques**
- Health: the state CKAN has consultation-level microdata (general, mental, oral health, family planning) and births by municipality (section 1) — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)
- Economy: DATA Nuevo León (Secretaría de Economía), with PDFs and infographics to Sept 2026 — [datos.nl.gob.mx](https://datos.nl.gob.mx/)
- Planning: Consejo Nuevo León's Plan Estratégico indicator monitor — [planestrategico.conl.mx/indicadores/objetivos](https://planestrategico.conl.mx/indicadores/objetivos). The state PED 2022-2027 indicator catalog CSV is on CKAN (`indicadores-de-desempeno-...`) — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)
- Parques y Vida Silvestre has only sport-hunting licenses by municipality (2026). Park visitor statistics come from OSETUR, Parque Fundidora and Fideicomiso Zaragoza (Parque El Salto) — [package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)

### Inferences
- For air quality in a hackathon, the realistic options are: (a) scrape SIMA's live hourly map or report during the event; (b) use MIDE's `uesi_mty2022` colonia-level PM2.5, NO2 and UHI as a static exposure layer; or (c) request historical hourly data, which takes too long for a weekend. SINAICA may carry SIMA stations, but this was not verified.
- Crime incidence at municipality × month level is most reliably available nationally from SESNSP. The state Fiscalía site is blocked for automated clients and probably needs a Mexican residential IP and a browser. This was not verified here.

### Gaps
- Fiscalía statistics: I could not see the latest month, the formats or the download URLs because of the 403.
- I did not find whether SINAICA publishes NL station data or any SIMA API.
- No state-level Atlas de Riesgos download (SHP or KML) was found.
- I did not check the state Secretaría de Salud's own site, IMA's GTFS plans, or Metrorrey ridership by station.

---

## 4. Civil-society and academic aggregators specific to Nuevo León

### Takeaway
**Cómo Vamos Nuevo León (CVNL)** is the most data-forward NGO. It has a public GitHub org with reproducible repos on SIMA station validity, gender violence, pedestrian and cyclist crashes, heat islands and trees, and survey microdata by manzana/AGEB. Its website mostly offers PDFs and maps. **Consejo Nuevo León** offers indicator dashboards and a security observatory but no clear bulk downloads.

### Cited Findings
- CVNL website products include the **Encuesta Así Vamos 2025** PDF (uploaded Feb 2026), **Ojos al gasto municipal** (May 2026), mayor and governor evaluations, a heat-zone research piece with map, and a parks and bike-lanes map — [comovamosnl.org](https://comovamosnl.org/); [Así Vamos 2025 PDF](https://comovamosnl.org/wp-content/uploads/2026/02/EncuestaCVNL-2025-31-marzo.pdf); [Zonas de calor](https://comovamosnl.org/investigaciones/zonas-de-calor-en-el-amm/)
- CVNL GitHub org `EvaluacionInvestigacion-CVNL` repos — [GitHub org repos API](https://api.github.com/users/EvaluacionInvestigacion-CVNL/repos):
  - `indice-monitoreo-estaciones-gcv`: SIMA station validity Oct 2025-Sep 2026; includes `cobertura_15_estaciones_monterrey_occam.csv`; pushed 2026-10-13.
  - `taller-condatos`: "Arborización estratégica para reducir islas de calor con datos satelitales - Abrelatam ConDatos 2026"; pushed 2026-10-09.
  - `dataset-violencia-genero` (2026-07-01), `mapa-hechos-peatones-y-ciclistas` (2026-07-24), `acv-validacion-arboles-zonas-calientes` (2026-05-11), `acv-territorio-posibilidad-reciclar`, `respondientes-por-manzana-ageb-distrito` (2026-07-02), `encuesta-asi-vamos-etl-pipeline`, `incidencia-corrupcion-tramites-encig`.
- Consejo Nuevo León (conl.mx) — [conl.mx](https://conl.mx/):
  - Plan Estratégico with indicator monitoring by objective ([planestrategico.conl.mx](https://planestrategico.conl.mx/indicadores/objetivos)).
  - Observatorio de Seguridad y Justicia (Q2 2026 finding, 28 Jul 2026).
  - Red de Conocimiento ([red.conl.mx](https://red.conl.mx/)).
  - 2025 impact report (17 Mar 2026).
  - A finding on drinking water and childhood obesity (30 Jun 2025).
  - Download formats are not stated.
- Tec de Monterrey: student SIMA projects (course MA2003B "Reto SIMA") use SIMA Excel files provided to the course, not public data — [reto-sima-multivariados](https://github.com/Leo-issacs/reto-sima-multivariados). A Tec team won a hackathon with a water-shortage solution — [Conecta Tec](https://conecta.tec.mx/es/noticias/monterrey/educacion/ganan-hackathon-con-solucion-al-desabasto-de-agua)

### Inferences
- CVNL's repos are probably the fastest way to get pre-cleaned NL data on safety, environment and survey topics. A hackathon team could fork them, or contact CVNL, since they are clearly active as of October 2026.

### Gaps
- FAMM (Fondo de Agua Metropolitano de Monterrey): the domains I guessed (`fondodeaguametropolitano.org`, `fondodeagua.org.mx`) did not respond from the VPS, so I did not verify its correct domain or its data (water-fund indicators, Monterrey water security plan). I also did not cover Observatorio Ciudadano de Seguridad, Redes Quinto Elemento NL investigations, UANL datasets, or the "Así Vamos" survey microdata availability.

---

## 5. The hackathon: a Monterrey hackathon around October 2026 linked to the Gobierno de Nuevo León

### Takeaway
I found **no hackathon run by the Gobierno de Nuevo León** in October 2026 and no official state data-sharing package for one. The closest matches are two community events that were **already finished** by 2026-10-14, both on **Saturday 3 Oct 2026** during **Monterrey Tech Week**. One is **"Hackathon por Nuevo León"**: an AI hackathon at Tec de Monterrey where experts presented state challenges in agua, movilidad, calidad del aire, seguridad and medio ambiente. The other is the **"Grok Monterrey Build Day / AI for Monterrey Hackathon"** (SpaceXAI, hosted by Aileen Villanueva and Monterrey Tech Week). Neither listing names specific datasets or APIs. **HackMTY 2026** (TEC ACM, "respaldado por el Gobierno de Nuevo León") has conflicting dates: 12-13 Sep or 23 Oct 2026.

### Cited Findings
- **"Hackathon por Nuevo León"**, organized by Monterrey Tech Week — [mexicohackathons.com event](https://mexicohackathons.com/events/hackathon-por-nuevo-leon); duplicate listing dated 2 Oct: [event -2](https://mexicohackathons.com/events/hackathon-por-nuevo-leon-2):
  - Saturday 3 Oct 2026, 10:00-17:00, at Aulas 6, Tec de Monterrey Campus Monterrey. Free, in person, marked FINALIZADO.
  - Description (verbatim): "Expertos en temas como agua, movilidad, calidad del aire, seguridad y medio ambiente presentarán retos del estado; posteriormente, equipos multidisciplinarios desarrollarán prototipos durante el evento utilizando herramientas de IA. El objetivo es conectar a la comunidad tecnológica con organizaciones, gobierno…"
  - Monterrey Tech Week's disclaimer (verbatim): "100% independiente, sin afiliación a partidos políticos, candidatos, escuelas ni instituciones de gobierno".
  - Registration link `lu.ma/monterrey-ezyj` now redirects to `luma.com/monterrey-ezyj` and returns **404**.
- **"Grok Monterrey Build Day — AI for Monterrey Hackathon"** — [Luma event](https://luma.com/5ohq71b3); [mexicohackathons listing](https://mexicohackathons.com/events/grok-monterrey-hackathon):
  - Presented by "SpaceXAI for Monterrey, Mexico" and hosted by **Aileen Villanueva** and **Monterrey Tech Week**. Date is 3 Oct 2026 per the directory; the Luma page does not show a date. Venue revealed only on registration.
  - Schedule: lightning talks "from civic leaders and subject matter experts", hacking from 10:45, code freeze at 17:00, awards at 18:15.
  - Tracks: Water & Sustainability; Climate & Air Quality; Smart Mobility; Public Safety; Health & Wellbeing; Education; Government Services; AI for Social Good; Open Innovation; Sponsor Challenges. Other listed areas include "open government data".
  - "Government agencies" appear only as **potential** partners. **No datasets or APIs are specified.**
  - Teams of up to 4. Finalists give a 3-minute demo plus 2 minutes of Q&A.
  - Judging criteria: technical execution, AI implementation, innovation, impact, feasibility, UX, scalability, responsible AI, presentation.
  - Prizes: "prizes, sponsor awards, cloud credits, and swag".
- Monterrey Tech Week 2026 ran 28 Sep-3 Oct with more than 100 free events, including other 3 Oct hackathons (AI Tinkerers at HUB Eduardo Garza T. Hangar 2, Hackathon Claude, Dalus, Claude Tec) — [monterreytechweek.mx](https://monterreytechweek.mx/); [mexicohackathons AI Tinkerers](https://mexicohackathons.com/events/ai-tinkerers-hackathon); [mexicohackathons index](https://mexicohackathons.com/)
- **HackMTY 2026** (TEC ACM, Arena Borregos, Tec de Monterrey):
  - One directory gives **23 Oct 2026** (48 h, 1,000+ participants, "respaldado por el Gobierno de Nuevo León y la Oficina de Convenciones y Visitantes de Monterrey", tracks sponsored by Capital One, Oracle, Banorte and GateGroup; 2025 had a "Banorte Smart Cities" track; registration at hackmty.com) — [andresospina.co](https://andresospina.co/eventos-ia/evento/hackmty-2026/)
  - Another lists it as **12-13 Sep 2026, FINALIZADO** (Devpost) — [mexicohackathons HackMTY](https://mexicohackathons.com/events/hackmty-2026)
  - The two sources conflict, and the official hackmty.com is a JS app whose static HTML showed no dates.
- AI Tinkerers Monterrey also ran a global "Agents, Everywhere" hackathon on 12 Sep 2026 — [monterrey.aitinkerers.org](https://monterrey.aitinkerers.org/)
- Upcoming Monterrey hackathons as of 2026-10-14: Polkadot University Bootcamp + Hackathon at UANL (29-31 Oct 2026) and "Revolution" (5-6 Dec 2026) — [mexicohackathons Monterrey](https://mexicohackathons.com/hackathons/monterrey)
- A national INE hackathon (Plataforma de Conteos Censales de Participación Ciudadana) closed team registration on 15 Oct 2026, with projects due 31 Oct 2026. It is not NL-specific — [INE Hackathon 2026](https://ine.mx/hackathon-2026/)
- Searches for "Hackatón Nuevo León" / "Hack NL" together with the state government or Consejo Nuevo León for Oct 2026 found no official state-run hackathon (WebSearch, 2026-10-14). State-backed innovation events in 2026 were incMTY (March) and InnovaFest — [nl.gob.mx InnovaFest bulletin](https://www.nl.gob.mx/es/boletines/invita-nuevo-leon-participar-en-innovafest-2026-para-impulsar-proyectos-de-innovacion); [Mexico Business News incMTY](https://mexicobusiness.news/trade-and-investment/news/nuevo-leon-strengthens-entrepreneurial-ecosystem-incmty-2026)
- Context to keep in mind: in Aug 2026 the Instituto de Control Vehicular NL was investigating a possible leak of about 2.4M license and 1.5M registration records offered by an actor called "Ethernal". The state had not confirmed a breach — [Récord](https://www.record.com.mx/historia/hackearon-al-gobierno-de-nuevo-leon-investigan-posible-filtracion-de-millones-de-datos-2026081316542262111). Any dataset from that leak is off-limits.

### Inferences
- "Hackathon por Nuevo León" and the "Grok/AI for Monterrey" hackathon share a date, a theme (state problems: water, air, mobility, security), Monterrey Tech Week hosting and an AI focus. They are likely the same event or two coordinated ones. The government involvement appears limited to experts presenting challenges, not formal data agreements.
- If the target hackathon is a later edition or follow-up (for example around HackMTY or a Monterrey Tech Week follow-up), teams should expect to bring their own data. The sources in sections 1-4 — the state CKAN, MIDE WFS, SIMA scraping and SADM dam levels — map directly onto those tracks (water, air, mobility, safety, health, education, government services).

### Gaps
- I could not confirm who the government-side experts were, whether any agency provided data or APIs to participants, the winners, or whether a follow-up "Hackathon por Nuevo León" is planned. The Luma page is gone and there was no press coverage in El Norte, Milenio, ABC or Posta.
- HackMTY 2026's real date and tracks are unresolved.

---

## 6. Is there a state "Agencia Digital" or digital-government unit with APIs, and any announced data-sharing agreements for hackathons?

### Takeaway
There is **no state "Agencia Digital" with a public developer API program**. Digital government sits with the **Subsecretaría de Tecnologías**, which runs the VÍA design system and the open data portal, and with the **NLínea** online-procedures window. The only real public APIs are **CKAN (catalogodatos.nl.gob.mx)** and **OCDS procurement (api-ocds.nl.gob.mx)**. I found no hackathon data-sharing agreement.

### Cited Findings
- The open data portal says it is "soportado por la Subsecretaría de Tecnologías" and links the VÍA design system (`ruta.digital.nl.gob.mx`) and `recursos.digital.nl.gob.mx` — [datosabiertos.nl.gob.mx](https://datosabiertos.nl.gob.mx/)
- **NLínea**, the digital procedures window, launched in early 2025. By late 2025 it had more than 3M catalog queries and 9k digital procedures completed, and the OECD cited it as a success case. It planned 81 digital procedures in 2026 — [nl.gob.mx docx Dec 2025](https://nl.gob.mx/sites/default/files/repositorio/Dependencias/Oficina%20Ejecutiva/Noticias/20251207_01_nl_referente_digitalizacion.docx); [Posta](https://www.posta.com.mx/nuevo-leon/nlinea-se-expande-y-estas-dependencias-seran-las-mas-beneficiadas/vl2151896)
- OGP commitment MXNLE0005 notes that only about 11% of portal datasets are disaggregated by sex or gender, and that NL scored 0.47 on the 2023 Open Government Index vs a 0.53 national average — [OGP MXNLE0005](https://www.opengovpartnership.org/es/members/nuevo-leon-state-mexico/commitments/MXNLE0005/). An earlier commitment covered dataLABNL and open-data innovation — [OGP end-of-commitment report](https://www.opengovpartnership.org/documents/end-of-commitment-report-participation-through-innovation-with-open-data-datalabnl-with-open-government/)
- The state also publishes a data-publishing guide ("guía orientadora de datos abiertos") — [nl.gob.mx](https://nl.gob.mx/guia-orientadora-de-datos-abiertos)
- INFONL's 2026 work plan sets "gobernanza abierta y digital" as an axis — [INFONL Plan 2026](https://infonl.mx/descargas/mn/PLAN_ANUAL_TRABAJO_INFONL_2026.pdf)
- Monterrey municipality: Secretaría de Innovación y Gobierno Abierto, with interoperability and data-opening guidelines and a technology governance regulation (on MIDE, 2024). The internal APIs (`*.apismty.gob.mx`, `id.api.monterrey.gob.mx`) are app backends, not documented public APIs — [MIDE API](https://mide.monterrey.gob.mx/api/v2/resources?page_size=200); [Monterrey SPA bundle](https://datos.monterrey.gob.mx/assets/index.8f76c916.js)
- A July 2025 Secretaría de Economía bulletin about FIME/UANL student talent turned up in searches tied to an "Open Source Office" announcement. I did not open or verify it — [nl.gob.mx docx](https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/Secretar%C3%ADa%20de%20Econom%C3%ADa/Noticias/20250707_04_talentos_estudiantiles_fime.docx)

### Inferences
- In practice the "API layer" for NL is three things: the state CKAN Action API, the OCDS API, and Monterrey's GeoNode REST and OGC WFS. Everything else needs scraping (SIMA, SADM), manual XLSX downloads (Escobedo, Santa Catarina), or transparency requests (Fiscalía detail, IRCNL cadastre values, historical SIMA).

### Gaps
- I could not confirm whether a state "Oficina de Código Abierto" exists or what it does, or whether any agency signed a data-sharing agreement for a 2026 hackathon. No such announcement was found.
- I did not systematically check SIPOT (Plataforma Nacional de Transparencia) obligations per municipality. For any dataset not listed above, assume a transparency request (about 10 business days or more), which does not fit a 24-48 h hackathon.
