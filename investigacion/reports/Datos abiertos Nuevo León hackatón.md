# Monterrey guarda sus mejores datos en geoservidores

Para un hackatón de 24–48 horas en Monterrey, los datos públicos que más rinden no están en el portal estatal, sino en **dos geoservidores WFS abiertos y sin llave de acceso**. El primero es **MIDE, del municipio de Monterrey**, con 125 capas vectoriales: entre ellas **444,948 choques geolocalizados desde 2017** y un índice por colonia de isla de calor, PM2.5, NO2 y cobertura arbórea. El segundo es el **GeoServer SINA de CONAGUA**, con concesiones REPDA que traen titular y coordenadas, la disponibilidad de los 23 acuíferos de Nuevo León y la piezometría. Alrededor de ellos todo se arma sobre el esqueleto de INEGI (Censo 2020 por AGEB y manzana, Marco Geoestadístico, DENUE 05/2026), más los índices de marginación de CONAPO y de rezago de CONEVAL. Todo se cruza por **CVEGEO**. Los satélites (Landsat para temperatura de superficie, Sentinel-2 para NDVI, el mapa de altura de copa de 1 m de Meta, Sentinel-5P para NO2) llenan lo que ningún gobierno publica. El portal estatal (CKAN, **132 datasets, no los 368 anunciados**) sirve para microdatos administrativos por municipio, como consultas médicas, nacimientos, solicitudes al 070 y rutas de camión, pero casi no trae geometría.

Los cruces con mejor relación impacto/esfuerzo son cuatro: un índice de vulnerabilidad al calor por AGEB, un mapa de quién tiene concesiones de agua en acuíferos sobreexplotados, un semáforo de presas que incluya la Presa Libertad medida por satélite y un recalculador abierto de días con aire fuera de norma. Las trampas que más horas cuestan son los asteriscos de confidencialidad del Censo 2020, el desfase entre versiones de AGEB, la API de presas de CONAGUA (congelada desde el 23-abr-2025), SIMA sin descarga masiva y las cuotas de Earth Engine vigentes desde el 27-abr-2026. **No se pudo identificar con certeza el hackatón.** No apareció ninguno organizado por el Gobierno de Nuevo León en octubre de 2026, y los dos más parecidos (3-oct-2026, Monterrey Tech Week) ya terminaron sin entregar datos propios.

> **Marcas de verificación usadas en todo el reporte.** **[V]** = verificado en vivo el 14-oct-2026: el endpoint respondió, se descargó el archivo o se consultó la API. **[D]** = documentado en la fuente citada, sin prueba en vivo. **[C]** = conocimiento previo del investigador (IDs de colecciones, fórmulas, especificaciones) sin re-verificar; pruébalo antes del evento.

## Ningún hackatón oficial publicó datos: cada equipo trae los suyos

La búsqueda no encontró ningún hackatón organizado por el Gobierno de Nuevo León en octubre de 2026 ni un convenio de datos para uno. Los dos eventos más cercanos fueron el **sábado 3-oct-2026**, durante Monterrey Tech Week, y ya aparecen como finalizados.

El primero es **"Hackathon por Nuevo León"**, en Aulas 6 del Tec Campus Monterrey. Ahí "expertos en temas como agua, movilidad, calidad del aire, seguridad y medio ambiente presentarán retos del estado" y los equipos hicieron prototipos con IA ([mexicohackathons](https://mexicohackathons.com/events/hackathon-por-nuevo-leon)). El segundo es el **"Grok Monterrey Build Day / AI for Monterrey Hackathon"**, organizado por Aileen Villanueva y Monterrey Tech Week. Tuvo tracks de Water & Sustainability, Climate & Air Quality, Smart Mobility, Public Safety, Health & Wellbeing, Education y Government Services, pero las dependencias aparecen solo como socios *potenciales* y **no se especificó ningún dataset ni API** ([Luma](https://luma.com/5ohq71b3)). Monterrey Tech Week se declara "100% independiente, sin afiliación a… instituciones de gobierno" ([mexicohackathons](https://mexicohackathons.com/events/hackathon-por-nuevo-leon)).

**HackMTY 2026**, "respaldado por el Gobierno de Nuevo León", tiene fechas contradictorias: un directorio dice 23-oct-2026 ([andresospina.co](https://andresospina.co/eventos-ia/evento/hackmty-2026/)) y otro dice 12–13 de septiembre, ya finalizado ([mexicohackathons](https://mexicohackathons.com/events/hackmty-2026)). Los próximos eventos en Monterrey son un bootcamp de Polkadot en la UANL (29–31 oct) y "Revolution" (5–6 dic) ([mexicohackathons Monterrey](https://mexicohackathons.com/hackathons/monterrey)).

Para el equipo, la consecuencia práctica es que el estado no tiene un programa de APIs para desarrolladores. El gobierno digital vive en la Subsecretaría de Tecnologías, que soporta el portal de datos abiertos ([datosabiertos.nl.gob.mx](https://datosabiertos.nl.gob.mx/)), y en la ventanilla de trámites NLínea. La capa real de APIs de Nuevo León se reduce a tres piezas: el **CKAN estatal**, la **API OCDS de compras** y el **GeoNode/WFS de Monterrey**. Todo lo demás requiere scraping, descargar XLSX a mano o pedir por transparencia, y una solicitud tarda 10 días hábiles o más, así que no cabe en 48 horas.

La buena noticia es que los tracks que propusieron los organizadores (agua, aire, movilidad, seguridad, salud) corresponden casi uno a uno con las fuentes de este reporte. Los criterios de evaluación del evento Grok (ejecución técnica, uso de IA, impacto, factibilidad, IA responsable) premian lo que una dependencia podría adoptar el lunes siguiente. El uso de IA más natural con estos datos es clasificar o geocodificar los ~320,000 reportes ciudadanos de texto libre que hay en MIDE, que no traen coordenadas.

## Dos geoservidores WFS y un CKAN concentran lo local

**MIDE (mide.monterrey.gob.mx)** es la fuente municipal estrella. Es un GeoNode cuya API devolvió 175 recursos, de ellos **125 capas vectoriales descargables por usuarios anónimos**, todas servidas por WFS ([MIDE API](https://mide.monterrey.gob.mx/api/v2/resources?page_size=200)). El viejo portal datos.monterrey.gob.mx está muerto: sus ligas CKAN regresan una página vacía ([datos.monterrey.gob.mx](https://datos.monterrey.gob.mx/)).

El **CKAN estatal** (catalogodatos.nl.gob.mx, versión 2.10.4) tiene API abierta. Reportó **132 datasets**, de los cuales 129 son CSV, con licencias odc-by o cc-by y actualizaciones hasta el mismo 14-oct-2026 ([CKAN package_search](https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000)). Eso contrasta con los 368 datasets que presumió un comunicado de octubre de 2025 ([nl.gob.mx](https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/Contralor%C3%ADa%20y%20Transparencia%20Gubernamental/Noticias/20251028_01_nl_gobiernoabierto_rendicioncuentas.docx)). El catálogo es fuerte en microdatos administrativos por municipio, débil en geometría, y **no tiene calidad del aire, incidencia delictiva ni catastro**.

Para agua, el hallazgo más valioso es el **GeoServer SINA de CONAGUA**. Tiene unas 150 capas, y con un solo GET por capa devuelve GeoJSON de todo el estado, incluido el REPDA masivo que mucha gente cree que solo se obtiene por transparencia ([SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities)).

| Fuente | Qué trae que valga la pena | Cómo se baja | Formato / grano | Llave de cruce | Verif. |
|---|---|---|---|---|---|
| **MIDE Monterrey (GeoNode)** | `incidentes_viales` (444,948 puntos desde 2017, act. mar-2025); `uesi_mty2022` (1,141 colonias con NO2, PM2.5, copa arbórea, isla de calor día/noche, NDBI; act. 2-may-2026); `uso_suelo` (363,368 polígonos); `zonas_inundacion`, `area_deslizamientos`, `rios_arroyos`; `rutas_transporte` (4,044 líneas); `ciclovias`; capas del Mundial (`zona_baja_velocidad`, act. 13–14-oct-2026); `permisos_de_construccion_2026` (811); `reportes_ciudadanos` (240,843, sin geometría) | WFS `https://mide.monterrey.gob.mx/geoserver/ows` con `outputFormat=application/json`; catálogo en `/api/v2/resources` | GeoJSON; punto, polígono de colonia o predio | colonia (polígono), punto en polígono | [V] |
| **CKAN estatal** | Consulta general de Salud (43 CSV, 2024–2026); nacimientos 2022–2025; solicitudes 070 (hasta jun-2026); rutas IMA con pasajeros, km e IPK; paradas Metrorrey con lat/lon; WiFi ConectaTeNL con lat/lon; diagnósticos comunitarios por colonia con lat/lon; `contratos-smpu` con coordenadas; residuos SIMEPRODE por municipio × mes; 4 CSV de SADM | `https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000` (no `datosabiertos.nl.gob.mx/api`, que da 404) | CSV con diccionario; municipio | `municipio` en texto (normalizar acentos), CCT en escuelas | [V] |
| **API OCDS de compras** | Contrataciones del estado en OCDS 1.1; release más reciente 9-oct-2026 | `https://api-ocds.nl.gob.mx/api/releases` | JSON paginado | ocid, proveedor | [V] |
| **CONAGUA SINA GeoServer** | REPDA `m01_vwaprovsbm` (51,642 aprovechamientos subterráneos de NL) y `m01_vwaprovspm` (1,369 superficiales), cortes 2020–2023; `m06_acuiferos_disponibilidad` (23 acuíferos, DOF 2023); `m06_vwpiezometria` (3,540 registros NL 2000–2022); `m02` RENAMECA; `m29`/`m30` plantas; `m28` cobertura; `m48`/`m50` marginación y rezago | `https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows` + `outputFormat=application/json&CQL_FILTER=…` | GeoJSON en EPSG:3857; punto/polígono | `clvacuifero`, municipio, coordenadas | [V] |
| **CONAGUA presas (API JSON)** | 210 presas por día: almacenamiento, NAMO/NAME, elevación. Claves NL: CCHNL, CPRNL, LBCNL, PSANL | `https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/AAAA-MM-DD` | JSON; presa × día, **1995 a 23-abr-2025** | fecha + clave SIH | [V] |
| **SADM "Niveles de Presas"** | Volumen diario de La Boca, Cerro Prieto y El Cuchillo; al 12-oct-2026, 925.539 de 1,458.1 Mm³ | Scraping de `https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles` | HTML | fecha + presa | [V] |
| **SMN estaciones diarias** | Lluvia, evaporación, Tmax y Tmin; estación 19052 "Monterrey (OBS)" con datos de 1951 al 9-oct-2026 | `https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/nl/dia{clave}.txt` | TXT por estación | coordenadas de la estación | [V] |
| **Monitor de Sequía municipal** | Categoría D0–D4 por municipio, de 31-ene-2003 a 30-sep-2026 | `MunicipiosSequia.xlsx` del SMN (2.1 MB) | XLSX; 2,478 municipios | CVEGEO municipal (5 dígitos) | [V] |
| **Cómo Vamos NL (GitHub)** | Repos reproducibles: completitud de estaciones SIMA, violencia de género, choques de peatones y ciclistas, árboles en zonas calientes, encuesta por manzana/AGEB, `taller-condatos` (arbolado contra islas de calor con satélite, actualizado 9-oct-2026) | `github.com/EvaluacionInvestigacion-CVNL` | CSV, Python | varía | [V] |

Fuentes de la tabla: [MIDE WFS](https://mide.monterrey.gob.mx/geoserver/ows?service=WFS&version=2.0.0&request=GetCapabilities), [CKAN status](https://catalogodatos.nl.gob.mx/api/3/action/status_show), [OCDS](https://api-ocds.nl.gob.mx/api/releases), [SINA presas](https://sinav30.conagua.gob.mx:8080/Presas/), [SADM](https://www.sadm.gob.mx/SADM/index.jsp?id_html=niveles), [SMN 19052](https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/nl/dia19052.txt), [Monitor de Sequía](https://smn.conagua.gob.mx/tools/RESOURCES/Monitor%20de%20Sequia%20en%20Mexico/MunicipiosSequia.xlsx), [repos CVNL](https://api.github.com/users/EvaluacionInvestigacion-CVNL/repos).

### Fuera de Monterrey, los municipios publican migajas

**San Pedro Garza García** tiene un CKAN viejo (2.7.6) con **12 datasets cuyo último cambio fue en junio de 2025**, uno de ellos un archivo `.numbers` de Apple disfrazado de CSV ([San Pedro CKAN](https://datos.sanpedro.gob.mx/api/3/action/package_search?rows=100)). **Escobedo** publica XLSX de permisos de construcción, obras públicas y reportes ciudadanos actualizados a mayo de 2026 ([Escobedo](https://escobedo.gob.mx/?p=datosabiertos)). **Santa Catarina** vive en `stacatarina.gob.mx`, porque `santacatarina.gob.mx` no resuelve ([Santa Catarina](https://www.stacatarina.gob.mx/da/datosabiertos.html)).

**Guadalupe** tiene un GeoServer público y sin documentar con **30 capas `gpe:`**: zonificación del PMDU 2040 y lo que parecen capas de atlas de riesgo (`ar08_zonapeligro`, `ar10_peligro`, `gpe_ar01` a `gpe_ar07`) ([GeoServer visormetropolitano](https://geoserver.visormetropolitano.com/geoserver/ows?service=WFS&version=2.0.0&request=GetCapabilities)). **Apodaca** solo ofrece su atlas en PDF, y en García y Juárez no se encontró nada.

Escobedo, San Pedro y Santa Catarina comparten el mismo set mínimo (calles, banquetas, ciclovías, permisos, reportes), así que se pueden comparar entre municipios, aunque con periodos distintos.

En transporte, **no existe GTFS público** de Metrorrey, TransMetro ni Ecovía, y el Mobility Database no tiene ningún feed de Nuevo León ([Mobility Database](https://share.mobilitydata.org/catalogs-csv)). Regio Ruta publica GTFS en tiempo real solo hacia Google Maps desde junio de 2026 ([ITDP](https://mexico.itdp.org/wp-content/uploads/2026/06/GTFS-Nota-tecnica-eventos-masivos-Jun-2026-.pdf)). Hay que reconstruir rutas con las capas `regio_ruta_` y `paradas_ruta_*` de MIDE.

### Agua: la API de presas murió en 2025, pero el WFS de CONAGUA sigue vivo

La serie diaria de presas tiene un hueco que hay que tapar a mano. La API JSON de CONAGUA reporta `fechaMonitoreo/ultimo` = **2025-04-23**, y cualquier fecha posterior al 25-abr-2025 regresa un arreglo vacío ([SINA último](https://sinav30.conagua.gob.mx:8080/SINA45/fechaMonitoreo/ultimo)). Para hoy existen la página HTML de SADM y la serie diaria de MVS, "Nivel de las presas en Nuevo León HOY", que cita el reporte interno de CONAGUA. Con corte del 13-oct-2026, **El Cuchillo estaba al 57.66%, Cerro Prieto al 81.49% y La Boca al 93.36%**, y El Cuchillo II extraía 2.685 m³/s de 5 m³/s nominales ([MVS 14-oct-2026](https://mvsnoticias.com/nuevo-leon/2026/10/14/nivel-de-las-presas-en-nuevo-leon-hoy-miercoles-14-de-octubre-del-2026-749708.html)). El Cuchillo pasó de 97.6% de su NAMO el 13-oct-2024 ([SINA](https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/2024-10-13)) a 51.30% el 1-oct-2026 ([Milenio](https://www.milenio.com/comunidad/nivel-presas-nuevo-leon-aumento-lluvias-primer-frente-frio-2026)).

La **Presa Libertad/León** (NAMO 221 Mm³) no aparece en SADM, en el reporte diario ni entre las 210 presas del SINA. Su último dato público es "35–40%" en febrero de 2026 ([88.9 Noticias](https://889noticias.mx/noticias/conagua-confirma-que-la-presa-leon-esta-lista-para-su-entrega/)).

El lado subterráneo está en números rojos y es descargable. Según la capa de disponibilidad (DOF 9-nov-2023), **13 de los 23 acuíferos de NL tienen disponibilidad negativa, con un déficit conjunto de unos −381 hm³/año**. Cuatro están formalmente sobreexplotados: Campo Buenos Aires, Campo Mina, Agualeguas-Ramones y Campo Cerritos ([SINA GeoServer](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities); [MVS 28-sep-2026](https://mvsnoticias.com/nuevo-leon/2026/9/28/los-acuiferos-que-sostienen-a-monterrey-operan-en-numeros-rojos-747715.html)). Agregando el REPDA del corte 2023, las concesiones de SADM en Campo Buenos Aires suman 62.7 hm³, contra una recarga total de 57 hm³. En Apodaca, San Pedro y García el volumen industrial concesionado supera al público-urbano.

Los cuatro CSV de SADM en el CKAN estatal están **congelados desde el 7-nov-2025**, pero traen un dato que vale todo el proyecto: el **agua no contabilizada osciló entre 41.11% y 48.25% mensual** entre septiembre de 2024 y agosto de 2025 ([uso_agua.csv](https://catalogodatos.nl.gob.mx/dataset/ac8539c7-0c4b-4845-a53c-58f46c90cf7c/resource/81bed7a2-ed69-4ad6-93cb-d7e244084df1/download/2024_2025_uso_agua.csv)). SADM no publica nada por colonia o sector, ni redes, fugas o tandeos. Los tandeos de 2026 (unas 290 colonias afectadas en García) solo existen en prensa ([Enfoque Monterrey](https://enfoquemonterrey.com.mx/2026/07/07/agua-y-drenaje-y-garcia-acuerdan-tandeos-para-asegurar-suministro-de-agua/)).

### Aire: datos horarios por la puerta trasera

SIMA es la única red de referencia: **15 estaciones fijas en 11 de los 12 municipios de la ZMM, más 2 móviles**, que miden CO, NO, NO2, SO2, O3, PM2.5, PM10 y meteorología cada hora ([SIMA Reporte Agosto 2026](https://aire.nl.gob.mx/docs/reportes/mensuales/2026/08_Reporte_Agosto_2026.pdf)). El sitio no tiene descarga masiva: la historia está en PDF mensuales y las tablas cargan por JavaScript. Pero hay **tres endpoints JSON sin documentar ni llave** que devolvieron datos con sello "2026-10-14 17:00:00": `api_conc.php` (concentraciones con unidad y norma), `api_indice.php` y `api_meteo.php`, todos bajo `https://aire.nl.gob.mx/SIMA2017reportes/` [V]. Por defecto devuelven una sola estación (CENTRO), y el parámetro para elegir otra no está documentado.

La historia limpia sale del espejo nacional SINAICA. Su página de descarga lista **15 estaciones de Monterrey con ID numérico**: Santa Catarina 139, San Bernabé 140, Obispado 141, San Nicolás 142, ITNL 143, Escobedo 144, García 145, Apodaca 146, Juárez 147, San Pedro 148, Cadereyta 424, UANL 425, Prepa Tec Garza Lagüera 426, Pesquería 446 y Misión San Juan 479 ([SINAICA](https://sinaica.inecc.gob.mx/data.php)). El paquete de R **`rsinaica` v1.2.0** (2-jun-2026) las descarga con `sinaica_station_data()`, hasta dos años por llamada ([CRAN](https://cran.r-project.org/web/packages/rsinaica/refman/rsinaica.html)). OpenAQ v3 exige API key (sin ella responde 401) y no se confirmó qué estaciones de Monterrey ingiere [V].

La completitud es un problema en sí mismo. Con datos del repo de Cómo Vamos, la red tuvo **88.5% de días válidos** de oct-2025 a sep-2026, pero **PM2.5 solo 81.0%**, y San Bernabé apenas 147 de 365 días válidos de PM2.5 ([CVNL IME](https://github.com/EvaluacionInvestigacion-CVNL/indice-monitoreo-estaciones-gcv)).

Hay también una disputa pública que un equipo puede zanjar con datos. El gobierno reporta promedios 2025 a la baja (**PM10 49 µg/m³, PM2.5 18.9 µg/m³**) ([boletín NL](https://www.nl.gob.mx/sites/default/files/repositorio/Dependencias/Secretar%C3%ADa%20de%20Medio%20Ambiente/Noticias/20260112_01_balance_medio_ambiente.docx)), mientras un conteo independiente da **188 días fuera de norma en 2025** ([Milenio](https://amp.milenio.com/comunidad/nuevo-leon-fueron-sucios-mas-de-la-mitad-de-dias-durante-2025)). El nuevo inventario federal de emisiones de la ZMM (año base 2023) se anunció como concluido el 30-sep-2026, **sin cifras publicadas por fuente** ([Publimetro](https://www.publimetro.com.mx/nuevo-leon/2026/09/30/calidad-del-aire-en-el-estado-mejorara-si-se-ordenan-transporte-e-industria-concluye-inventario-de-emisiones/)).

### La primera hora en cinco comandos

Los endpoints de abajo se verificaron en vivo el 14-oct-2026. La sintaxis exacta de cada `curl` se armó a partir de ellos y no se ejecutó tal cual.

```bash
# CKAN estatal: catálogo completo (132 datasets)
curl -s 'https://catalogodatos.nl.gob.mx/api/3/action/package_search?rows=1000' > ckan_nl.json

# MIDE Monterrey: índice por colonia de calor / PM2.5 / NO2 / copa arbórea
curl -s 'https://mide.monterrey.gob.mx/geoserver/ows?service=WFS&version=2.0.0&request=GetFeature&typeNames=geonode:uesi_mty2022&outputFormat=application/json' > uesi_mty2022.geojson

# CONAGUA SINA: REPDA subterráneo de NL (~35 MB, ~6 s); geometría en EPSG:3857
curl -sG 'https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows' \
  --data-urlencode 'service=WFS' --data-urlencode 'version=2.0.0' --data-urlencode 'request=GetFeature' \
  --data-urlencode 'typeNames=Sina:m01_vwaprovsbm' --data-urlencode 'outputFormat=application/json' \
  --data-urlencode "CQL_FILTER=clvedo='19'" > repda_sub_nl.geojson

# CONAGUA presas: un día (la serie termina el 2025-04-23)
curl -s 'https://sinav30.conagua.gob.mx:8080/PresasPG/presas/reporte/2025-04-20' > presas_2025-04-20.json

# SIMA en vivo: concentraciones de la última hora (estación por defecto)
curl -s 'https://aire.nl.gob.mx/SIMA2017reportes/api_conc.php'
```

## CVEGEO amarra todo: INEGI y los federales a nivel AGEB

INEGI pone el esqueleto y la llave. Todo lo federal se cruza por la jerarquía **CVEGEO**: entidad (2) + municipio (3) + localidad (4) + AGEB (4, alfanumérica) + manzana (3) ([SNIEG NT MG](https://www.snieg.mx/Documentos/Demografico/sesiones/doc_12025/2_ntmg08mayo2025.pdf)).

El dato que define la estrategia es que **no hubo "Conteo 2025"**. INEGI levantó la **Encuesta Intercensal 2025**, publicada el 22-sep-2026, que solo baja a municipio y a localidades de 50,000 habitantes o más ([INEGI 54/26](https://www.inegi.org.mx/contenidos/saladeprensa/boletines/2026/ei/EIC2025-def_CP.pdf)). Por eso el **Censo 2020 sigue siendo la fuente más fina por AGEB y manzana**. El CONEVAL desapareció en 2025 y sus funciones pasaron al INEGI ([Zeta Tijuana](https://zetatijuana.com/2025/06/senado-concretan-extincion-del-coneval-trasladan-sus-funciones-al-inegi/)), así que sus productos por AGEB son legado congelado, pero siguen descargables.

| Producto | Grano | Descarga | Nota | Verif. |
|---|---|---|---|---|
| Censo 2020, resultados por AGEB y manzana urbana (NL) | AGEB (222 indicadores), manzana (215) | [ageb_mza_urbana_19_cpv2020_csv.zip](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/ageb_manzana/ageb_mza_urbana_19_cpv2020_csv.zip) (12.0 MB) | Asteriscos por confidencialidad | [V] |
| Censo 2020 ITER (NL) | localidad | [iter_19_cpv2020_csv.zip](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/datosabiertos/iter/iter_19_cpv2020_csv.zip) | | [V] |
| Censo 2020, microdatos del cuestionario ampliado (NL) | muestra representativa por municipio | [Censo2020_CA_nl_csv.zip](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/microdatos/Censo2020_CA_nl_csv.zip) (11.4 MB) | | [V] |
| Marco Geoestadístico, dic-2024 | polígonos de municipio, localidad, AGEB y manzana | [794551132173_s.zip](https://www.inegi.org.mx/contenidos/productos/prod_serv/contenidos/espanol/bvinegi/productos/geografia/marcogeo/794551132173_s.zip) (**3.33 GB**, nacional) | No se encontró un MG 2025 | [V] |
| wscatgeo (sin token) | municipios de NL con población | [gaia.inegi.org.mx/wscatgeo/v2/mgem/19](https://gaia.inegi.org.mx/wscatgeo/v2/mgem/19) | JSON | [V] |
| Encuesta Intercensal 2025 | municipio + localidades de 50k o más | [conjunto_de_datos_eic2025_105_csv.zip](https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip) (8.3 MB) | NL = 6,274,840 hab.; temas nuevos: desplazamiento forzado, salud mental | [V] |
| DENUE 05/2026 | punto por establecimiento | [denue_19_csv.zip](https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_csv.zip) (21.5 MB), [denue_19_shp.zip](https://www.inegi.org.mx/contenidos/masiva/denue/denue_19_shp.zip) (42.2 MB); [API](https://www.inegi.org.mx/servicios/api_denue.html) con token, radio máximo de 5 km | Próximo corte: 25-nov-2026 | [V] |
| Censos Económicos 2024 (año de referencia 2023) | hasta AGEB/manzana | [CSV nacional](https://www.inegi.org.mx/programas/ce/2024/) | Ruta de las tablas por AGEB sin confirmar | [V] nacional, [D] AGEB |
| CONAPO Índice de Marginación Urbana 2020 | AGEB y **colonia** (con SHP de colonias) | [datos.gob.mx indices_marginacion](https://www.datos.gob.mx/api/3/action/package_show?id=indices_marginacion) | Llaves sin ceros a la izquierda | [V] columnas |
| CONEVAL Grado de Rezago Social 2020 | AGEB (con SHP) | [datos.gob.mx rezago_social](https://www.datos.gob.mx/api/3/action/package_show?id=rezago_social) | Trae `i_noagua`, `i_nodren`, `i_nointernet` | [V] columnas |
| CLUES (ago-2026) y SEP Centros de Trabajo 2025 | punto (lat/lon por confirmar) | [DGIS CLUES](http://www.dgis.salud.gob.mx/contenidos/intercambio/clues_gobmx.html), [SEP CCT](https://www.datos.gob.mx/api/3/action/package_show?id=catalogo_centros_trabajo_sep) | | [D] |
| SESNSP incidencia municipal | municipio × mes, 2015 a dic-2025 | [datos.gob.mx incidencia_delictiva](https://www.datos.gob.mx/api/3/action/package_show?id=incidencia_delictiva) | Quiebre metodológico en ene-2026 | [D] |
| INEGI ATUS (accidentes) | municipio | [atus_anual_csv.zip](https://www.inegi.org.mx/sistemas/olap/proyectos/bd/continuas/transporte/accidentes.asp) (131.7 MB, fechado ago-2024) | Archivo masivo 2025 sin confirmar | [V] |

| Llave | Formato | Ejemplo real | Dónde aparece |
|---|---|---|---|
| Municipio | 5 dígitos (2+3) | `19039` = Monterrey | wscatgeo, Monitor de Sequía, CONAPO `clave_compuesta_municipio` |
| Localidad | 9 dígitos (2+3+4) | `190390000` | EIC 2025 |
| AGEB | 13 caracteres (2+3+4+4); la AGEB es alfanumérica, p. ej. `084A` | `0100100010017` (Aguascalientes, en IMU) | Censo, IMU (`CVE_AGEB`), GRS |
| Manzana | 16 caracteres (AGEB + 3) | — | Censo por manzana, Marco Geoestadístico |
| Estación de aire | ID numérico SINAICA | 141 = Obispado | SINAICA, `rsinaica` |
| Presa | clave SIH de 5 letras | `CCHNL` = El Cuchillo | API de presas CONAGUA |
| Acuífero | `clvacuifero` | 1906 AMM, 1907 Campo Buenos Aires, 1908 Campo Mina | SINA `m01`, `m06` |
| Escuela | CCT | — | CKAN estatal, SEP |
| Municipio (estado) | texto libre | "Monterrey" | CKAN estatal, 070, Salud |

La ZM Monterrey de CONAPO 2020 son **16 municipios**: 19006, 19009, 19010, 19012, 19018, 19019, 19021, 19025, 19026, 19031, 19039, 19041, 19045, 19046, 19048 y 19049 ([CONAPO metrópolis](https://www.datos.gob.mx/dataset/da65ccd9-888c-4ce8-b3b5-6bd867be344d/resource/6f57ab97-d1df-4768-beb8-c929c2449923/download/municipios_poblacion.csv)).

La Encuesta Intercensal muestra dónde envejeció más el Censo 2020. **García pasó de 397,205 a 550,959 habitantes (+39%)** y Apodaca llegó a 712,979 ([EIC 2025](https://www.inegi.org.mx/contenidos/programas/eic/2025/datosabiertos/conjunto_de_datos_eic2025_105_csv.zip)). Cualquier métrica "por habitante" calculada por AGEB en la periferia norte y poniente subestima el denominador. Conviene reescalar con los totales municipales de 2025 y decirlo en la lámina.

Dos atajos ahorran horas. El SHP de GRS por AGEB 2020 y el de IMU por colonia ya traen geometría de 2020, así que la descarga de 3.33 GB del Marco Geoestadístico es opcional para un primer prototipo. Y la librería `INEGIpy` envuelve las APIs de INEGI en Python ([PyPI](https://pypi.org/pypi/INEGIpy/json)).

## Los satélites miden lo que nadie publica: calor, verde y agua

Tres huecos de datos de tierra los llena el espacio. No se encontró un inventario georreferenciado de árboles en ningún municipio del AMM. Tampoco se encontró un mapa oficial de vulnerabilidad al calor por colonia. Y la Presa Libertad no tiene nivel público. Para el municipio de Monterrey hay un atajo: la capa `uesi_mty2022` de MIDE ya trae isla de calor día/noche, PM2.5, NO2 y copa arbórea por colonia. Los satélites sirven para extender eso a los otros 15 municipios de la ZM y para validarlo.

Como línea base citable existe un estudio publicado en ISPRS Annals que relaciona temperatura de superficie con infraestructura verde-azul en el AMM para 2003, 2013 y 2021 ([ISPRS 2024](https://isprs-annals.copernicus.org/articles/X-3-2024/439/2024/)).

| Capa | Resolución / periodo | Acceso | Para qué sirve | Verif. |
|---|---|---|---|---|
| Landsat 8/9 C2 L2, banda `ST_B10` | 30 m (TIRS nativo de 100 m), revisita de 8 días, desde 2013 | GEE `LANDSAT/LC08/C02/T1_L2` y `LANDSAT/LC09/C02/T1_L2`; Planetary Computer `landsat-c2-l2` | Temperatura de superficie; K = ST_B10 × 0.00341802 + 149.0 | [C] ([GEE](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2)) |
| Sentinel-2 L2A + Cloud Score+ | 10 m, unos 5 días | GEE `COPERNICUS/S2_SR_HARMONIZED` + `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED`; Planetary Computer `sentinel-2-l2a` | NDVI; MNDWI para el área de las presas | [C] ([GEE](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)) |
| Dynamic World V1 | 10 m por escena, de 2015 a casi tiempo real | GEE `GOOGLE/DYNAMICWORLD/V1` | Cambio en árboles y área construida, 2016→2026 | [C] ([GEE](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1)) |
| Meta/WRI altura de copa | **1 m**; imágenes 2009–2020; error medio de 2.8 m | GEE community `projects/sat-io/open-datasets/facebook/meta-canopy-height` | % de la AGEB con copa de más de 3 m | [V] ([catálogo](https://gee-community-catalog.org/projects/meta_trees/)) |
| Sentinel-5P TROPOMI | unos 5.5 × 3.5 km, diario hacia las 13:30 | GEE `COPERNICUS/S5P/OFFL/L3_NO2` (y SO2, CO, HCHO) | NO2 a escala metropolitana o municipal, **no por AGEB** | [C] ([GEE](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_NO2)) |
| TEMPO | horario de día; píxel nominal de 2 × 4.75 km, más grueso sobre Monterrey | NASA Earthdata / `earthaccess` | Ciclo diario de NO2 | [V] cobertura ([SAO](https://tempo.si.edu/instrument.html)); estado en 2026 sin confirmar |
| Open Buildings 2.5D Temporal | anual 2016–2023, 4 m efectivos, con alturas | GEE `GOOGLE/Research/open-buildings-temporal/v1` | Expansión urbana, efecto cañón | [V] ([GEE](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1)); inclusión de México sin probar |
| Overture Maps (edificios, lugares, calles) | GeoParquet mensual | `overturemaps download --bbox=-100.65,25.45,-99.95,26.05 -f geoparquet --type=building` | Edificios, parques, servicios | [C] ([docs](https://docs.overturemaps.org/getting-data/)) |
| Copernicus DEM GLO-30 | 30 m | GEE `COPERNICUS/DEM/GLO30` | Pendientes, control de elevación, proximidad a cauces | [C] ([GEE](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30)) |
| JRC Global Surface Water + Sentinel-1 GRD | 30 m 1984–**2021**; radar de 10 m desde 2014 | GEE `JRC/GSW1_4/...`, `COPERNICUS/S1_GRD` | Historia del agua superficial; inundaciones bajo nubes | [C] ([GEE](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD)) |
| CHIRPS / ERA5-Land | unos 5 km diario desde 1981; unos 9 km horario desde 1950 | GEE `UCSB-CHG/CHIRPS/DAILY`, `ECMWF/ERA5_LAND/HOURLY`; [data.chc.ucsb.edu](https://data.chc.ucsb.edu/products/CHIRPS-2.0/) | Lluvia, temperatura del aire | [V] descarga, [C] IDs |
| NASA FIRMS | VIIRS 375 m, menos de 3 h de latencia | [API](https://firms.modaps.eosdis.nasa.gov/api/) con MAP_KEY gratuita | Incendios en Cumbres y Sierra Madre | [C] |
| OPERA DISP-S1 | 30 m, 2016–2025 | ASF Vertex | Subsidencia cerca de pozos | [V] la cobertura incluye México hasta Panamá ([Earthdata](https://www.earthdata.nasa.gov/data/catalog/asf-opera-l3-disp-s1-v1-1)); frames sobre Monterrey sin verificar |

**Earth Engine cambió de reglas.** Desde el **27-abr-2026**, cada proyecto no comercial tiene una cuota mensual. El nivel Community da **150 EECU-horas**. El nivel Contributor da 1,000, pero requiere ligar una cuenta de facturación, aunque el uso no comercial de EE no se cobra. El nivel Partner da 100,000 y su aprobación tarda "varias semanas". Al pasarse de la cuota, el proyecto cae en un "modo restringido" con menos capacidad, y **está prohibido multiplicar proyectos para sumar cuota** ([GEE tiers](https://developers.google.com/earth-engine/guides/noncommercial_tiers)). 150 horas alcanzan para estadísticas zonales de unos miles de AGEB si se usan medianas y exportaciones por lote. El riesgo es que todo el equipo comparta un solo proyecto y haga mosaicos interactivos sin parar.

El plan B sin cuota es Python local contra el catálogo STAC de Planetary Computer, que sigue operando aunque su Hub gratuito cerró el 6-jun-2024 ([GitHub PC](https://github.com/microsoft/PlanetaryComputer/discussions/347)). Se usa con `pystac-client` + `odc-stac` + `exactextract`.

Planet no es opción. Su programa Education & Research exige correo universitario y tarda hasta 3 semanas en aprobarse ([Planet](https://support.planet.com/hc/en-us/articles/360016570538-How-Can-I-Register-for-the-Education-and-Research-Basic-Program)). MODIS sigue disponible, pero Terra y Aqua van a la deriva y terminan hacia 2027, así que para series nuevas conviene VIIRS ([LAADS](https://ladsweb.modaps.eosdis.nasa.gov/learn/modis-to-viirs-transition/)).

Tres decisiones de método evitan que el jurado tumbe el resultado:

- **NDVI en época seca.** Calcular NDVI con compuestos de marzo a mayo separa el pasto regado del matorral seco.
- **Controlar la elevación en la LST.** El valle está a unos 500–600 m y las sierras pasan de 2,000 m. Hay que meter el DEM como covariable o quedarse solo con AGEB urbanas.
- **Llamar a la LST por su nombre.** Landsat mide la superficie a media mañana, no el aire en la tarde. Hay que presentarla como "exposición térmica superficial".

El AOI del área metropolitana es `[-100.65, 25.45, -99.95, 26.05]`, en UTM 14N (EPSG:32614). Las presas quedan fuera de ese recuadro, así que hay que ampliarlo al oriente para El Cuchillo y al sur para Cerro Prieto.

```python
# Receta mínima NDVI + LST por AGEB en Earth Engine.
# [C] Escrita a partir de las specs del catálogo, NO ejecutada: probar antes del evento.
import ee
ee.Initialize(project="TU-PROYECTO-NO-COMERCIAL")
aoi = ee.Geometry.Rectangle([-100.65, 25.45, -99.95, 26.05])
agebs = ee.FeatureCollection("projects/TU-PROYECTO/assets/ageb_urbana_mty")  # SHP de INEGI subido como asset

csp = ee.ImageCollection("GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED")
ndvi = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi)
        .filterDate("2026-03-01", "2026-05-31").linkCollection(csp, ["cs_cdf"])
        .map(lambda i: i.updateMask(i.select("cs_cdf").gte(0.6))
                        .normalizedDifference(["B8", "B4"]).rename("ndvi"))
        .median())

def lst(i):
    clear = i.select("QA_PIXEL").bitwiseAnd(0b11111).eq(0)  # relleno, nube dilatada, cirros, nube, sombra
    return (i.select("ST_B10").multiply(0.00341802).add(149.0).subtract(273.15)
             .updateMask(clear).rename("lst_c"))

lst_med = (ee.ImageCollection("LANDSAT/LC08/C02/T1_L2")
           .merge(ee.ImageCollection("LANDSAT/LC09/C02/T1_L2"))
           .filterBounds(aoi).filterDate("2023-01-01", "2026-10-01")
           .filter(ee.Filter.calendarRange(5, 9, "month")).map(lst).median())

stats = ndvi.addBands(lst_med).reduceRegions(
    collection=agebs, reducer=ee.Reducer.mean(), scale=30, tileScale=4)
ee.batch.Export.table.toDrive(stats, description="mty_ageb_ndvi_lst", fileFormat="CSV").start()
```

## Ocho cruces que caben en 48 horas, ordenados por impacto

La lista se ordenó con tres criterios: que todos los insumos estén verificados como descargables, que el hueco no lo llene hoy ninguna fuente pública, y que una dependencia estatal o municipal entienda el resultado y lo pueda adoptar. Los cuatro primeros tienen todos sus insumos verificados y caben en el tiempo del evento. Para un equipo de cuatro, un reparto que funciona es: una persona en Earth Engine, una en vectores y Censo, una en series de agua y aire, una en el frontend.

| # | Cruce | Datos exactos (marca de verificación) | Llave | Por qué gana | Riesgo principal |
|---|---|---|---|---|---|
| 1 | **Vulnerabilidad al calor por AGEB o colonia** | Exposición: LST de Landsat 8/9, mediana de mayo a septiembre 2023–2026 [C], o `uesi_mty2022` de MIDE para Monterrey [V]. Falta de enfriamiento: NDVI de Sentinel-2 + copa de Meta de 1 m [C/V]. Sensibilidad: Censo 2020 por AGEB, población por edad [V] (nombres de variables [C]) e IMU 2020 [V]. Capacidad de adaptación: distancia a parques de OSM/Overture o MIDE | CVEGEO de AGEB (estadística zonal) o polígono de colonia | No hay mapa oficial por colonia. NL tuvo **102 muertes por calor en 2023**, y el índice de calor fue peor en el oriente (Juárez, San Nicolás) | La LST no es temperatura del aire; la elevación confunde |
| 2 | **¿Quién tiene concesiones de agua en acuíferos sobreexplotados?** | SINA `m01_vwaprovsbm` + `m06_acuiferos_disponibilidad` + `m06_vwpiezometria` [V]; marginación SINA `m48` o IMU por municipio [V] | `clvacuifero` + municipio + punto en polígono | 13 de 23 acuíferos en déficit (−381 hm³). Es la primera respuesta abierta al debate de 2022 entre industria y hogares | El volumen es concesionado, no medido; SADM le vende agua a la industria |
| 3 | **Semáforo de días de suministro + rastreador satelital de la Presa Libertad** | Historia de la API de presas 1995–abr-2025 [V]; scraper de SADM [V]; notas diarias de MVS para el hueco; Monitor de Sequía [V]; SMN 19052 o CHIRPS [V]; área MNDWI de Sentinel-2 calibrada contra el almacenamiento oficial [C] | fecha + clave SIH | Libertad (221 Mm³) **no tiene nivel público**; El Cuchillo bajó de 97.6% a 51.3% en un año | Hueco abr-2025 → hoy; los NAMO no coinciden entre fuentes |
| 4 | **Recalculador abierto de excedencias de aire + tablero de funcionamiento de estaciones** | SINAICA vía `rsinaica`, 15 estaciones horarias [V]; JSON en vivo de SIMA [V]; repo IME de Cómo Vamos [V] | ID de estación + hora | Zanja la disputa entre el promedio oficial a la baja y los 188 días fuera de norma, fase por fase de la NOM-025 | PM2.5 con solo 81% de días válidos |
| 5 | **Equidad verde: m² por habitante contra marginación** | Parques de OSM/Overture [C]; capas `vegetacion` y parques de MIDE [V]; árboles de Dynamic World [C]; POBTOT del Censo por AGEB [V]; SHP de IMU por colonia [V] | CVEGEO de AGEB o colonia | Las cifras publicadas van de **3.9 a 7.75 m²/hab** según el método, contra 12.96 en San Pedro y 2.63 en el norte de Monterrey. Nadie ha publicado un método abierto | La definición de "área verde" cambia según la fuente |
| 6 | **Seguridad vial y zonas del Mundial** | `incidentes_viales` (444,948), `ciclovias` y `zona_baja_velocidad` de MIDE [V]; ATUS [V]; Censo por AGEB [V] | punto en polígono (colonia/AGEB) | Es la capa puntual más grande disponible, y las motos casi se duplicaron entre 2019 y 2025 | Solo cubre el municipio de Monterrey; la capa es de mar-2025 |
| 7 | **Resiliencia hídrica por manzana** | Variables de vivienda del Censo 2020 por manzana (tinaco, cisterna, agua entubada; nombres exactos [C]); DEM GLO-30 como proxy de presión [C]; tandeos en García sacados de prensa; IMU [V] | CVEGEO de manzana + colonia | En 2022 García pasó hasta 18 días seguidos sin agua; San Pedro, alrededor de uno | No hay dataset de tandeos; hay que geocodificar notas |
| 8 | **Huella de inundación de Alberto (2024)** | Sentinel-1 GRD del 19 al 21 de junio de 2024 [C]; `zonas_inundacion` y `puntos_inundacion` de MIDE [V]; manzanas del INEGI [V] | polígono a manzana | El atlas estatal es de 2012 y el de Monterrey, de 2009 | El radar sufre layover en la montaña: hay que enmascarar pendientes |

Fuentes de los datos de contexto de la tabla: muertes por calor e índice de calor ([UANL, ISPRS 2026](https://isprs-annals.copernicus.org/articles/X-3-W3-2025/165/2026/isprs-annals-X-3-W3-2025-165-2026.pdf)); acuíferos ([MVS](https://mvsnoticias.com/nuevo-leon/2026/9/28/los-acuiferos-que-sostienen-a-monterrey-operan-en-numeros-rojos-747715.html)); área verde 3.9 m²/hab ([Milenio](https://www.milenio.com/estados/falta-74-area-verde-zona-metropolitana)), 7.75 m²/hab ([Manzanilla-Quiñones 2021](https://www.scielo.org.mx/pdf/era/v8n1/2007-901X-era-8-01-e2676.pdf)) y San Pedro / Monterrey norte ([Casillas-Zapata 2022](https://dialnet.unirioja.es/descarga/articulo/8532781.pdf)); motos ([El Norte vía vLex](https://vlex.com.mx/vid/duplican-motos-triplican-muertes-1076580954)); días sin agua ([N+](https://www.nmas.com.mx/monterrey/falta-de-agua-en-nuevo-leon-municipio-de-garcia-el-mas-afectado-por-desabasto/)); atlas ([HCNL](https://www.hcnl.gob.mx/glpan/2024/07/atlas-de-riesgo-en-nuevo-leon.php)).

**El cruce 1 es la apuesta más segura.** Todos sus insumos son gratuitos y se calculan el primer día. Además ya hay de dónde arrancar: el repo `taller-condatos` de Cómo Vamos ("Arborización estratégica para reducir islas de calor con datos satelitales") se actualizó cinco días antes de este reporte ([repos CVNL](https://api.github.com/users/EvaluacionInvestigacion-CVNL/repos)). Y existe una plantilla metodológica, el índice de vulnerabilidad al calor de Ciudad Juárez, hecho con componentes principales sobre el Censo 2020 ([UACJ](https://erevistas.uacj.mx/ojs/index.php/memoriascyt/article/download/6431/8035/29584)).

**El cruce 2 tiene la historia más fuerte para un jurado de gobierno.** Contesta con datos oficiales una pregunta que en 2022 se discutió solo con notas de prensa. Hay que nombrar el volumen como "concesionado" y validar totales por título, porque no está claro si `volsb` se repite en cada pozo de un mismo título.

**Los cruces 3 y 4 ganan por frescura.** Si el equipo arranca los scrapers de SADM y de SIMA en el minuto cero, a la hora del demo tendrá 24–48 horas de serie viva propia, algo que ninguna otra fuente le da.

## Las trampas que tumban un demo a medianoche

| Trampa | Qué pasa | Cómo esquivarla |
|---|---|---|
| **Asteriscos del Censo 2020** [V] | En municipio, localidad y AGEB, todo indicador con menos de 3 unidades sale como `*`, salvo POBTOT, VIVTOT y TVIVHAB. Las manzanas con 1 o 2 viviendas habitadas solo traen POBTOT y VIVTOT ([INEGI](https://www.inegi.org.mx/contenidos/programas/ccpv/2020/doc/fd_agebmza_urbana_cpv2020.pdf)) | Leer `*` como nulo, nunca como cero; agregar a AGEB o colonia; reportar qué porcentaje está suprimido |
| **Versiones de AGEB** | Las tablas del Censo 2020 corresponden a la geometría del MG 2020. El MG verificado más reciente es el de dic-2024, y en García, Juárez, Escobedo, Apodaca, Pesquería y El Carmen hay AGEB nuevas o recodificadas. No hay tabla oficial de equivalencias. Además, una nueva Norma Técnica del Marco Geoestadístico entró en vigor el 26-jun-2026 ([SNIEG](https://www.snieg.mx/Documentos/Normatividad/Vigente/NT_Marco_Geoestadistico.pdf)) | Unir el Censo 2020 con la geometría de 2020 (o con los SHP de GRS/IMU 2020); pasar entre versiones por traslape espacial, no por clave |
| **Ceros a la izquierda** [V] | CONAPO guarda ENT/MUN/LOC como enteros (`1`) y su llave auxiliar como float (`100100010017.0`); la AGEB es alfanumérica ([imu_2020.csv](https://www.datos.gob.mx/dataset/d8f2a534-bcee-4114-853d-82982a81ce24/resource/9600f414-c1ba-408a-8dd6-7f73d76601d4/download/imu_2020.csv)) | Leer todo como texto y rellenar a 2/3/4/4/3 |
| **La EIC 2025 no es el Censo** [V] | Solo llega a municipio y localidades de 50k o más; trae 5 renglones por geografía (valor, error estándar, límites, CV); viene en Latin-1 | Filtrar `ESTIMADOR == "Valor"`; usarla para reescalar, no para mapear AGEB |
| **API de presas congelada** [V] | Desde el 25-abr-2025 regresa `[]` | API para la historia + scraper de SADM + notas de MVS |
| **Los NAMO no cuadran** | Cerro Prieto: 295 (SADM), 300 (CONAGUA) o 393 Mm³ (NASA) ([NASA EO](https://earthobservatory.nasa.gov/images/150123/a-reservoir-runs-dry)); La Boca: 35.0 contra 36.78 | Declarar el denominador en cada porcentaje |
| **SIMA sin descarga masiva** [V] | Historia solo en PDF; el JSON entrega una estación sin parámetro documentado; en vivo usa PM2.5 24 h = 33 µg/m³, mientras el reporte de agosto 2026 usa 25 | Historia vía SINAICA; umbral de la norma como parámetro; completitud explícita en el resultado |
| **Cuotas de Earth Engine** [V] | 150 EECU-h al mes desde el 27-abr-2026; modo restringido al pasarse; sin plazo publicado para verificar el registro | Registrar el proyecto días antes; considerar Contributor; exportar compuestos antes del evento |
| **Desfase de Sentinel-2** [C] | Desde el 25-ene-2022, el L2A fuera de la colección `_HARMONIZED` de GEE trae un desfase de −1000 DN | Restar 1000 en Planetary Computer o AWS |
| **Choque de claves SMN contra INEGI** [V] | La estación SMN 19039 es Las Enramadas (Los Ramones); el municipio INEGI 19039 es Monterrey ([SMN](https://smn.conagua.gob.mx/tools/RESOURCES/Normales_Climatologicas/Diarios/nl/dia19039.txt)) | Ubicar estaciones por coordenadas, nunca por clave |
| **SINA filtra distinto en cada capa** [V] | `m01` usa `clvedo='19'`, la piezometría `clveestado='19'`, RENAMECA `estado='NUEVO LEÓN'` y los acuíferos `clvacuifero LIKE '19%'`; el servidor está detrás de Incapsula y no publica términos de uso | Revisar `DescribeFeatureType`; reproyectar de 3857; descargar una vez y cachear |
| **MIDE: reportes sin coordenadas** [V] | `reportes_ciudadanos` trae geometría nula y fechas mezcladas (`12/9/2025` y `8/23/25`); la capa 911 tiene justo 10,000 puntos (posible tope); no se localizó la licencia | Geocodificar por colonia; normalizar fechas; citar MIDE como fuente |
| **Portales que engañan** [V] | datos.nl.gob.mx es estadística económica, no el CKAN; `datosabiertos.nl.gob.mx/api` da 404; ima.nl.gob.mx da 502; metrorrey.gob.mx no resuelve; fiscalianl.gob.mx da 403 ([Fiscalía](https://fiscalianl.gob.mx/estadisticas/)) | Usar solo los hosts de este reporte; para delitos, SESNSP municipal |
| **Bloqueos federales** [V] | La API de datos.gob.mx da 403 sin User-Agent de navegador; `repodatos.atdt.gob.mx` respondió "Access Denied" desde un servidor fuera de México ([datos.gob.mx](https://www.datos.gob.mx/api/3/action/package_show?id=rezago_social)) | Mandar User-Agent; descargar desde una red mexicana antes del evento |
| **Quiebre del SESNSP** | Desde ene-2026 hay un nuevo registro de incidencia, sin puente con 2015–2025 ([Expansión](https://politica.expansion.mx/voces/2026/03/06/el-sesnsp-y-el-truco-del-ilusionista)) | No pegar las dos series |
| **Datos filtrados del ICV** | Hay una posible filtración de unos 2.4 M de licencias, investigada en ago-2026 ([Récord](https://www.record.com.mx/historia/hackearon-al-gobierno-de-nuevo-leon-investigan-posible-filtracion-de-millones-de-datos-2026081316542262111)) | Prohibidos: ni tocarlos |

**Una semana antes del evento** conviene dejar listas las cuentas:

- proyecto no comercial de Earth Engine
- NASA Earthdata Login
- Copernicus Data Space
- MAP_KEY de FIRMS
- API key de OpenAQ
- tokens de DENUE y del API de Indicadores de INEGI

**También conviene precargar en disco:**

- el Censo por AGEB de NL
- los SHP de GRS e IMU
- el DENUE
- el REPDA de SINA (35 MB)
- las capas de MIDE que se vayan a usar
- si hay tiempo y ancho de banda, el Marco Geoestadístico (3.33 GB)

Si GEE se pone lento durante el hackatón, ayuda tener exportado de antemano un compuesto de LST y uno de NDVI en GeoTIFF.

## Conclusión

El mapa de huecos es el mejor pitch. El gobierno anuncia 368 datasets y publica 132. Los datos locales más ricos vienen de un municipio y de un GeoServer federal que nadie documenta. Y las capas que más faltan son justo lo que un jurado de gobierno no puede conseguir en otro lado:

- el nivel de la Presa Libertad
- un índice de vulnerabilidad al calor por colonia
- un inventario de árboles
- el inventario de emisiones 2023, que se anunció como "concluido" pero no se ha publicado
- la historia de SIMA, atrapada en PDF
- el monitoreo de calidad del agua de RENAMECA, que cayó de unos 500 muestreos de ríos al año a 1 en 2021 ([SINA](https://geosinav30.conagua.gob.mx:8080/geoserver/Sina/ows?service=WFS&request=GetCapabilities))

Un equipo que entregue un pipeline reproducible con el método abierto le ofrece al estado algo que hoy no tiene, y eso pesa más que una visualización bonita.

La restricción real no es la disponibilidad sino la antigüedad de cada capa. El Censo es de 2020 en una periferia donde García creció 39%; JRC Global Surface Water termina en 2021; las imágenes del mapa de copa de Meta son de 2018–2020; los CSV de SADM tienen 11 meses de atraso; la API de presas lleva 18 meses congelada. Los proyectos que ganan fechan cada capa en pantalla y usan Dynamic World, Sentinel-2 y la Intercensal 2025 para traer al presente las líneas base viejas, en lugar de esconder el desfase.
