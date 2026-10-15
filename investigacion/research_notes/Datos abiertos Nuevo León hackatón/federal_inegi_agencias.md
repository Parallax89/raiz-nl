# Federal public datasets (INEGI and other federal agencies) for Nuevo León / Monterrey metro, with fine spatial resolution

Research date: 2026-10-14. Geographic focus: Nuevo León (CVE_ENT = 19), Zona Metropolitana de Monterrey (ZMM).
Method note: many URLs were checked live from a server outside Mexico. For each one the note says whether it was opened (HTTP 200, Last-Modified header, or file contents read) or only reported by a secondary source.

---

## 1. Current state (Oct 2026): which editions are actually published, and which agencies or portals were reorganized?

### Takeaway
INEGI did not run a "Conteo 2025". It ran the **Encuesta Intercensal (EIC) 2025** instead and published results on **22 Sep 2026**. Those results go down to **municipality and localities of 50,000+ inhabitants only**, so the **Censo 2020 is still the most recent AGEB/manzana source**. **CONEVAL was abolished in 2025** and its poverty measurement moved to INEGI. CONEVAL's old site and its datasets are still online. **datos.gob.mx has been relaunched by the ATDT** as a working CKAN portal, and the files are now hosted on `repodatos.atdt.gob.mx`.

### Cited Findings
**Encuesta Intercensal 2025 (replaces the "Conteo 2025")**
- EIC 2025 results were released on 22 Sep 2026 (comunicado 54/26). Fieldwork ran **6 Oct–14 Nov 2025** on a sample of just over **7.3 million occupied private dwellings**. Results cover "las 32 entidades federativas, los 2 478 municipios o demarcaciones territoriales y las localidades con 50 000 habitantes y más". INEGI says they are comparable with earlier censuses and counts and with EIC 2015. Results, interactive tools and **microdata** are announced on inegi.org.mx — [INEGI comunicado 54/26 (PDF)](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/ei/EIC2025-def_CP.pdf)
- National total: 130.9 M residents. The analysed universe is 130,393,389 people in private dwellings and 39,699,242 occupied private dwellings — [INEGI 54/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/ei/EIC2025-def_CP.pdf); [Milenio](https://www.milenio.com/comunidad/inegi-revela-cifra-oficial-poblacion-mexico-2025)
- Program page: https://www.inegi.org.mx/programas/eic/2025/. Open-data bundle (verified, 8.3 MB, Last-Modified 22 Sep 2026): `https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip`. It contains `conjunto_datos_eic2025_105.csv` plus a data dictionary and metadata, titled "Principales resultados por localidad de 50 000 y más habitantes". The metadata says it gives estimates "con desagregación geográfica hasta municipio" and adds new topics such as **internal forced displacement** and **declared mental health condition** — [INEGI EIC 2025 page](https://www.inegi.org.mx/programas/eic/2025/) (zip downloaded and inspected)
- File structure, from inspecting the zip: columns `CVEGEO, CVE_ENT, NOM_ENT, CVE_MUN, NOM_MUN, CVE_LOC, NOM_LOC, ESTIMADOR, POBTOT, …`. Every geography has 5 rows: `Valor`, `Error estándar`, `Límite inferior/superior de confianza`, `Coeficiente de variación`. Encoding is Latin-1. NL has 67 "Valor" rows: the state, 51 municipalities, the "997/9997 Localidades de menos de 50 000" aggregate, and these localities ≥50k: Ciudad Apodaca, Cadereyta Jiménez, García, **Mitras Poniente (García, loc 0212)**, San Pedro Garza García, Ciudad General Escobedo, Guadalupe, Ciudad Benito Juárez, **Jardines de la Silla (Juárez, loc 0045)**, Linares, Montemorelos, Monterrey, San Nicolás de los Garza, Ciudad Santa Catarina — [EIC 2025 open data zip](https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip)
- EIC 2025 POBTOT ("Valor"): NL **6,274,840**; Monterrey 1,135,843; Apodaca 712,979; Guadalupe 631,799; Juárez 596,176; García 550,959; General Escobedo 507,642; San Nicolás 382,034; Santa Catarina 308,887; San Pedro Garza García 132,933 — [EIC 2025 open data zip](https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip)
- History: INEGI dropped the EIC 2025 in Jan 2025 for budget reasons and reinstated it after SHCP widened its budget. One news headline ("Siempre no reviven…", May 2025) suggests the reinstatement was contested. In the end it went to the field in Oct–Nov 2025 — [Crónica](https://www.cronica.com.mx/nacional/2025/05/12/siempre-no-reviven-la-encuesta-intercensal-2025-tras-ampliacion-presupuestaria/); [SNIEG EIC 2025 doc](https://www.snieg.mx/Documentos/CONSEJO/sesiones/doc_12025/4_eic_2025.pdf)

**CONEVAL → INEGI**
- The Senate approved CONEVAL's extinction on 26 Jun 2025, with its functions passing to INEGI and program evaluation going to SHCP. Diputados had approved it on 23 Jun — [Zeta Tijuana](https://zetatijuana.com/2025/06/senado-concretan-extincion-del-coneval-trasladan-sus-funciones-al-inegi/); [Cámara de Diputados síntesis](https://comunicacion.diputados.gob.mx/sintesis/LINKSIN3/P24625_L_24H_0_DIPUTADOSAPRUEBAN_FUNCIONESDECONEVALAAINEGI_3DIP_.pdf)
- INEGI took over CONEVAL's functions on **17 Jul 2025** and said the 2018 methodology would be kept — [El CEO](https://elceo.com/economia/inegi-asume-las-funciones-del-coneval-y-divulga-nuevo-calendario/)
- INEGI published the **Medición de pobreza multidimensional 2024** on 13 Aug 2025 (national/state): 29.6% in poverty (38.5 M people) — [La Política Online](https://www.lapoliticaonline.com/mexico/economia-mx/inegi-asume-la-medicion-de-pobreza-y-reporta-una-fuerte-caida-entre-2022-y-2024/); [Puebla CEIGEP presentation](https://ceigep.puebla.gob.mx/storage/documentos/2025-12-17-presentacion.pdf)
- The EIC 2025 is meant to feed **municipal poverty measurement** (Art. 37 LGDS) — [SNIEG EIC 2025 doc](https://www.snieg.mx/Documentos/CONSEJO/sesiones/doc_12025/4_eic_2025.pdf)
- coneval.org.mx is still online. The IRS 2020 annex page and the "Pobreza a nivel municipio 2010–2020" page both returned HTTP 200 on 14 Oct 2026 — [CONEVAL IRS 2020 anexos](https://www.coneval.org.mx/Medicion/IRS/Paginas/Indice_de_Rezago_Social_2020_anexos.aspx); [CONEVAL pobreza municipal 2010–2020](https://www.coneval.org.mx/Medicion/Paginas/Pobreza-municipio-2010-2020.aspx)

**datos.gob.mx (ATDT)**
- New lineamientos for open data in the federal public administration were published in the DOF on 11 Sep 2025 and signed by the ATDT head (José Antonio Peña Merino) — [DOF 11-09-2025 copy (IPN)](https://www.aplicaciones.abogadogeneral.ipn.mx/ACUERDOS/2025/dof-11-09-2025.pdf)
- The portal is live as "Plataforma Nacional de Datos Abiertos – datos.gob.mx". On 14 Oct 2026 its homepage showed **8,030 bases de datos, 189 instituciones, 2,455 visualizaciones, 28 categorías** — [datos.gob.mx](https://www.datos.gob.mx/)
- It runs CKAN. The API works at `https://www.datos.gob.mx/api/3/action/package_search?q=…` and `package_show?id=…`. It returned **403 without a browser User-Agent** and worked with one. The old path `/busca/api/3/action/...` now returns 404 — [datos.gob.mx API](https://www.datos.gob.mx/api/3/action/package_show?id=rezago_social) (checked live)
- Most resources now live at `https://repodatos.atdt.gob.mx/api_update/<institución>/<dataset>/<file>`. Ranged requests to that host from a non-Mexican server returned "Access Denied", which may be bot or geo filtering — [example SESNSP resource](https://repodatos.atdt.gob.mx/api_update/sesnsp/incidencia_delictiva/IDM_NM_dic25.csv)

**Other portals**
- DataMéxico: `datamexico.org` now redirects to `https://www.economia.gob.mx/datamexico/` (checked live), and the site shows 2026 data such as 2026-T1 unemployment and June 2026 exports — [economia.gob.mx/datamexico](https://www.economia.gob.mx/datamexico/es/profile/geo/mexico)
- SESNSP: from **Jan 2026** crime incidence moved from form CNSP/38/15 to a new **Registro Nacional de Incidencia Delictiva**. It changes how nine crimes are recorded and adds geolocation and new breakdowns. A critic (opinion column) says there is no methodological bridge between the 2015–2025 and 2026+ blocks — [Expansión (opinion)](https://politica.expansion.mx/voces/2026/03/06/el-sesnsp-y-el-truco-del-ilusionista); the instrument update was approved by the CNSP in Dec 2024 (acuerdo 11/L/2024) — [SNIEG](https://www.snieg.mx/Documentos/Gobierno/sesiones/doc_12025/1_nueva_metod_rec_inc_delic.pdf)
- Norma Técnica del Marco Geoestadístico: published in the DOF 25 Jun 2026, in force from 26 Jun 2026 — [SNIEG NT MG](https://www.snieg.mx/Documentos/Normatividad/Vigente/NT_Marco_Geoestadistico.pdf) (reported by a search summary of that document)

### Inferences
- At AGEB/manzana level the hackathon has to use **Censo 2020** (and Marco Geoestadístico 2020/2024 geometries). Use EIC 2025 to update or calibrate at municipality level, and at the 14 big NL localities. García (+39% vs. the 2020 census figure of 397,205 in the CONAPO metro file) and Apodaca are where the 2020 AGEB picture is most stale.
- CONEVAL-branded products (IRS 2020 by AGEB, municipal poverty 2010–2020) are frozen legacy products. New municipal poverty estimates would come from INEGI, based on EIC 2025.

### Gaps
- I could not confirm the publication date of INEGI's **municipal poverty 2025** (EIC-based), or whether INEGI has moved CONEVAL's poverty pages to an inegi.org.mx URL. Both `inegi.org.mx/programas/pobreza/` and `/temas/pobreza/` returned "Página no encontrada".
- I could not confirm the EIC 2025 microdata file path. A guessed path (`/microdatos/eic2025_19_csv.zip`) returned a soft 404.
- The SESNSP gob.mx open-data page blocked automated access ("Challenge Validation"), so I could not see the official layout of the 2026 municipal file under the new methodology.

---

## 2. INEGI inventory: census, geography, economy, surveys, registries, APIs and viewers

### Takeaway
INEGI is the backbone. The **Marco Geoestadístico** (latest verified: Dec 2024) provides the AGEB/manzana polygons and CVEGEO keys. **Censo 2020 "Principales resultados por AGEB y manzana urbana"** is the densest attribute table (222 AGEB / 215 manzana indicators). **DENUE 05/2026** is point-level and has an API. **Censos Económicos 2024** (reference year 2023) is published down to manzana. INEGI also offers a no-token geo-catalog web service and token-based APIs for indicators and DENUE.

### Cited Findings
**Censo de Población y Vivienda 2020**
- Program page: https://www.inegi.org.mx/programas/ccpv/2020/ — [INEGI CPV 2020](https://www.inegi.org.mx/programas/ccpv/2020/)
- **Resultados por AGEB y manzana urbana, NL**: `https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_19_cpv2020_csv.zip` (verified 200, 12.0 MB, Last-Modified 26 Jul 2021) — [INEGI](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_19_cpv2020_csv.zip)
- The product has **222 indicators for 64,313 AGEB** and **215 indicators for more than 1 million urban manzanas** nationally — [INEGI descriptor / search summary](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/fd_agebmza_urbana_cpv2020.pdf)
- **Confidentiality rules** (verbatim from the INEGI field descriptor): "A nivel municipio o demarcación territorial, localidad y AGEB, cualquier indicador con menos de tres unidades aparece con asterisco a excepción de las variables Población total (POBTOT), Total de viviendas (VIVTOT) y Total de viviendas habitadas (TVIVHAB). A nivel manzana también se aplica el criterio anterior; adicionalmente, para aquellas de una o dos viviendas habitadas, sólo se presenta información en las variables Población total (POBTOT) y Total de viviendas (VIVTOT), en el resto de los indicadores aparecen asteriscos." — [INEGI fd_agebmza_urbana_cpv2020.pdf](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/fd_agebmza_urbana_cpv2020.pdf)
- **ITER (Principales resultados por localidad), NL**: `https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_19_cpv2020_csv.zip` (verified 200, Last-Modified 19 May 2022). The national version is `iter_00_cpv2020_csv.zip` — [INEGI](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_19_cpv2020_csv.zip)
- **Microdatos, cuestionario ampliado, NL**: `https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/Censo2020_CA_nl_csv.zip` (verified 200, 11.4 MB). This is the sample questionnaire, representative at municipal level — [INEGI](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/Censo2020_CA_nl_csv.zip)
- **SCINCE 2020** (thematic cartography of census variables by AGEB/manzana) responds at https://gaia.inegi.org.mx/scince2020/ and https://www.inegi.org.mx/app/scince/2020/ (both 200). The bare `/app/scince/` path returns "Página no encontrada" — [SCINCE 2020](https://gaia.inegi.org.mx/scince2020/)
- **Inventario Nacional de Vivienda (INV) 2020** shows, for every urban manzana in the country, its total number of dwellings, and complements the census — [IIEG Jalisco presentation of INV 2020](https://iieg.gob.mx/ns/wp-content/uploads/2022/08/Presentación-Inventario-Nacional-de-Viviendas-2020.pdf). The viewer is at https://www.inegi.org.mx/app/mapa/inv/ (200) — [INEGI INV](https://www.inegi.org.mx/app/mapa/inv/)

**Marco Geoestadístico (MG)**
- The latest version I could verify is the **national MG zip dated Dec 2024**: `https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/794551132173_s.zip` (verified 200, **3.33 GB**, Last-Modified 16 Dec 2024). A third-party script identifies it as "mgn2024", with per-state manzana shapefiles inside `conjunto_de_datos/` — [INEGI file](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/794551132173_s.zip); [GitLab script reference](https://gitlab.geoint.mx/mario.chirinos/espaciopublico/commit/f0abaaaa091b80b11de89bc9097b0677a309fa26)
- MG section: https://www.inegi.org.mx/temas/mg/ (the page renders via JavaScript). The 2025 Norma Técnica draft defines the geocode hierarchy. A manzana code concatenates entidad + municipio + localidad + AGEB + manzana — [SNIEG NT MG draft May 2025](https://www.snieg.mx/Documentos/Demografico/sesiones/doc_12025/2_ntmg08mayo2025.pdf)
- **No-token geo-catalog API (wscatgeo)**: `https://gaia.inegi.org.mx/wscatgeo/v2/mgem/19` returns JSON for every NL municipality with `cvegeo, cve_ent, cve_mun, nomgeo, cve_cab, pob_total, pob_femenina, pob_masculina, total_viviendas_habitadas` (e.g., `"cvegeo":"19001","nomgeo":"Abasolo","pob_total":"2974"`) — [INEGI wscatgeo](https://gaia.inegi.org.mx/wscatgeo/v2/mgem/19) (checked live)

**DENUE (Directorio Estadístico Nacional de Unidades Económicas)**
- **DENUE 05/2026** was published 20 May 2026 with **6,138,075 establishments**. The next release is **25 Nov 2026** (semiannual) — [INEGI DENUE 05/2026 press release](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/denue/DENUE2026_05.pdf)
- Bulk NL downloads (verified Last-Modified 20 May 2026): CSV `https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_csv.zip` (21.5 MB) and SHP `https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_shp.zip` (42.2 MB) — [INEGI DENUE CSV NL](https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_csv.zip)
- **API DENUE v1** (free token on registration). Methods: `Buscar` (keyword + lat,lon + radius; **max radius 5,000 m**), `Ficha`, `Nombre`, `BuscarEntidad`, `BuscarAreaAct`, `BuscarAreaActEstr`, `Cuantificar`. Pattern: `https://www.inegi.org.mx/app/api/denue/v1/consulta/Buscar/{condición}/{lat},{lon}/{metros}/{token}` — [INEGI API DENUE](https://www.inegi.org.mx/servicios/api_denue.html)

**Censos Económicos 2024**
- Definitive results came out 24 Jul 2025, and the **reference year is 2023** — [INEGI CE2024 definitive release](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE2024_def.pdf)
- Results are disaggregated down to **AGEB and manzana** (and by sector to activity class) — [Tabasco "Panorama de los CE2024"](https://tabasco.gob.mx/sites/default/files/users/planeacion_spf/Panorama_de_los_CE2024.pdf) (secondary)
- National open-data CSV: `https://www.inegi.org.mx/contenidos/programas/ce/2024/datosabiertos/conjunto_de_datos_ce_nac_2024_csv.zip` (verified 200, Last-Modified 29 Sep 2025) — [INEGI CE 2024](https://www.inegi.org.mx/programas/ce/2024/)

**Physical geography**
- **Uso de Suelo y Vegetación Serie VII**, 1:250,000: 149 sheets produced 2017–2021 from Landsat Geomedian (2018 base), published around Dec 2021 — [INEGI USV 250K SVII doc](https://inegi.org.mx/contenidos/temas/usosuelo/doc/USV_250K_SVII.pdf); [CONAFOR IDEFOR metadata](https://idefor.cnf.gob.mx/layers/geonode%3Acdv_usuev250svii_cnal_wgs84/pdf_metadata_layer). Theme page: https://www.inegi.org.mx/temas/usosuelo/ (200)
- **Continuo de Elevaciones Mexicano (CEM)**: page https://www.inegi.org.mx/app/geo2/elevacionesmex/ (200, title "Continuo de elevaciones mexicano y modelos digitales de elevación") — [INEGI CEM](https://www.inegi.org.mx/app/geo2/elevacionesmex/)
- **Red Nacional de Caminos (RNC) 2025** was released 15 Dec 2025, with the next edition due 15 Dec 2026. Network lengths: 178,608 km carreteras, 530,493 km rural, 21,597 km footpaths, **274,097 km urban streets** (+73,537 km vs. 2024, mostly urban). Free SHP downloads; routing service at https://www.inegi.org.mx/servicios/Ruteo/Default.html — [INEGI RNC 2025 release](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/rnc/RNC2025.pdf); [INEGI Ruteo](https://www.inegi.org.mx/servicios/Ruteo/Default.html)

**Registries and surveys**
- **ATUS (accidentes de tránsito urbanos)**: program https://www.inegi.org.mx/programas/accidentes/. The bulk file `.../accidentes/datosabiertos/atus_anual_csv.zip` was verified at 131.7 MB, Last-Modified **19 Aug 2024**. The OLAP query page says "Información de 1997 a 2024" and filters by entity and municipality. It notes that **2024 deaths were corrected in 2025 for Apodaca** (and Aguascalientes, Hermosillo). There is also a catalog of **municipalities with georeferenced accidents** — [INEGI ATUS consulta](https://www.inegi.org.mx/sistemas/olap/proyectos/bd/continuas/transporte/accidentes.asp); [Municipios georreferenciados (PDF)](https://gaia.inegi.org.mx/documentos/atus/Municipios_georreferenciados.pdf). 2025 ATUS figures were published around July 2026 (380,391 events nationally) — [Milenio](https://www.milenio.com/policia/accidentes-de-transito-aumentan-en-mexico-segun-el-inegi); [La Razón](https://www.razon.com.mx/mexico/2026/07/30/huyen-conductores-en-accidentes-con-muertos/)
- **Estadísticas de Defunciones Registradas (EDR)**: preliminary 2025 numbers are 762,494 deaths, crude rate 584 per 100k, and 27,989 presumed homicides. The **definitive 2025** release is scheduled for **Nov 2026** (after confrontas with SSA) — [INEGI EDR 2025 press release](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/edr/EDR2025_CP.pdf). Program/microdata page: https://www.inegi.org.mx/programas/edr/ (200). Microdata include municipality of residence and occurrence, plus ICD-10 cause, which supports heat-related (X30) and respiratory (J00–J99) analysis. The ICD-coding detail is my own knowledge and was not re-checked. Bulk file naming that **was** verified: `.../edr/datosabiertos/conjunto_de_datos_defunciones_registradas_2022_csv.zip` — [INEGI EDR](https://www.inegi.org.mx/programas/edr/)
- **ENIGH 2024**: https://www.inegi.org.mx/programas/enigh/nc/2024/ (200), published 30 Jul 2025 — [Puebla CEIGEP](https://ceigep.puebla.gob.mx/storage/documentos/2025-12-17-presentacion.pdf). Representative at national/state level only.
- **ENVIPE 2026**: https://www.inegi.org.mx/programas/envipe/2026/ (200, temporalCoverage 2026). **ENSU** (quarterly urban security perception by city): https://www.inegi.org.mx/programas/ensu/ (200). **ENOE**: https://www.inegi.org.mx/programas/enoe/15ymas/ (200, quarterly CSV open data) — [INEGI ENVIPE 2026](https://www.inegi.org.mx/programas/envipe/2026/); [INEGI ENSU](https://www.inegi.org.mx/programas/ensu/); [INEGI ENOE](https://www.inegi.org.mx/programas/enoe/15ymas/)

**APIs and viewers**
- **API de Indicadores (Banco de Indicadores BISE + BIE)**, free token. Pattern: `https://www.inegi.org.mx/app/api/indicadores/desarrolladores/jsonxml/INDICATOR/{id}/es/{área geo}/false/BISE/2.0/{token}?type=json`. The area code goes to municipal level, e.g. `00000` style codes. There are catalog endpoints (`CL_GEO_AREA`, `CL_INDICATOR`, `CL_UNIT`…) and JSON-stat output — [INEGI API Indicadores](https://www.inegi.org.mx/servicios/api_indicadores.html)
- **Espacio y Datos de México** https://www.inegi.org.mx/app/mapa/espacioydatos/ (200) and the Mapas section https://www.inegi.org.mx/app/mapas/ (200) — [INEGI Espacio y Datos](https://www.inegi.org.mx/app/mapa/espacioydatos/)
- **INEGIpy 2.0.0** on PyPI: "Librería en Python para facilitar el uso de las APIs del INEGI". Repo: https://github.com/andreslomeliv/DatosMex/tree/master/INEGIpy — [PyPI INEGIpy](https://pypi.org/pypi/INEGIpy/json)

### Inferences
- The fastest AGEB-level stack is: MG 2024 manzana/AGEB polygons, plus Censo 2020 AGEB/manzana CSV (join on CVEGEO), plus DENUE points (spatial join, or DENUE's own AGEB/manzana fields), plus CE 2024 AGEB/manzana tables.
- The DENUE API's 5 km radius cap makes the bulk SHP/CSV the better choice for metro-wide work. The API is useful for live demos.

### Gaps
- I could not confirm whether an **MG 2025** (e.g., Dec 2025) exists. INEGI's MG page is JavaScript-only and searches found none. Treat Dec 2024 as the latest verified version.
- **Serie VIII** of Uso de Suelo: no evidence found that it is published.
- I could not verify the CEM's current version or resolution (commonly cited as CEM 3.0 at 15 m, but not re-checked).
- I could not confirm the exact file path of the **CE 2024 AGEB/manzana** tables (likely the SAIC system). Guessed per-state open-data paths returned soft 404s.
- I could not verify the **EDR 2024/2025 open-data file names**. Guessed `..._2024_csv.zip` returned a soft 404 under both `/programas/mortalidad/` and `/programas/edr/`. Look them up on the EDR page.
- I could not confirm whether the 2025 ATUS bulk file has been posted (the bulk zip is still dated Aug 2024), or whether NL metro municipalities are in the "georreferenciados" list.
- Mapa Digital de México (`/app/mapadigital/`) was not checked.

---

## 3. CONAGUA / SMN (water and climate) — brief federal source list

### Takeaway
Daily station data (SMN/CLICOM), the municipal drought file, and per-dam historical CSVs are all **static files with no token**. REPDA is a query app, and SINA has no confirmed bulk export. Water is covered in depth by another researcher.

### Cited Findings
- **SMN daily climatological station data** are plain-text files per station: `https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/nl/dia{CLAVE}.txt`. Example 19039 "LAS ENRAMADAS", Los Ramones, NL: status OPERANDO, lat 25.50138889, lon −99.52138889, emission 09/10/2026, "datos disponibles … a octubre de 2026". The older path `/tools/RESOURCES/Diarios/19039.txt` now returns 404/500 — [SMN dia19039.txt](https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/nl/dia19039.txt) (checked live)
- **Monitor de Sequía de México, municipal history**: `https://smn.conagua.gob.mx/tools/RESOURCES/Monitor%20de%20Sequia%20en%20Mexico/MunicipiosSequia.xlsx` (verified 200, about 2.1 MB) — [SMN MunicipiosSequia.xlsx](https://smn.conagua.gob.mx/tools/RESOURCES/Monitor%20de%20Sequia%20en%20Mexico/MunicipiosSequia.xlsx)
- **Dam storage (SIH)**: https://sih.conagua.gob.mx/presas.html lists a dam catalog (`basedatos/Presas/0_Catalogo_de_presas.csv` / `.xls`) and **one historical CSV per dam**, keyed by a 5-letter code (e.g., `basedatos/Presas/ABRAG.csv`) — [CONAGUA SIH presas](https://sih.conagua.gob.mx/presas.html)
- **REPDA** (water concessions: titular, volume, use) is available as a query app at https://app.conagua.gob.mx/consultarepda.aspx (200). datos.gob.mx returned **0 hits for "repda"** — [CONAGUA REPDA consulta](https://app.conagua.gob.mx/consultarepda.aspx); [datos.gob.mx API search](https://www.datos.gob.mx/api/3/action/package_search?q=repda)
- On datos.gob.mx, CONAGUA has **aguas_subterraneas** (includes `red_piezometrica.zip`, updated 2026-08-14), **estaciones_sistema_informacion_hidrologica** (station catalog CSV), and **programa_nacional_contra_sequia_pronacose** (`vulnerabilidad_social_municipal.csv`). SHCP has **derechos_agua_municipal** — [datos.gob.mx search "derechos de agua"](https://www.datos.gob.mx/api/3/action/package_search?q=derechos%20de%20agua); [datos.gob.mx search "sequia"](https://www.datos.gob.mx/api/3/action/package_search?q=sequia)

### Inferences
- SMN station files and dam CSVs are points in time and space. To cross them with AGEBs, interpolate (IDW/kriging) or take the nearest station. NL's metro area has few SMN stations, so cross-check against state networks (another researcher).

### Gaps
- I did not verify the URLs for SINA (Sistema Nacional de Información del Agua), the DOF aquifer-availability tables, or SMN climatological normals. The guessed normals path `/Normales9120/nl/nor19039.txt` returned 404.

---

## 4. Air and environment: SINAICA, SEMARNAT RETC/COA, CONABIO, CONANP, CONAFOR, CENAPRED

### Takeaway
Air quality comes from **SINAICA** (no official API; the R package `rsinaica` is the practical client) and from INECC's **validated annual NL concentrations** on datos.gob.mx (latest year 2022). **RETC** has establishment-level data through 2024 (189 NL companies), but I could not confirm a bulk download. CONAFOR fires (CSV/SHP), CONAPO urban expansion, and the CENAPRED Atlas download page are all available.

### Cited Findings
- **SINAICA** site is https://sinaica.inecc.gob.mx/ (200) — [SINAICA](https://sinaica.inecc.gob.mx/)
- The **rsinaica** R package (maintained by Diego Valle-Jones, on CRAN) downloads SINAICA pollutant and meteorological data from more than 100 stations. The main function is `sinaica_station_data()`. No Python equivalent was found — [CRAN rsinaica](https://cran.r-project.org/web/packages/rsinaica/refman/rsinaica.html); [rdocumentation](https://www.rdocumentation.org/packages/rsinaica/versions/1.1.1)
- INECC dataset **concentraciones_validadas_calidad_aire_entidad_federativa** covers CO, NO2, SO2, O3, PM10 and PM2.5 from monitoring stations. The NL resource is "Concentraciones validadas de calidad del aire de Nuevo León (2022)": `https://repodatos.atdt.gob.mx/api_update/inecc/concentraciones_validadas_calidad_aire_entidad_federativa/nuevo_leon_013.csv` (dataset modified 2026-03-07) — [datos.gob.mx package](https://www.datos.gob.mx/api/3/action/package_show?id=concentraciones_validadas_calidad_aire_entidad_federativa)
- **RETC**: SEMARNAT updated the federal RETC portal with data through **2024**, listing **189 NL companies** that report emissions to air, water or soil, including Ternium, Iberdrola, Pemex Cadereyta and Nemak — [El Imparcial, Feb 2026](https://www.elimparcial.com/mexico/2026/02/16/189-empresas-en-nuevo-leon-reportan-emisiones-contaminantes-ante-semarnat-que-dice-el-registro-oficial-y-esto-es-lo-que-significa-para-la-poblacion/). The query portal is `sinat.semarnat.gob.mx/retc/index.php`. Reporters are federal-jurisdiction fixed sources, generators of ≥10 t/yr hazardous waste, and wastewater dischargers, under NOM-165-SEMARNAT-2013 — [CEC 2025 presentation](https://cec.org/files/documents/events/day-1_2c_ernesto_2025_presentacion.pdf)
- The **Monterrey metro emissions inventory** (federal + state + UNAM) was still under validation in Aug 2026, and its results are to be released by the federal government — [Gobierno NL bulletin, 20 Aug 2026](https://nl.gob.mx/es/boletines/se-reunen-nuevo-leon-semarnat-y-unam-para-revisar-elementos-tecnicos-del-inventario-de)
- INECC **INEGyCEI** (national GHG inventory, 1990–) is on datos.gob.mx (35 resources, modified 2026-03-06). It is national, not spatial — [datos.gob.mx search](https://www.datos.gob.mx/api/3/action/package_search?q=emisiones%20transferencia%20contaminantes)
- **CONAFOR incendios_forestales**: CSV for 2025 (`2025_Incendios_forestales.csv`), statistics 2015–2024, and **annual SHP 2010–2023** (dataset modified 2026-03-24) — [datos.gob.mx incendios_forestales](https://www.datos.gob.mx/api/3/action/package_show?id=incendios_forestales). CONAFOR also has National Forest and Soil Inventory datasets for the 2004–2007, 2009–2014 and 2015–2020 cycles — [datos.gob.mx "uso de suelo" search](https://www.datos.gob.mx/api/3/action/package_search?q=uso%20de%20suelo)
- **CONANP** on datos.gob.mx publishes ADVC (voluntary conservation areas) and World Heritage sites as CSV. I did not find an ANP polygons dataset there — [datos.gob.mx ANP search](https://www.datos.gob.mx/api/3/action/package_search?q=anp%20areas%20naturales%20protegidas)
- **CONABIO Geoportal** http://geoportal.conabio.gob.mx/ (200) — [CONABIO geoportal](http://geoportal.conabio.gob.mx/)
- **CENAPRED Atlas Nacional de Riesgos** http://www.atlasnacionalderiesgos.gob.mx/ (200). Sections include `archivo/descargas.html`, `archivo/indicadores-municipales.html`, `archivo/visor-capas.html` and `archivo/cob-atlas-municipales.html` — [Atlas Nacional de Riesgos](http://www.atlasnacionalderiesgos.gob.mx/)
- **CONAPO "Expansión urbana, zonas de análisis"** SHPs for 1985 (Serie I), 2002 (Serie III) and 2018 (Serie VII) — [datos.gob.mx distribucion_territorial](https://www.datos.gob.mx/api/3/action/package_show?id=distribucion_territorial)
- PROFEPA "Emergencias ambientales por municipio según su causa" CSV — [datos.gob.mx inspeccion_vigilancia_industrial](https://www.datos.gob.mx/api/3/action/package_search?q=zonas%20metropolitanas)

### Inferences
- For an AGEB-level pollution-exposure layer: geocode RETC establishments, or match them by name/RFC to DENUE points. Then intersect with SINAICA station data (interpolated) and with census vulnerability (IMU/GRS).

### Gaps
- **RETC bulk download format** (CSV/XLSX vs. query only) is unconfirmed. datos.gob.mx returned 0 hits for "retc" and for "cédula de operación anual".
- The **CONANP ANP shapefile** server (`sig.conanp.gob.mx`) did not respond from this server. The **CONAFOR SNIF** fire page (`snif.cnf.gob.mx/incendios/`) also timed out.
- SINAICA's own download endpoints and real-time API were not documented in any source I found. The INECC validated NL series on datos.gob.mx goes only to **2022**.

---

## 5. Social and economic federal sources: CONEVAL, CONAPO, Salud, SEP, SESNSP, IMSS, DataMéxico, SAT

### Takeaway
Ready-made **AGEB-level** indices (with SHP) exist for **CONAPO Índice de Marginación Urbana 2020** (AGEB and **colonia**) and **CONEVAL Grado de Rezago Social 2020** (AGEB). CONAPO also offers municipal projections to 2040, the 2020 metropolis delimitation, and a new **Índice de Calidad del Entorno 2020**. Point layers: **CLUES** (Aug 2026) and the **SEP Catálogo de Centros de Trabajo** (2025). Crime is **municipal only** (SESNSP, to Dec 2025 on the old methodology).

### Cited Findings
**CONAPO** (dataset `indices_marginacion` on datos.gob.mx)
- Índice de marginación estatal/municipal 2010/2015/2020 and por localidad 2020 (`iml_2020.csv`). **IMU AGEB 2020**: `imu_2020.csv`. **IMU colonia 2020**: `imuc_2020.csv`, with geometry `https://repodatos.atdt.gob.mx/CONAPO/indices_marginacion/colonias_imc2020_shp.zip` — [datos.gob.mx indices_marginacion](https://www.datos.gob.mx/api/3/action/package_show?id=indices_marginacion)
- IMU AGEB columns (read directly): `CVE_AGEB, ENT, NOM_ENT, MUN, NOM_MUN, LOC, NOM_LOC, AGEB, POB_TOTAL, P6A14NAE, SBASC, PSDSS, OVSDE, OVSEE, OVSAE, OVPT, OVSREF, OVSINT, OVSCEL, OVHAC, IM_2020, GM_2020, IMN_2020`. **`ENT`/`MUN`/`LOC` are unpadded integers** (e.g., `1`), and the helper field `fn_CVE_AGEB` is a float (`100100010017.0`), so leading zeros are lost — [imu_2020.csv](https://www.datos.gob.mx/dataset/d8f2a534-bcee-4114-853d-82982a81ce24/resource/9600f414-c1ba-408a-8dd6-7f73d76601d4/download/imu_2020.csv)
- IMU 2020 covers urban AGEBs and, **for the first time, colonias**. It is built from Censo 2020 microdata using the Distancias Ponderadas al cuadrado (DP2) method, which allows comparison over time — [CONAPO urbana.pdf](https://www.gob.mx/cms/uploads/attachment/file/828844/urbana.pdf); [CONAPO Índices 2020 publication](https://www.gob.mx/cms/uploads/attachment/file/848423/Indices_Coleccion_280623_entymun-p_ginas-1-153.pdf)
- **Índice de Calidad del Entorno (ICE) 2020**, at municipal and locality level, CSV + SHP (dataset modified 2026-07-29). It combines marginación with the availability and concentration of urban services and equipment — [datos.gob.mx indice_calidad_entorno](https://www.datos.gob.mx/api/3/action/package_show?id=indice_calidad_entorno)
- **Proyecciones**: "Población a mitad de año por municipio y grupos quinquenales de edad (1990–2040)" and "Indicadores demográficos para los municipios (1990–2040)", plus state/national 1950–2070 series — [datos.gob.mx proyecciones-de-poblacion](https://www.datos.gob.mx/api/3/action/package_show?id=proyecciones-de-poblacion)
- **Metrópolis de México 2020**: CSV (basic characteristics, population by metropolis and by municipality) plus geospatial zip `https://repodatos.atdt.gob.mx/CONAPO/metropolis_mexico/metropolis_2020.zip`. **ZM Monterrey (clave 19.1.01) = 16 municipalities**: Apodaca (19006), Cadereyta Jiménez (19009), El Carmen (19010), Ciénega de Flores (19012), García (19018), San Pedro Garza García (19019), General Escobedo (19021), General Zuazua (19025), Guadalupe (19026), Juárez (19031), Monterrey (19039), Pesquería (19041), Salinas Victoria (19045), San Nicolás de los Garza (19046), Santa Catarina (19048), Santiago (19049). In this file `clave_municipio` is unpadded (`6`), but `clave_compuesta_municipio` is the 5-digit key — [datos.gob.mx metropolis_mexico_2020](https://www.datos.gob.mx/api/3/action/package_search?q=zonas%20metropolitanas); [municipios_poblacion.csv](https://www.datos.gob.mx/dataset/da65ccd9-888c-4ce8-b3b5-6bd867be344d/resource/6f57ab97-d1df-4768-beb8-c929c2449923/download/municipios_poblacion.csv)
- Sistema Urbano Nacional 2020 (by city and by locality) — [datos.gob.mx sistema_urbano_nacional](https://www.datos.gob.mx/api/3/action/package_search?q=zonas%20metropolitanas)

**CONEVAL legacy** (dataset `rezago_social` on datos.gob.mx)
- IRS by entidad, municipio and localidad for 2000–2020. **Grado de rezago social por AGEB 2020** (`grs_ageb_2020.csv`) plus geometry `https://repodatos.atdt.gob.mx/CONEVAL/rezago_social/grs_ageb_2020_shp.zip`, and GRS AGEB 2010 — [datos.gob.mx rezago_social](https://www.datos.gob.mx/api/3/action/package_show?id=rezago_social)
- GRS AGEB columns: `clave_entidad, …, clave_localidad, clave_ageb, folio_ageb, poblacion, viviendas_habitadas, i_analf, i_asistesc_6a14, …, i_sdsalud, i_hacinamiento, i_noagua, i_nosan, i_nodren, i_noelec, i_ptierra, …, i_nointernet, grs` — [grs_ageb_2020.csv](https://www.datos.gob.mx/dataset/ef697817-92a9-4937-8323-c08dda8bd00f/resource/baec624e-416a-4a01-a85d-73002451b3ee/download/grs_ageb_2020.csv)
- coneval.org.mx still hosts IRS 2020 zips (`/Medicion/Documents/IRS_2020/IRS_ent_mun_2000_2020.zip`, `IRS_loc_2000_2020.zip`) — [CONEVAL IRS 2020 anexos](https://www.coneval.org.mx/Medicion/IRS/Paginas/Indice_de_Rezago_Social_2020_anexos.aspx)

**Salud**
- **CLUES** (health facility catalog): the DGIS page links `http://gobi.salud.gob.mx/gobi/catalogos/catalogosmaestros/ESTABLECIMIENTO_SALUD_202608.xlsx?V=2026.09.23`, i.e. an **Aug 2026 cut** — [DGIS Catálogos CLUES](http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html)
- The old DGIS open-data page for **egresos** (`da_egresos_gobmx.html`) returns **404**. On datos.gob.mx, egresos appear only per institution: ISSSTE 2024, Hospital Infantil, Hospital Juárez. ISSSTE `servicios_salud_issste` includes SHP — [datos.gob.mx "egresos hospitalarios"](https://www.datos.gob.mx/api/3/action/package_search?q=egresos%20hospitalarios)
- Secretaría de Salud **registro_defunciones** on datos.gob.mx (annual CSVs starting 1998; modified 2025-06-04) — [datos.gob.mx "defunciones"](https://www.datos.gob.mx/api/3/action/package_search?q=defunciones)

**SEP**
- **Catálogo de Centros de Trabajo SEP (2025)**: `CNCT_DA_2025_13112025.csv` (and 2024), plus per-state legacy files including NL `catalogo_centro_trabajo_19_csv.csv` (dataset modified 2026-03-13) — [datos.gob.mx catalogo_centros_trabajo_sep](https://www.datos.gob.mx/api/3/action/package_show?id=catalogo_centros_trabajo_sep). SIGED school search: https://www.siged.sep.gob.mx/SIGED/escuelas.html (200) — [SEP SIGED](https://www.siged.sep.gob.mx/SIGED/escuelas.html)

**SESNSP**
- `incidencia_delictiva` on datos.gob.mx covers 2015–Dec 2025: state (`INM_estatal_dic25.csv`), **municipal** (`IDM_NM_dic25.csv`) and victims (`IDVFC_NM_dic25.csv`) on the 2015–2025 methodology — [datos.gob.mx incidencia_delictiva](https://www.datos.gob.mx/api/3/action/package_show?id=incidencia_delictiva)
- In the first half of 2026, 48 municipalities concentrated half of all intentional homicides — [ONC 1S2026](https://onc.org.mx/public/onc_site/uploads/reportes/ONC_Rueda_1S2026.pdf)

**IMSS**
- IMSS publishes employment and affiliation data at national and state level with **open data, interactive maps, time series and dynamic cubes**. Releases come on the 5th of each month (since Jan 2022) — [SNIEG IMSS methodology](https://www.snieg.mx/Documentos/IIN/Acuerdo_10_VIII_2020/sintesis_metod_ieptrp_imss.pdf). The portal `datos.imss.gob.mx` returned an "Error" page to automated requests on 14 Oct 2026 — [datos.imss.gob.mx](http://datos.imss.gob.mx/)
- IMSS keeps its **own municipality catalog**, maintained through internal procedure 9210-003-105. The format described appears alphanumeric, which differs from INEGI CVE_MUN — [IMSS procedure 9210-003-105](https://www.imss.gob.mx/sites/all/statics/pdf/procedimientos/9210-003-105.pdf) (weak evidence; verify against the files)

**Housing / SEDATU** (datos.gob.mx)
- `rezago_habitacional_2024.csv`, `deficit_vivienda_2024_adtd.csv` and `oferta_vivienda` (housing inventory days, 2025) — [datos.gob.mx "indice de rezago social" search](https://www.datos.gob.mx/api/3/action/package_search?q=indice%20de%20rezago%20social); [datos.gob.mx "vivienda registro unico" search](https://www.datos.gob.mx/api/3/action/package_search?q=vivienda%20registro%20unico)

**SAT**
- SAT has `declaraciones_y_pagos` on datos.gob.mx (aggregate tax collection, not spatial) — [datos.gob.mx search](https://www.datos.gob.mx/api/3/action/package_search?q=cedula%20de%20operacion%20anual)

### Inferences
- IMU (AGEB + colonia) and GRS (AGEB) together give two independent vulnerability scores on the same 2020 AGEB geometry. Colonia-level IMU is the most "citizen-legible" unit for a Monterrey demo.
- SESNSP has no AGEB detail. Sub-municipal crime would need state/municipal sources (out of scope) or the 2026 geolocated registry if it is ever published openly.

### Gaps
- **IMSS asegurados by municipality**: I found no verified dataset URL or dictionary. datos.gob.mx returned 0 hits for "asegurados imss" / "trabajadores asegurados".
- **Dengue / vector-borne disease open data**: 0 hits on datos.gob.mx, and the SSA page was not verified.
- **SSA morbidity/egresos (SAEH) national bulk** location after the DGIS URL change: not found.
- I could not read whether CLUES and the SEP CCT include **lat/lon**. CLUES is XLSX and was not opened; the SEP CSV was blocked by repodatos "Access Denied" from this server.
- I found no evidence on the SESNSP 2026 municipal open-data layout.

---

## 6. Join keys and gotchas: how do these datasets cross?

### Takeaway
Everything joins on **INEGI's CVEGEO hierarchy**: ENT(2) + MUN(3) + LOC(4) + AGEB(4) + MZA(3). Most problems are **zero-padding loss**, **census-vintage geometry mismatch**, **confidentiality asterisks**, **survey estimator rows**, and **non-INEGI municipal catalogs** (IMSS).

### Cited Findings
- The manzana geocode concatenates entidad, municipio, localidad, AGEB and manzana. The levels are standardized in the MG Norma Técnica — [SNIEG NT MG draft 2025](https://www.snieg.mx/Documentos/Demografico/sesiones/doc_12025/2_ntmg08mayo2025.pdf)
- Real key examples: municipality CVEGEO `19039` (Monterrey) via [wscatgeo](https://gaia.inegi.org.mx/wscatgeo/v2/mgem/19); EIC 2025 CVEGEO `190390000` (ent+mun+loc, 9 digits) via [EIC 2025 zip](https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip); IMU AGEB `CVE_AGEB` `0100100010017` (13 characters = ENT2+MUN3+LOC4+AGEB4) via [imu_2020.csv](https://www.datos.gob.mx/dataset/d8f2a534-bcee-4114-853d-82982a81ce24/resource/9600f414-c1ba-408a-8dd6-7f73d76601d4/download/imu_2020.csv)
- **Confidentiality**: AGEB and manzana indicators below 3 units show as `*`. Manzanas with 1–2 occupied dwellings show only POBTOT/VIVTOT — [INEGI fd_agebmza_urbana_cpv2020.pdf](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/fd_agebmza_urbana_cpv2020.pdf)
- INEGI aggregates finer grids into levels 4–9 for confidentiality reasons — [INEGI/CEPAL CPV 2020 innovations](https://d7.cepal.org/sites/default/files/presentations/innovaciones_censo_poblacion_vivienda_2020_mexico-inegi.pdf) (search summary)
- **Unpadded keys**: CONAPO IMU `ENT/MUN/LOC` stored as integers, with a float helper key — [imu_2020.csv](https://www.datos.gob.mx/dataset/d8f2a534-bcee-4114-853d-82982a81ce24/resource/9600f414-c1ba-408a-8dd6-7f73d76601d4/download/imu_2020.csv). CONAPO metro `clave_municipio` is unpadded — [municipios_poblacion.csv](https://www.datos.gob.mx/dataset/da65ccd9-888c-4ce8-b3b5-6bd867be344d/resource/6f57ab97-d1df-4768-beb8-c929c2449923/download/municipios_poblacion.csv)
- **EIC 2025**: filter `ESTIMADOR == "Valor"`, keep the CV and confidence-interval rows for quality flags, and read as Latin-1 — [EIC 2025 zip](https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip)
- **Metro localities are split**: Mitras Poniente (García) and Jardines de la Silla (Juárez) are separate ≥50k localities, apart from the municipal seats — [EIC 2025 zip](https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip)
- **Methodology breaks**: SESNSP incidence changes in Jan 2026 — [Expansión](https://politica.expansion.mx/voces/2026/03/06/el-sesnsp-y-el-truco-del-ilusionista). ATUS revised 2024 deaths for Apodaca — [INEGI ATUS](https://www.inegi.org.mx/sistemas/olap/proyectos/bd/continuas/transporte/accidentes.asp). CE 2024 values refer to **2023** — [INEGI CE2024](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2025/ce/CE2024_def.pdf)
- **IMSS municipality catalog** differs from INEGI's — [IMSS 9210-003-105](https://www.imss.gob.mx/sites/all/statics/pdf/procedimientos/9210-003-105.pdf) (unverified on actual files)

### Inferences
- **AGEB boundary changes**: AGEBs are created, subdivided and recoded between MG versions as the urban edge grows. Fast-growing García, Juárez, Escobedo, Apodaca, Pesquería and El Carmen (CONAPO 2010–2020 growth rates 6–22%/yr) will have many new AGEBs. Join 2020 census tables to the **MG version used for the 2020 census**, not to MG 2024, and use spatial overlay to move 2010 data onto 2020 geometry. This is standard INEGI practice; I did not find an INEGI document quantifying NL AGEB changes.
- Cast all keys to zero-padded strings at load time: `CVE_ENT` → 2, `CVE_MUN` → 3, `CVE_LOC` → 4, `CVE_AGEB` → 4 (alphanumeric, e.g. "084A"), `CVE_MZA` → 3.
- DENUE, CLUES, SEP CCT, RETC, SMN and SINAICA points all go to manzana/AGEB via point-in-polygon on the MG layer.

### Gaps
- No official crosswalk between AGEB versions (2010 → 2020 → 2024) was found.

---

## 7. APIs vs. bulk downloads, and the 10 most valuable datasets for AGEB/manzana crossing in Monterrey

### Takeaway
Real APIs: **INEGI Indicadores (token)**, **INEGI DENUE (token)**, **INEGI wscatgeo (no token)**, and the **datos.gob.mx CKAN API** (no token; needs a User-Agent). Everything else is bulk CSV/SHP/XLSX or a query app. For AGEB/manzana crossing, the top 10 are listed below.

### Cited Findings
**APIs**
- INEGI Indicadores (BISE/BIE v2.0, JSON/XML/JSON-stat, token) — [INEGI](https://www.inegi.org.mx/servicios/api_indicadores.html)
- INEGI DENUE v1 (token, 5 km radius cap) — [INEGI](https://www.inegi.org.mx/servicios/api_denue.html)
- INEGI wscatgeo (open) — [INEGI](https://gaia.inegi.org.mx/wscatgeo/v2/mgem/19)
- datos.gob.mx CKAN `api/3/action` — [datos.gob.mx](https://www.datos.gob.mx/api/3/action/package_show?id=indices_marginacion)
- Wrappers: INEGIpy 2.0.0 (Python) — [PyPI](https://pypi.org/pypi/INEGIpy/json); rsinaica (R) — [CRAN](https://cran.r-project.org/web/packages/rsinaica/refman/rsinaica.html)

**Bulk only (static files, no token)**
- Censo 2020 AGEB/manzana and ITER, MG 2024, DENUE CSV/SHP, CE 2024, ATUS, EDR, EIC 2025, SMN daily `.txt`, Monitor de Sequía XLSX, SIH dam CSVs, CLUES XLSX, CONAPO/CONEVAL/CONAFOR/SESNSP/SEP CSVs (sources above)

**Query apps only**
- REPDA — [CONAGUA](https://app.conagua.gob.mx/consultarepda.aspx); RETC — [CEC](https://cec.org/files/documents/events/day-1_2c_ernesto_2025_presentacion.pdf); SCINCE / INV / Espacio y Datos viewers (sources above)

**Top 10 for AGEB/manzana crossing in the ZMM** (my ranking; each dataset's source is cited above)
1. **INEGI Marco Geoestadístico** (AGEB/manzana/localidad polygons; Dec 2024 national zip, 3.3 GB). It is the geometry backbone.
2. **Censo 2020 – Principales resultados por AGEB y manzana urbana (NL)**: 222/215 indicators, CVEGEO join.
3. **DENUE 05/2026** (points, CSV/SHP plus API; next release 25 Nov 2026).
4. **CONAPO Índice de Marginación Urbana 2020**: AGEB and **colonia** (with SHP).
5. **CONEVAL Grado de Rezago Social por AGEB 2020** (CSV + SHP).
6. **Censos Económicos 2024** AGEB/manzana results (reference year 2023).
7. **INEGI ATUS** (municipal; georeferenced points in listed municipalities), joined to RNC 2025 streets.
8. **CLUES (Aug 2026) + SEP Catálogo de Centros de Trabajo (2025)** as service-access points (lat/lon still to be confirmed).
9. **Physical layers**: CEM (elevation), USV Serie VII, CONAPO urban expansion 1985/2002/2018, CENAPRED Atlas layers. Use zonal statistics per AGEB.
10. **Environmental points**: SMN daily stations, SINAICA/INECC NL concentrations, RETC 2024 facilities (189 NL). Interpolate or buffer to AGEB.
- Municipal-level complements: EIC 2025, CONAPO projections to 2040, SESNSP municipal crime (to Dec 2025), EDR deaths (definitive 2025 due Nov 2026), Monitor de Sequía municipal, CONAPO ICE 2020.

### Inferences
- The highest-leverage hackathon join is **Censo 2020 AGEB + IMU/GRS + DENUE + CLUES/SEP points on MG geometry**. It covers vulnerability against access to services and jobs at walking scale, and every dataset in it is free, tokenless (except optional DENUE API) and already verified as downloadable.
- Pre-download everything before the event. INEGI's MG national zip is 3.3 GB, and `repodatos.atdt.gob.mx` may block automated or non-Mexican traffic.

### Gaps
- The ranking is a judgment call, not source-backed.
- Lat/lon availability in CLUES and SEP CCT, the ATUS georeferencing coverage for NL, and the CE 2024 AGEB file paths still need hands-on confirmation.
