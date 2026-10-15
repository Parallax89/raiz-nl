# Free satellite and global geospatial datasets for the Monterrey metro area (hackathon inventory, as of 2026-10-14)

Legend used throughout: **[V]** = verified in a web source fetched/searched in this research session (2026-10-14). **[K]** = collection ID / spec taken from the researcher's prior knowledge with the canonical catalog URL cited; NOT re-fetched this session. Treat [K] items as "very likely correct, but click the link before the hackathon". AOI used everywhere: bbox lon -100.65 to -99.95, lat 25.45 to 26.05 (`[-100.65, 25.45, -99.95, 26.05]`). The whole AOI falls in UTM zone 14N (EPSG:32614), since zone 14 spans 102°W–96°W.

## Vegetation and green areas (Sentinel-2, Landsat, HLS, MODIS, WorldCover, Dynamic World, canopy height, urban tree cover)

### Takeaway
For per-colonia/AGEB green-space metrics, the best stack is: Sentinel-2 L2A (10 m) NDVI with Google Cloud Score+ masking in Earth Engine, Dynamic World (10 m, per-scene land-cover probabilities) or ESA WorldCover (10 m, frozen at 2020/2021) for tree/built fractions, and the Meta/WRI 1 m canopy-height map for tree canopy. HLS (30 m, 2–3 day) is the right choice for dense NDVI time series. MODIS NDVI is legacy: Terra and Aqua are drifting and end around late 2026 to 2027, so switch to VIIRS.

### Cited Findings
**Sentinel-2 L2A (ESA/Copernicus)** [K]
- 10 m (B2/B3/B4/B8), 20 m (red-edge, SWIR). About 5-day revisit with 2 satellites. Global L2A from about Dec 2018 (GEE collection starts 2017-03 but is sparse before Dec 2018). License is Copernicus free and open. Access:
  - GEE `COPERNICUS/S2_SR_HARMONIZED` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED)
  - Cloud mask: GEE `GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED` (band `cs_cdf`, threshold around 0.6) — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_CLOUD_SCORE_PLUS_V1_S2_HARMONIZED)
  - Planetary Computer STAC `sentinel-2-l2a` — [PC catalog](https://planetarycomputer.microsoft.com/dataset/sentinel-2-l2a)
  - AWS / Element84 Earth Search STAC `https://earth-search.aws.element84.com/v1`, collections `sentinel-2-l2a` / `sentinel-2-c1-l2a` — [AWS Registry](https://registry.opendata.aws/sentinel-2-l2a-cogs/)
  - Copernicus Data Space Ecosystem (free account; also openEO and Sentinel Hub APIs) — [CDSE](https://dataspace.copernicus.eu)
- **Pitfall [K]:** ESA processing baseline 04.00 (from 25 Jan 2022) adds a -1000 DN offset (`BOA_ADD_OFFSET`) to L2A reflectances. GEE's `_HARMONIZED` collection removes it. Raw Planetary Computer/AWS items do NOT. Subtract 1000 before computing NDVI on post-2022 scenes, or the time series will jump. See the [GEE S2 harmonized notes](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR_HARMONIZED).

**Landsat 8/9 Collection 2 Level-2 (USGS/NASA)** [K]
- 30 m reflectance. 8-day combined revisit with L8+L9. Archive from 2013 (L8) and 2021 (L9). Public domain.
  - GEE `LANDSAT/LC08/C02/T1_L2`, `LANDSAT/LC09/C02/T1_L2` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2)
  - PC `landsat-c2-l2` — [PC catalog](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2)
  - AWS `s3://usgs-landsat` (requester pays) — [AWS Registry](https://registry.opendata.aws/usgs-landsat/)
- Reflectance scale: `SR_B* × 0.0000275 − 0.2`.

**HLS v2.0 (Harmonized Landsat Sentinel-2, NASA LP DAAC)** [K]
- 30 m surface reflectance harmonized across Landsat 8/9 and Sentinel-2. Combined revisit about 2–3 days. Global land (Monterrey covered). NASA open data.
  - GEE `NASA/HLS/HLSL30/v002` and `NASA/HLS/HLSS30/v002` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/NASA_HLS_HLSL30_v002)
  - NASA Earthdata CMR-STAC (LPCLOUD), `HLSL30_2.0` / `HLSS30_2.0` — [Earthdata](https://www.earthdata.nasa.gov/data/projects/hls)
  - AppEEARS for polygon time series without code — [AppEEARS](https://appeears.earthdatacloud.nasa.gov/)
- Requires a free Earthdata Login (instant) outside GEE.

**MODIS vegetation indices (NASA)** [K for IDs; V for end of life]
- MOD13Q1 / MYD13Q1: 250 m, 16-day NDVI/EVI, 2000–present. GEE `MODIS/061/MOD13Q1` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD13Q1)
- Continuity product: VIIRS VNP13A1, 500 m — GEE `NASA/VIIRS/002/VNP13A1` [K]
- **End-of-life status [V]:** Terra and Aqua are drifting from their controlled sun-synchronous orbits because of fuel limits. NASA advises users to assess the impact of these overpass-time changes and to move to VIIRS. Stated end dates differ by source:
  - CAMS: Terra January 2027, Aqua about September 2027 — [CAMS](https://atmosphere.copernicus.eu/drifting-away-modis-cams-global-fire-assimilation-system)
  - NASA LAADS: Terra February 2027, Aqua September 2027 — [LAADS MODIS→VIIRS](https://ladsweb.modaps.eosdis.nasa.gov/learn/modis-to-viirs-transition/)
  - NASA Earthdata alert: "late 2026/early 2027" — [Earthdata alert](https://www.earthdata.nasa.gov/data/alerts-outages/transition-from-modis-viirs)
  - A June 2026 ICAP talk says the missions end later in 2026 — [Levy ICAP June 2026](https://events.ecmwf.int/event/541/contributions/6192/attachments/3726/6366/Levy_ICAP_June2026A.pdf)
  - NASA states the VIIRS land products were built for continuity with MODIS — [Earthdata blog](https://earthdata.nasa.gov/news/blog/from-modis-viirs-continuing-legacy)

**ESA WorldCover (ESA/VITO)** [K]
- 10 m, 11 classes (tree cover, grassland, built-up, bare, water…). Only 2020 (v100) and 2021 (v200) exist. License CC BY 4.0.
  - GEE `ESA/WorldCover/v200` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200)
  - PC `esa-worldcover` — [PC catalog](https://planetarycomputer.microsoft.com/dataset/esa-worldcover)
  - AWS `s3://esa-worldcover` — [AWS Registry](https://registry.opendata.aws/esa-worldcover-vito/)

**Google Dynamic World V1 (Google/WRI)** [K]
- 10 m, one land-cover image per Sentinel-2 scene, 2015-06-27 to present, near real time. 9 classes with per-class probabilities (`trees`, `grass`, `built`, `water`, …) plus a `label` band. License CC BY 4.0.
  - GEE `GOOGLE/DYNAMICWORLD/V1` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_DYNAMICWORLD_V1)
- Best option for "green cover change 2016→2026 per colonia".

**Esri / Impact Observatory 10 m annual LULC** [K]
- Annual maps from 2017 onward (Sentinel-2). CC BY 4.0.
  - PC `io-lulc-annual-v02` — [PC catalog](https://planetarycomputer.microsoft.com/dataset/io-lulc-annual-v02)
  - Esri Living Atlas — [Living Atlas](https://livingatlas.arcgis.com/landcover/)

**Meta + WRI + Land & Carbon Lab global canopy height** [V]
- 1 m, global. Imagery from 2009–2020, with 80% from 2018–2020. Meta reports a mean absolute error of 2.8 m. Data and models are free, including for commercial use — [ESG News](https://esgnews.com/meta-wri-and-land-carbon-lab-launch-global-ai-powered-tree-canopy-height-map); [Carbon Credits](https://carboncredits.com/ai-powered-global-tree-canopy-map-unveiled-by-meta-wri-for-forest-carbon-credit)
- GEE community catalog: `ee.ImageCollection("projects/sat-io/open-datasets/facebook/meta-canopy-height")`, layer `canopy_ht_1m` — [GEE Community Catalog: meta_trees](https://gee-community-catalog.org/projects/meta_trees/)
- Also on AWS: `s3://dataforgood-fb-data/forests/v1/` [K]

**ETH Global Canopy Height 2020 (Lang et al.)** [K]
- 10 m, from Sentinel-2 + GEDI. GEE community asset `users/nlang/ETH_GlobalCanopyHeight_2020_10m_v1` — [GEE community catalog](https://gee-community-catalog.org/projects/canopy/)
- A coarser but consistent alternative to Meta 1 m.

**GEDI L2A/L2B/L4A (NASA lidar)** [K]
- 25 m footprints, 51.6°N–51.6°S, so Monterrey is covered. Footprint samples, not wall-to-wall. GEE `LARSE/GEDI/GEDI02_A_002_MONTHLY` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/LARSE_GEDI_GEDI02_A_002_MONTHLY)
- Use to validate canopy heights.

**Hansen Global Forest Change (UMD)** [K]
- 30 m tree cover 2000 and annual loss. GEE `UMD/hansen/global_forest_change_2024_v1_12` (the latest version ID may have advanced) — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/UMD_hansen_global_forest_change_2024_v1_12)
- Relevant for the Sierra Madre / Parque Nacional Cumbres de Monterrey edge, not for urban trees.

**Urban tree cover via Google Environmental Insights Explorer (EIE)** [V, partly dated]
- A circa-2023 source says EIE's tree canopy layer uses aerial imagery and was "currently piloting in selected US cities" — [CAKEX](https://www.cakex.org/tools/google-environmental-insights-explorer)
- I found no evidence that Monterrey has an EIE tree-canopy layer.

### Inferences
- In Monterrey, steep terrain (Cerro de la Silla, Las Mitras, Sierra Madre) plus irrigated parks versus xeric scrub means NDVI alone confuses "green" with "irrigated". Pair NDVI with the Dynamic World `trees` probability and Meta canopy height (for example "% of AGEB with canopy > 3 m") to separate trees from lawns and matorral.
- Dry-season composites (March–May) best separate irrigated urban green from the semi-arid background. Wet-season composites (around September) inflate natural vegetation.
- WorldCover is a fixed 2020/2021 snapshot. Use Dynamic World or Esri/IO annual LULC for change since then.

### Gaps
- I did not confirm whether NASA's HLS Vegetation Indices product (HLS-VI) is live in GEE or Planetary Computer as of Oct 2026.
- I did not confirm the current Hansen GFC version ID.
- I did not confirm whether EIE now has tree canopy data for any Mexican city.
- No dedicated, published 1 m urban tree-cover dataset for Monterrey was found. Local sources (municipal tree inventories, Tec/UANL) were outside this scope.

## Heat (Landsat LST, ECOSTRESS, MODIS LST, ERA5-Land, urban heat island methods)

### Takeaway
Landsat 8/9 C2 L2 `ST_B10` is the workhorse for intra-urban heat maps per AGEB. It is natively 100 m TIRS resampled to 30 m, with about a 10:30–11:00 local overpass and an 8-day combined revisit. Use a multi-year summer median composite. Add MODIS/VIIRS 1 km LST for day/night and long trends, ERA5-Land (about 9 km, hourly) for air temperature and heat-wave context, and ECOSTRESS (70 m, variable time of day, including afternoons) if you can get scenes. A published Monterrey study (ISPRS 2024) already links LST to green-blue infrastructure and urban growth, and gives the team a citable baseline.

### Cited Findings
**Landsat 8/9 C2 L2 surface temperature** [K]
- Same collections as above. Band `ST_B10`; Kelvin = `ST_B10 × 0.00341802 + 149.0`. Cloud mask from `QA_PIXEL` bits 0–4 (fill, dilated cloud, cirrus, cloud, cloud shadow) — [GEE LC09 C02 T1_L2](https://developers.google.com/earth-engine/datasets/catalog/LANDSAT_LC09_C02_T1_L2)
- Planetary Computer `landsat-c2-l2`: band `lwir11`, same scale — [PC](https://planetarycomputer.microsoft.com/dataset/landsat-c2-l2)

**ECOSTRESS (NASA JPL, on ISS)** [K]
- About 70 m LST&E (L2 LSTE v002). Revisit is irregular, and the precessing ISS orbit gives samples at different times of day, including afternoon/evening, which is valuable for heat-stress peaks.
- Access via NASA Earthdata (LP DAAC) and AppEEARS — [LP DAAC ECOSTRESS](https://lpdaac.usgs.gov/products/eco_l2t_lstev002/); [AppEEARS](https://appeears.earthdatacloud.nasa.gov/)
- Mission status: I could not confirm 2026 status. The FY2026 White House request proposed cutting NASA science by about 47% and terminating dozens of missions. Congress pushed back, but the outcome for specific missions was not found — [Space.com](https://space.com/space-exploration/congress-rejects-president-trumps-deep-nasa-budget-cuts-proposes-usd24-4-billion-for-the-agency); [Universe Today](https://universetoday.com/articles/nasas-fy-2026-budget-request-has-been-released)

**MODIS LST** [K IDs; V end-of-life]
- MOD11A1 / MYD11A1: 1 km, daily, day and night, nominal overpasses about 10:30/22:30 (Terra) and 13:30/01:30 (Aqua). GEE `MODIS/061/MOD11A1`, `MODIS/061/MYD11A1` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MOD11A1)
- Drifting overpass times are degrading trend analysis, and the missions end around late 2026–2027 — [LAADS](https://ladsweb.modaps.eosdis.nasa.gov/learn/modis-to-viirs-transition/)
- Continuity is VIIRS LST (VNP21 / VJ121 family) [K].

**ERA5-Land (ECMWF / Copernicus C3S)** [K]
- 0.1° (about 9 km), hourly, 1950–present. Latency about 5 days. 2 m temperature, dewpoint, wind, soil moisture, precipitation.
  - GEE `ECMWF/ERA5_LAND/HOURLY`, `ECMWF/ERA5_LAND/DAILY_AGGR` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_ERA5_LAND_HOURLY)
  - Copernicus Climate Data Store API (the new CDS needs a new account/API key since the 2024 migration) — [CDS](https://cds.climate.copernicus.eu/)

**GOES-East ABI LST (NOAA)** [K]
- About 2 km, hourly full-disk LST. Free on AWS (`noaa-goes19`, no account) — [AWS Registry NOAA GOES](https://registry.opendata.aws/noaa-goes/)
- Gives a true diurnal heat cycle over Monterrey. GOES-19 replaced GOES-16 as GOES-East in 2025 [K].

**Yale YCEO Surface UHI dataset** [K]
- MODIS-derived, city-level summer/winter, day/night SUHI intensities (2003–2018). GEE `YALE/YCEO/UHI/...` — [GEE catalog search "YCEO"](https://developers.google.com/earth-engine/datasets/tags/uhi)
- Quick benchmark of Monterrey's SUHI against other cities.

**Monterrey literature** [V]
- Zapata Wah, Yépez Rincón and Huerta-García (ISPRS Annals X-3-2024) analyze LST for 2003, 2013 and 2021 against green-blue infrastructure (GBI) in the Monterrey Metropolitan Area. They report that urbanization decreases the cooling effect of urban rivers and green areas — [ISPRS Annals 2024](https://isprs-annals.copernicus.org/articles/X-3-2024/439/2024/)
- The same group published a 2026 heat-index assessment for the Monterrey Metropolitan Area during heat waves — [ISPRS Annals X-3-W3-2025](https://isprs-annals.copernicus.org/articles/X-3-W3-2025/165/2026/isprs-annals-X-3-W3-2025-165-2026-relations.html)
- Methodological analogue in Mexico: Mérida Landsat study found LST rose about 4 °C (dry season) and 3 °C (wet season) with land-use change, with a positive LST–NDVI relationship mainly in the dry season — [MDPI IJGI](https://mdpi-res.com/d_attachment/ijgi/ijgi-10-00076/article_deploy/ijgi-10-00076.pdf)

### Inferences
- **Standard SUHI recipe for the hackathon:**
  1. Build a Landsat L8+L9 LST median for May–September over 2023–2026 (to beat clouds).
  2. Compute mean LST per AGEB with `reduceRegions` at 30 m.
  3. Compute SUHI = AGEB LST minus the mean LST of a rural reference. The reference is non-urban pixels (Dynamic World or WorldCover not built) in a 10–20 km buffer, excluding the mountains above about 1,000 m to avoid elevation cooling bias.
  4. Correlate with NDVI and canopy share.
- Elevation strongly confounds LST in Monterrey (the valley is about 500–600 m; the sierras exceed 2,000 m). Include a DEM covariate (Copernicus GLO-30) or restrict to urban AGEBs.
- Landsat LST is a morning-surface measure, not afternoon air temperature. Frame results as "surface heat exposure" and use ERA5-Land or ground stations for heat-wave air temperature.

### Gaps
- I did not confirm ECOSTRESS operational status in Oct 2026, or whether new scenes over Monterrey exist for 2025–2026.
- I did not confirm the exact GEE ID or current version of the Yale UHI dataset.
- I found no Monterrey study pairing Landsat LST with NDVI at AGEB level. The ISPRS abstract does not confirm NDVI use.

## Air quality (Sentinel-5P, MAIAC/VIIRS AOD, TEMPO, OpenAQ, CAMS, ground sensors)

### Takeaway
- **Sentinel-5P TROPOMI** (about 5.5×3.5 km, daily around 13:30) is the zero-friction choice in GEE for NO2/SO2/CO/CH4/HCHO/aerosol index over Monterrey.
- **TEMPO** (geostationary, hourly daytime, about 2×4.75 km at the center of its field) covers Monterrey. Its field of regard reaches south to Mexico City, about 6° south of Monterrey. TEMPO adds the diurnal cycle but needs Earthdata download and 2026 mission status is unconfirmed.
- **Ground data** come from Nuevo León's SIMA network (aire.nl.gob.mx) and INECC/SINAICA. These are visible on AQICN, but SIMA data completeness has been criticized.
- **OpenAQ coverage** of Monterrey and **PurpleAir density** were not confirmed.

### Cited Findings
**Sentinel-5P TROPOMI (ESA/Copernicus)** [K]
- About 5.5×3.5 km since Aug 2019. Daily, about 13:30 local overpass. 2018–present.
- GEE Level-3 (OFFL, latency days): `COPERNICUS/S5P/OFFL/L3_NO2`, `.../L3_SO2`, `.../L3_CO`, `.../L3_CH4`, `.../L3_HCHO`, `.../L3_AER_AI`, `.../L3_O3`, `.../L3_CLOUD`
- Near-real-time (latency hours): `COPERNICUS/S5P/NRTI/L3_*` — [GEE catalog S5P OFFL NO2](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S5P_OFFL_L3_NO2)
- L2 NetCDF: Planetary Computer `sentinel-5p-l2-netcdf` — [PC](https://planetarycomputer.microsoft.com/dataset/sentinel-5p-l2-netcdf)
- License: Copernicus free and open.

**TEMPO (NASA / Smithsonian SAO)** [V]
- Geostationary at 91°W. Scans the field of regard east to west every daylight hour. Nominal pixels are about 2 km N–S × 4.75 km E–W at the field-of-regard center (about 33.5°N, 89.2°W), coarser toward the edges — [TEMPO instrument (SAO)](https://tempo.si.edu/instrument.html); [NASA Earthdata forum](https://forum.earthdata.nasa.gov/viewtopic.php?p=25494)
- Coverage is described as "from Mexico City and Cuba to the Canadian tar sands" and "Central Canada to Mexico City" — [NASA SPoRT TEMPO 2024](https://ntrs.nasa.gov/api/citations/20240001639/downloads/TEMPO_AMS_SPoRT_2024.pdf); [CEOS training](https://training.ceos.org/events/2388)
- First NO2 light on 2 August 2023. NASA visualizations show high NO2 over Mexican urban areas. No retrievals under clouds — [NASA SVS 5142](https://svs.gsfc.nasa.gov/5142/)
- Early-morning scans cover only the east and late-day scans only the west. Effective hourly coverage of a given point varies by time of day — [Earthdata forum](https://forum.earthdata.nasa.gov/viewtopic.php?p=25494)
- Access [K]:
  - NASA ASDC via Earthdata Search or the `earthaccess` Python library; L2/L3 NO2, HCHO, O3 total, clouds — [Earthdata TEMPO](https://www.earthdata.nasa.gov/data/instruments/tempo?level=2)
  - Not in the official GEE catalog to my knowledge.

**MAIAC AOD (MODIS)** [K]
- MCD19A2: 1 km, daily AOD 470/550 nm. GEE `MODIS/061/MCD19A2_GRANULES` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/MODIS_061_MCD19A2_GRANULES)
- Ends with Terra/Aqua (see MODIS end-of-life above).
- Continuity [V]: VIIRS aerosol products agree with MODIS C6.1 within about ±0.02 AOD — [Levy ICAP June 2026](https://events.ecmwf.int/event/541/contributions/6192/attachments/3726/6366/Levy_ICAP_June2026A.pdf)

**GOES-East ABI AOD (NOAA)** [K]
- 2 km, every 10 minutes (full disk). Free on AWS `noaa-goes19` — [AWS Registry](https://registry.opendata.aws/noaa-goes/)
- Useful for dust and smoke events (Saharan dust, agricultural/wildfire smoke reaching Monterrey).

**CAMS (ECMWF Copernicus Atmosphere)** [K]
- Global forecasts (about 0.4°) and the EAC4 reanalysis (about 0.75°, 2003 onward) for PM2.5, PM10, NO2, O3, AOD.
  - GEE `ECMWF/CAMS/NRT` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/ECMWF_CAMS_NRT)
  - Atmosphere Data Store API (free account) — [ADS](https://ads.atmosphere.copernicus.eu/)
- Too coarse for intra-urban maps. Good for regional context and for event attribution (dust, smoke).

**OpenAQ** [V docs; K for API change]
- The v3 API exposes station locations with coordinates, operator and per-parameter sensors — [OpenAQ docs: locations](https://docs.openaq.org/resources/locations)
- [K] v1/v2 were retired in early 2025. v3 requires a free API key (`X-API-Key` header) and supports bbox queries, e.g. `GET https://api.openaq.org/v3/locations?bbox=-100.65,25.45,-99.95,26.05`.

**SIMA Nuevo León (state network)** [V]
- Run by the state Secretaría de Desarrollo Sustentable. Publishes pollutant concentrations for the metro area and monthly reports — [aire.nl.gob.mx monthly report](https://aire.nl.gob.mx/docs/reportes/mensuales/2020/04_Reporte_Abril_2020.pdf)
- Press reports say SIMA modules gave incomplete data, with some stations measuring only CO at one point — [Milenio](https://www.milenio.com/politica/comunidad/modulos-sima-arroja-datos-incompletos-contaminacion-nuevo-leon)

**AQICN / WAQI**
- Lists Monterrey-area stations (e.g., Universidad, Cadereyta, Metrorrey) with data credited to the Nuevo León government and INECC — [AQICN Metrorrey](https://aqicn.org/city/@6490); [AQICN Cadereyta](https://aqicn.org/city/mexico/nuevo-leon/monterrey/cadereyta/)
- Sensor aggregator Sensoto lists "706 sensors" for Nuevo León (mix of sources, unverified quality) — [Sensoto](https://sensoto.io/en/overview/Nuevo_León-aaecee)

**Literature context** [V]
- Ozone trends 1993–2014 in Monterrey vs Mexico City and Guadalajara. Highest O3 in spring — [Tec research](https://research.tec.mx/vivo-tec/display/AcademicArticleSCO_85026551177)

### Inferences
- **TEMPO coverage.** Correction to one search summary: Monterrey (about 25.7°N, 100.3°W) is NORTH of Mexico City (19.4°N) and well inside TEMPO's east–west scan. It is therefore inside the field of regard, with pixels somewhat larger than nominal because it sits away from the center.
- **Hackathon NO2 story.** TROPOMI 2019–2026 monthly NO2 means over the metro, plus TEMPO hourly NO2 for a few clear-sky weeks, can show the industrial corridor and rush-hour cycle. Candidate sources are the Cadereyta refinery area on the east edge of the bbox, the Apodaca/Escobedo industrial zones, and the highways. Validate against SIMA/SINAICA hourly data.
- **TROPOMI resolution limit.** At about 5 km, TROPOMI cannot resolve AGEB-level differences. Present it at metro/municipality scale, or use oversampling (averaging many orbits) for about 1–2 km effective detail.

### Gaps
- I could not confirm whether OpenAQ v3 ingests SIMA/SINAICA stations for Monterrey. Test with the bbox query above.
- PurpleAir sensor count in Monterrey and current PurpleAir API pricing/keys were not found.
- TEMPO's operating status and product version (V03 vs V04) in Oct 2026 are unconfirmed, given FY2026 NASA budget turbulence.
- GEE availability of TEMPO is unconfirmed.

## Water (JRC Global Surface Water, Sentinel-1 floods, GRACE-FO, CHIRPS, IMERG, SMAP)

### Takeaway
Monterrey's water story (reservoir drawdown, droughts, flash floods in the Santa Catarina river and arroyos) is best told with:
- JRC GSW (30 m, 1984–2021) and Sentinel-2/Landsat water indices for reservoir area
- Sentinel-1 (10 m SAR, all-weather) for flood extent
- CHIRPS (about 5 km daily) and IMERG (about 10 km, 30 min, hours latency) for rainfall
- GRACE-FO, at basin scale only (about 300 km effective)

Note that the main supply reservoirs (El Cuchillo, Cerro Prieto, La Boca) sit at or outside the metro bbox. Enlarge the AOI for water-supply analysis.

### Cited Findings
**JRC Global Surface Water v1.4 (EC JRC / Google)** [K]
- 30 m, 1984–2021: occurrence, change, seasonality, monthly history.
  - GEE `JRC/GSW1_4/GlobalSurfaceWater`, `JRC/GSW1_4/MonthlyHistory`, `JRC/GSW1_4/YearlyHistory` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/JRC_GSW1_4_GlobalSurfaceWater)
- No 2022+ data, so for the 2022 drought and later use Sentinel-2 MNDWI or Dynamic World `water`.

**Sentinel-1 GRD / RTC (ESA)** [K]
- 10 m C-band SAR, VV+VH, IW mode, 2014 onward.
  - GEE `COPERNICUS/S1_GRD` (already terrain-corrected, dB) — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S1_GRD)
  - Planetary Computer `sentinel-1-rtc` (radiometric terrain corrected) — [PC](https://planetarycomputer.microsoft.com/dataset/sentinel-1-rtc)
  - CDSE (free) — [CDSE](https://dataspace.copernicus.eu)
- Sentinel-1C launched December 2024 [K]. Actual revisit over Mexico depends on the acquisition plan (often 12 days).

**NASA OPERA suite** [K except DISP]
- DSWx-HLS (30 m surface water, global)
- DSWx-S1 and RTC-S1 (North America)
- DIST-ALERT (vegetation disturbance, global)
- Via NASA Earthdata/ASF — [Earthdata OPERA](https://www.earthdata.nasa.gov/data/projects/opera?page=%2C1)

**GRACE / GRACE-FO** [K]
- Monthly terrestrial water storage anomalies. JPL mascons on a 0.5° grid, but true resolution is about 300 km.
  - GEE `NASA/GRACE/MASS_GRIDS_V04/MASCON_CRI` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/NASA_GRACE_MASS_GRIDS_V04_MASCON_CRI)
- Basin-level (Río Bravo/San Juan) only. Not usable per municipality.

**CHIRPS (UCSB Climate Hazards Center)** [K]
- 0.05° (about 5.5 km), daily/pentad, 1981–present, 50°S–50°N. Latency weeks (final) / days (prelim).
  - GEE `UCSB-CHG/CHIRPS/DAILY` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/UCSB-CHG_CHIRPS_DAILY)
- License: public domain-like (CC0/"no restrictions" as stated by CHC) [K].

**GPM IMERG V07 (NASA)** [K]
- 0.1°, 30-minute. Latency: Early run about 4 h, Late about 12–14 h, Final about 3.5 months.
  - GEE `NASA/GPM_L3/IMERG_V07` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/NASA_GPM_L3_IMERG_V07)
- Captures storm events such as tropical cyclone rain over Monterrey.

**SMAP soil moisture (NASA)** [K]
- L3 36 km / 9 km enhanced, L4 9 km 3-hourly model-assimilated.
  - GEE `NASA/SMAP/SPL4SMGP/...` and `NASA/SMAP/SPL3SMP_E/...` (check current version suffix) — [GEE SMAP tag](https://developers.google.com/earth-engine/datasets/tags/smap)
- Regional drought context only.

**Monterrey context found** [V]
- A Tec de Monterrey 2020 Google.org/ICLEI-funded project using EIE involved the Tec Water Center director — [Conecta Tec](https://conecta.tec.mx/en/news/national/research/tec-engineers-google-and-ngos-working-lowering-polluting-emissions)

### Inferences
- For the hackathon, an "agua" track could use:
  - Sentinel-2 MNDWI / Dynamic World `water` monthly area of the El Cuchillo, Cerro Prieto and La Boca reservoirs, 2017–2026, with CHIRPS rainfall overlays
  - Sentinel-1 before/after flood maps for a recent storm event over the Santa Catarina river. Expect strong layover/shadow from the mountains on the south side, so use RTC data and mask steep slopes with a DEM.
- Expand the AOI eastward (El Cuchillo is around -99.3°) and southward (Cerro Prieto near Linares) for reservoir work. These are outside the stated metro bbox.

### Gaps
- I did not confirm Sentinel-1C's acquisition plan over northern Mexico (whether 6-day revisit is restored).
- I did not confirm whether Copernicus EMS or the International Charter mapped recent Monterrey floods.
- I did not confirm the CHIRPS v3 release/ID in GEE.
- I did not confirm the current SMAP collection version suffixes in GEE.

## Urbanization and population (GHSL, Open Buildings, Microsoft footprints, Overture, OSM, WorldPop, Meta HRSL, VIIRS night lights)

### Takeaway
- **Buildings:** use Overture Maps buildings (monthly GeoParquet releases that merge OSM + Microsoft + Google + Esri footprints) via a one-line CLI bbox download.
- **Growth and density:** GHSL R2023A (built-up surface, height, population in 5-year epochs 1975–2030).
- **Temporal building change:** Google Open Buildings 2.5D Temporal (annual 2016–2023, 4 m effective, with heights; Latin America covered).
- **Night lights:** VIIRS Black Marble (daily/monthly 500 m) for activity and blackout proxies.
- **Census:** INEGI census AGEB data should remain the population denominator. Gridded WorldPop/GHSL/Meta are for cross-checks.

### Cited Findings
**Google Open Buildings 2.5D Temporal V1** [V]
- Annual 2016–2023. Bands `building_presence`, `building_fractional_count`, `building_height` (0–100 m). Effective resolution 4 m (rasters at 0.5 m). Coverage: Africa, South Asia, South-East Asia, Latin America and the Caribbean. Dual-licensed CC BY 4.0 / ODbL v1.0. GEE `GOOGLE/Research/open-buildings-temporal/v1` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings-temporal_v1)
- The page does not name Mexico explicitly [V].

**Google Open Buildings v3 polygons** [K]
- Footprint polygons with confidence scores. Latin America added in v3. GEE `GOOGLE/Research/open-buildings/v3/polygons` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons)
- Download tiles at [sites.research.google/open-buildings](https://sites.research.google/open-buildings/).

**Microsoft Global ML Building Footprints** [K]
- About 1.4B footprints, ODbL. GitHub `microsoft/GlobalMLBuildingFootprints` (per-country quadkey CSV/GeoJSON) — [GitHub](https://github.com/microsoft/GlobalMLBuildingFootprints)
- Planetary Computer `ms-buildings` — [PC](https://planetarycomputer.microsoft.com/dataset/ms-buildings)

**Overture Maps Foundation** [K]
- Monthly releases. Themes: addresses, base, buildings, divisions, places, transportation. GeoParquet on S3 `s3://overturemaps-us-west-2/release/<version>/` and Azure.
- Licenses: ODbL for OSM-derived themes (buildings, transportation, base); CDLA-Permissive-2.0 for places.
- Fast path: `pip install overturemaps`, then `overturemaps download --bbox=-100.65,25.45,-99.95,26.05 -f geoparquet --type=building -o mty_buildings.parquet` (also `--type=place`, `--type=segment`). DuckDB also works directly on S3 — [Overture docs](https://docs.overturemaps.org/getting-data/)

**OpenStreetMap** [K]
- Geofabrik Mexico extract (daily, `.osm.pbf`) — [Geofabrik](https://download.geofabrik.de/north-america/mexico.html)
- Overpass API for targeted queries (parks `leisure=park`, trees `natural=tree`, hospitals, schools) — [Overpass Turbo](https://overpass-turbo.eu/)
- ODbL. Use `osmnx` for street networks and walkability to parks.

**GHSL R2023A (EC JRC)** [K]
- GHS-BUILT-S (10 m for 2018; 100 m for 1975–2030 epochs), GHS-BUILT-H (building height, 100 m, 2018), GHS-POP (100 m / 1 km, 1975–2030), GHS-SMOD (degree of urbanisation). CC BY 4.0.
  - GEE `JRC/GHSL/P2023A/GHS_BUILT_S`, `JRC/GHSL/P2023A/GHS_POP`, `JRC/GHSL/P2023A/GHS_BUILT_H`, `JRC/GHSL/P2023A/GHS_SMOD_V2-0` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/JRC_GHSL_P2023A_GHS_BUILT_S)
  - Downloads at [ghsl.jrc.ec.europa.eu](https://ghsl.jrc.ec.europa.eu/download.php)
  - GHS Urban Centre Database (UCDB) has Monterrey urban-centre indicators — [GHSL UCDB](https://ghsl.jrc.ec.europa.eu/ghs_stat_ucdb2015mt_r2019a.php)

**WorldPop** [K]
- 100 m population counts, 2000–2020 (unconstrained/constrained) and age/sex structures. CC BY 4.0.
  - GEE `WorldPop/GP/100m/pop`, `WorldPop/GP/100m/pop_age_sex` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/WorldPop_GP_100m_pop)
  - Downloads at [worldpop.org](https://www.worldpop.org/)

**Meta (Data for Good) High Resolution Population Density** [K]
- About 30 m population and demographic layers (women, children under 5, elderly 60+…). CC BY 4.0.
  - HDX — [HDX Meta HRSL](https://data.humdata.org/organization/meta)
  - AWS `s3://dataforgood-fb-data/hrsl-cogs/` — [AWS Registry](https://registry.opendata.aws/dataforgood-fb-hrsl/)

**VIIRS night lights** [K]
- NASA Black Marble VNP46A2 (daily, gap-filled, BRDF/moon corrected, about 500 m), VNP46A3/A4 (monthly/annual).
  - GEE `NASA/VIIRS/002/VNP46A2` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/NASA_VIIRS_002_VNP46A2)
- NOAA/Colorado School of Mines EOG monthly and annual composites. GEE `NOAA/VIIRS/DNB/MONTHLY_V1/VCMSLCFG` and `NOAA/VIIRS/DNB/ANNUAL_V22` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/NOAA_VIIRS_DNB_MONTHLY_V1_VCMSLCFG)
- EOG direct downloads need a free registration.

**Tsinghua GAIA impervious surface** [K]
- 30 m annual impervious expansion 1985–2018. GEE `Tsinghua/FROM-GLC/GAIA/v10` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/Tsinghua_FROM-GLC_GAIA_v10)

### Inferences
- The strongest "urban sprawl" visual is GHSL BUILT-S epochs 1975→2020 plus Open Buildings Temporal 2016→2023 plus Dynamic World `built` 2016→2026 over the metro. Sprawl toward García, Juárez, Apodaca, Escobedo, Pesquería and Salinas Victoria should show clearly.
- Building heights (Open Buildings Temporal or GHS-BUILT-H) plus LST give a fast "urban canyon / heat" covariate.
- Night lights per AGEB are a defensible socioeconomic proxy. Prefer the INEGI census for real indicators, and use night lights for change detection (e.g., new industrial parks, nearshoring growth in Apodaca/Escobedo/Santa Catarina).

### Gaps
- I did not confirm Mexico's inclusion in Open Buildings v3 and Temporal V1. "Latin America" is stated, but the precise country list was not checked. Run a quick GEE `filterBounds` on the AOI to test.
- I did not confirm whether WorldPop's newer global 2015–2030 release (if any) is in GEE.
- I did not confirm the current Overture release version, or how many Monterrey buildings come from OSM vs ML sources.
- OSM building completeness in Monterrey was not assessed.

## Terrain and risk (Copernicus DEM, NASADEM, ALOS, InSAR deformation, FIRMS fires)

### Takeaway
- **DEM:** Copernicus GLO-30 (30 m DSM) is the default, available in GEE, Planetary Computer and AWS. Use FABDEM (bare-earth) for urban flood or slope analysis.
- **Deformation:** there is no EGMS-like product for Mexico. However, NASA OPERA DISP-S1 (30 m Sentinel-1 displacement time series, 2016 onward) is defined to cover North America including the mainland from the US southern border to Panama, so Monterrey should be covered. Check the ASF Displacement Portal or Vertex.
- **Fires:** NASA FIRMS gives VIIRS (375 m) and MODIS active fires with under 3 h latency through a free MAP_KEY API.

### Cited Findings
**DEMs** [K]
- Copernicus DEM GLO-30 (2011–2015 TanDEM-X, DSM, 30 m):
  - GEE `COPERNICUS/DEM/GLO30` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_DEM_GLO30)
  - PC `cop-dem-glo-30` — [PC](https://planetarycomputer.microsoft.com/dataset/cop-dem-glo-30)
  - AWS `s3://copernicus-dem-30m` — [AWS Registry](https://registry.opendata.aws/copernicus-dem/)
- NASADEM: GEE `NASA/NASADEM_HGT/001` — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/NASA_NASADEM_HGT_001)
- ALOS AW3D30: GEE `JAXA/ALOS/AW3D30/V3_2` (version may have advanced) — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/JAXA_ALOS_AW3D30_V3_2)
- FABDEM (Copernicus DEM with buildings and forests removed, 30 m, CC BY-NC-SA 4.0, so non-commercial only) — [GEE community catalog FABDEM](https://gee-community-catalog.org/projects/fabdem/)

**InSAR / ground deformation** [V]
- OPERA L3 DISP-S1: 30 m posting, from Sentinel-1 IW acquisitions starting mid-2016. Catalog notes data 2016–2025. Spatial extent: the US, US territories within 200 km of the border, Canada, and "mainland nations from the southern U.S. border down to Panama". Search/download via the ASF Displacement Portal / Vertex — [NASA Earthdata catalog DISP-S1](https://www.earthdata.nasa.gov/data/catalog/asf-opera-l3-disp-s1-v1-1); [data.gov entry](https://catalog.data.gov/dataset/opera-surface-displacement-from-sentinel-1-validated-product-version-1-c00ca); [Earthdata roundup June 2025](https://earthdata.nasa.gov/news/earth-science-data-roundup-june-2025)
- No frame-level map for Mexico was found. Frame IDs (e.g., 10854 over Texas) appear in third-party catalogs — [TACC CKAN example](https://ckan.tacc.utexas.edu/dataset/subsidence-rates--subside-h2i-2016-07-22-2025-05-30-f1b3f483-4670-4b73-a7a9-988be92194d6-007/resource/c20c33f3-34b1-4c5c-8c2a-4d8a5e3555bb)
- EGMS (European Ground Motion Service) covers Copernicus participating states only, so Mexico is not covered [K] — [EGMS](https://land.copernicus.eu/en/products/european-ground-motion-service)
- On-demand alternative: ASF HyP3 (free, Earthdata login, monthly credits) generates Sentinel-1 interferograms — [HyP3](https://hyp3-docs.asf.alaska.edu/) [K]

**NASA FIRMS active fires** [K]
- VIIRS S-NPP / NOAA-20 / NOAA-21 (375 m) and MODIS (1 km). Global near real time (under about 3 h). The faster "URT/RT" products are for the US/Canada. Archive from 2000 (MODIS) and 2012 (VIIRS).
- API needs a free MAP_KEY (email, instant), with a transaction limit per 10-minute window. Example:
  `https://firms.modaps.eosdis.nasa.gov/api/area/csv/<MAP_KEY>/VIIRS_NOAA20_NRT/-100.65,25.45,-99.95,26.05/7` — [FIRMS API](https://firms.modaps.eosdis.nasa.gov/api/)
- GEE: `FIRMS` (MODIS-based) — [GEE catalog](https://developers.google.com/earth-engine/datasets/catalog/FIRMS)
- MODIS burned area: `MODIS/061/MCD64A1` [K]
- [V] CAMS added VIIRS active fires to its Global Fire Assimilation System from 4 December 2025 as MODIS winds down — [CAMS](https://atmosphere.copernicus.eu/drifting-away-modis-cams-global-fire-assimilation-system)

### Inferences
- Monterrey hazard layers a team can build in hours:
  - slope and terrain-position from GLO-30 (hillside informal settlements on Cerro del Topo Chico / La Campana – Altamira)
  - HAND-style flood proximity along the Santa Catarina river and arroyos (FABDEM)
  - FIRMS fire density on the Sierra Madre / Cumbres de Monterrey interface
  - OPERA DISP-S1 velocity, if frames exist, for subsidence near wells and industrial zones
- Mountain terrain will cause SAR layover/shadow on south-facing slopes. Mask with the DEM before interpreting DISP or flood maps.

### Gaps
- I did not verify that DISP-S1 frames actually exist over Monterrey, or the current processing latency (the archive cited runs to 2025). Check the ASF Displacement Portal.
- No published InSAR subsidence study for Monterrey was found in this session.
- I did not verify the exact FIRMS API transaction limit and maximum day range in 2026.
- INEGI's national DEM/LiDAR (Continuo de Elevaciones Mexicano) was not checked; it may be covered by another researcher.

## Commercial-but-free-for-research (Planet, Google EIE, Google Maps Platform environment APIs, Mapbox, Esri Living Atlas)

### Takeaway
For a 24–48 h event, assume NO commercial-imagery access unless a teammate already has it. Planet's Education & Research Basic program requires a university affiliation and can take up to 3 weeks to approve. Google EIE has Monterrey-relevant history (a Tec de Monterrey 2020 climate-action project using EIE emissions/solar data), but tree canopy data appears US-pilot only. Google's Air Quality, Solar and Pollen APIs need a billing-enabled Google Cloud project, and their free tier changed in 2025. Esri Living Atlas layers (Sentinel-2/IO land cover) are viewable free.

### Cited Findings
**Planet Education & Research (E&R) Basic** [V]
- Limited access to PlanetScope (and RapidEye archive) for students, researchers, technical staff and faculty at recognized universities. University email required. Non-profit and government employees are not eligible.
- Fixed two-year term. Approval may take up to 3 weeks — [Planet support: E&R Basic](https://support.planet.com/hc/en-us/articles/360016570538-How-Can-I-Register-for-the-Education-and-Research-Basic-Program); [Planet support: timeline/eligibility](https://support.planet.com/hc/en-us/articles/360017551718)
- Planet moved the broader E&R program to three-tier, country-adjusted campus pricing in 2023 — [BusinessWire 2023](https://www.businesswire.com/news/home/20230104005416/en)

**Google Environmental Insights Explorer** [V]
- Free for cities/local governments to understand GHG sources (buildings, transportation) and opportunities (rooftop solar), with global city coverage per CDP's guide — [Google Sustainability EIE](https://sustainability.google/working-together/tools/environmental-insights-explorer/); [CDP guide](https://www.cdp.net/en/cities/ghg-emissions-tools-and-datasets-guide-for-cities/google-environmental-insights-explorer)
- Tec de Monterrey won a 2020 Google.org/ICLEI call to use EIE for climate action plans in the Monterrey Metropolitan Area (mobility, energy efficiency, solar potential) — [Conecta Tec](https://conecta.tec.mx/en/news/national/research/tec-engineers-google-and-ngos-working-lowering-polluting-emissions)
- Tree canopy in EIE was described as a pilot in selected US cities — [CAKEX](https://www.cakex.org/tools/google-environmental-insights-explorer)

**Google Maps Platform environment APIs (Air Quality, Solar, Pollen)** [K]
- Air Quality API: about 500 m hourly AQI heatmap tiles, current conditions plus forecast and history.
- Solar API: building insights and data layers (DSM, annual flux, roof masks) where imagery exists.
- Pollen API.
- All need an API key on a billing-enabled Cloud project. In March 2025 Google replaced the US$200 monthly credit with per-SKU free monthly usage caps — [Google Maps Platform pricing](https://developers.google.com/maps/billing-and-pricing/pricing)
- Not verified this session: whether Monterrey has Solar API high-quality coverage, and the current free caps per SKU.

**Mapbox and Esri Living Atlas** [K]
- Mapbox: free tier for web map loads (good for the demo frontend) — [Mapbox pricing](https://www.mapbox.com/pricing)
- Esri Living Atlas: free public layers including Sentinel-2 10 m LULC, Landsat/Sentinel imagery services, World Imagery basemap (display only) — [Living Atlas](https://livingatlas.arcgis.com/)

**Other open commercial-source imagery** [K]
- Maxar Open Data (event-triggered, disaster-only)
- Satellogic EarthView, Umbra and Capella open SAR samples on AWS Open Data
- Monterrey coverage NOT checked — [AWS Open Data Registry](https://registry.opendata.aws/)

### Inferences
- Do not plan the hackathon around Planet. The approval latency (up to 3 weeks) and eligibility (university only) make it unrealistic unless a UANL/Tec/UDEM participant already has an account.
- For a "wow" demo layer, the Google Solar API (if Monterrey has coverage) or Meta 1 m canopy height give sub-10 m detail for free.

### Gaps
- I did not determine whether EIE currently shows Monterrey (or San Pedro Garza García, Guadalupe, etc.) building/transport emissions, or any tree canopy layer, in 2026.
- I did not confirm Google Air Quality API spatial resolution and coverage of Monterrey, Solar API coverage, or the 2026 free caps.
- I did not confirm NICFI/Planet tropical basemap availability (Monterrey at 25.7°N; program scope and continuation after 2025 unknown).
- Mapbox and Living Atlas terms were not re-checked.

## Access platforms, sign-up and quotas as of October 2026 (GEE, Planetary Computer, AWS, CDSE, NASA Earthdata)

### Takeaway
Earth Engine changed materially in 2026. Since 27 April 2026, every noncommercial project gets a monthly compute quota:
- Community: 150 EECU-hours, the default
- Contributor: 1,000 EECU-hours, requires a billing account but noncommercial EE use is not charged
- Partner: 100,000 EECU-hours, by application, several weeks to approve

Over quota, projects drop into a throttled "restricted mode" rather than being cut off, and using multiple projects to multiply quota is banned. Planetary Computer's free Hub was retired in 2024, but its STAC API and data remain usable anonymously from local Python.

### Cited Findings
**Google Earth Engine noncommercial tiers** [V]
- Monthly per-project quotas reset on the 1st at midnight Pacific. Unused hours don't roll over.
  - Community: 150 EECU-hours (540,000 EECU-seconds), all verified noncommercial projects.
  - Contributor: 1,000 EECU-hours, requires a billing account (noncommercial EE use isn't charged, other Cloud services are).
  - Partner: 100,000 EECU-hours, for nonprofits/NGOs and university/government research groups working on climate mitigation/adaptation/nature protection. Separate application, manual review taking "several weeks".
- Over quota, projects enter restricted mode with lower concurrency/throughput. EE Apps count against their parent project.
- Effective 27 April 2026; default tier is Community. Noncommercial status must be reverified annually. "Quota farming" across multiple projects is prohibited.
- The page gives no verification-time estimate for basic noncommercial registration. Page last updated 25 Sep 2026 — [GEE Noncommercial tiers](https://developers.google.com/earth-engine/guides/noncommercial_tiers)
- The API may only be used for development, research or educational purposes under noncommercial terms — [EE Additional API Terms](https://developers.google.cn/earth-engine/reference/Additional.API.Terms?hl=en)

**Microsoft Planetary Computer** [V]
- The Planetary Computer Hub (free JupyterHub) was retired on 6 June 2024. Data and APIs remain — [GitHub discussion #347](https://github.com/microsoft/PlanetaryComputer/discussions/347)
- The STAC API endpoint is `https://planetarycomputer.microsoft.com/api/stac/v1/`, with assets in Azure Blob Storage. Some datasets require (anonymous) SAS tokens via the `planetary-computer` package — [UA DataLab wiki](https://github.com/ua-datalab/Geospatial_Workshops/wiki/Microsoft-Planetary-Computer); [PC docs](https://planetarycomputer.microsoft.com/docs/concepts/data-catalog)
- "Planetary Computer Pro" is a separate commercial Azure product — [innFactory](https://innfactory.de/en/cloud/azure/products/planetary-computer-pro/)

**AWS Open Data** [K]
- Element84 Earth Search STAC `https://earth-search.aws.element84.com/v1` indexes Sentinel-2 L2A COGs, Landsat C2 L2, Copernicus DEM, NAIP, Sentinel-1 GRD. No account needed for most; USGS Landsat and S1 GRD buckets are requester-pays — [AWS Registry Sentinel-2](https://registry.opendata.aws/sentinel-2-l2a-cogs/)

**Copernicus Data Space Ecosystem (CDSE)** [K]
- Free self-registration (minutes). Browser, OData/STAC catalog, S3 access, openEO and Sentinel Hub APIs with monthly free processing quotas — [CDSE](https://dataspace.copernicus.eu)

**NASA Earthdata Login** [K]
- Free and instant. Needed for HLS, ECOSTRESS, TEMPO, OPERA and SMAP downloads; use the `earthaccess` Python library.
- AppEEARS extracts point/polygon time series (MODIS, VIIRS, HLS, ECOSTRESS, SMAP) as CSV with no code — [Earthdata Login](https://urs.earthdata.nasa.gov/); [AppEEARS](https://appeears.earthdatacloud.nasa.gov/)

### Inferences
- **GEE quota for a hackathon.** 150 EECU-hours per month per project is ample for metro-scale AGEB statistics (a few thousand polygons, 10–30 m composites), provided teams use median composites over filtered date ranges and run `reduceRegions` as batch exports. The risk is many people sharing one project, or heavy interactive map tiling.
- **Register projects early.** Register the noncommercial Cloud project days before the event; verification time is unspecified. Consider upgrading to Contributor (attach a billing account) for 1,000 EECU-hours as a safety margin.
- **Fallback.** Local Python against Planetary Computer/Earth Search STAC (no quota, no sign-up) is the resilient fallback when GEE is throttled.

### Gaps
- I did not find the typical approval time for GEE noncommercial registration in 2026.
- I did not confirm CDSE free quotas (Sentinel Hub processing units, openEO credits) for 2026.
- I did not confirm Planetary Computer catalog health or any dataset deprecations in 2026.
- I did not confirm ASF HyP3 monthly credit quotas.

## Highest-value layers for a Monterrey hackathon and the quickest pipeline to compute NDVI and LST per AGEB/colonia

### Takeaway
Ten layers cover heat, green, air, water, growth and risk, and nine of them load in one GEE session:
1. S2 NDVI (Cloud Score+)
2. Landsat 8/9 LST
3. Dynamic World
4. Meta 1 m canopy height
5. Sentinel-5P NO2 (+TEMPO for diurnal)
6. GHSL built/population plus Overture/Open Buildings
7. VIIRS Black Marble
8. Copernicus DEM (+FABDEM)
9. JRC GSW / Sentinel-1
10. FIRMS fires plus ERA5-Land/CHIRPS climate

The fastest pipeline is GEE: upload the INEGI AGEB shapefile as an asset, build composites, run `reduceRegions`, export CSV and join in pandas/GeoPandas. The quota-free fallback is `pystac-client` + `odc-stac` against Planetary Computer, with zonal stats via `exactextract`/`rasterstats`.

### Cited Findings
- All collection IDs below are cited in the thematic sections above.
- GEE quota context for this pipeline: Community tier, 150 EECU-hours/month, restricted mode over quota — [GEE tiers](https://developers.google.com/earth-engine/guides/noncommercial_tiers) [V]
- Planetary Computer STAC remains available without the Hub — [GitHub #347](https://github.com/microsoft/PlanetaryComputer/discussions/347) [V]
- Meta canopy GEE path — [GEE community catalog](https://gee-community-catalog.org/projects/meta_trees/) [V]
- Overture CLI bbox download — [Overture docs](https://docs.overturemaps.org/getting-data/) [K]
- A citable Monterrey LST–green infrastructure baseline — [ISPRS 2024](https://isprs-annals.copernicus.org/articles/X-3-2024/439/2024/) [V]

**Getting started in 1 hour: GEE path (Python; code written by the researcher from catalog specs, not executed)**
```python
import ee, geemap  # pip install earthengine-api geemap
ee.Authenticate(); ee.Initialize(project="YOUR-NONCOMMERCIAL-PROJECT")
aoi = ee.Geometry.Rectangle([-100.65, 25.45, -99.95, 26.05])
agebs = ee.FeatureCollection("projects/YOUR-PROJECT/assets/ageb_urbana_mty")  # INEGI AGEB shp uploaded via Code Editor > Assets

# Sentinel-2 NDVI, dry season, Cloud Score+ mask
csp = ee.ImageCollection("GOOGLE/CLOUD_SCORE_PLUS/V1/S2_HARMONIZED")
s2 = (ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED").filterBounds(aoi)
        .filterDate("2026-03-01", "2026-05-31").linkCollection(csp, ["cs_cdf"]))
ndvi = (s2.map(lambda i: i.updateMask(i.select("cs_cdf").gte(0.6))
                          .normalizedDifference(["B8", "B4"]).rename("ndvi"))
          .median())

# Landsat 8/9 LST (deg C), May-Sep 2023-2026 median
def lst(i):
    clear = i.select("QA_PIXEL").bitwiseAnd(0b11111).eq(0)   # fill, dilated cloud, cirrus, cloud, shadow
    t = i.select("ST_B10").multiply(0.00341802).add(149.0).subtract(273.15)
    return t.updateMask(clear).rename("lst_c")
ls = (ee.ImageCollection("LANDSAT/LC08/C02/T1_L2").merge(ee.ImageCollection("LANDSAT/LC09/C02/T1_L2"))
        .filterBounds(aoi).filterDate("2023-01-01", "2026-10-01")
        .filter(ee.Filter.calendarRange(5, 9, "month")).map(lst).median())

trees = ee.ImageCollection("GOOGLE/DYNAMICWORLD/V1").filterBounds(aoi) \
          .filterDate("2026-01-01", "2026-10-01").select("trees").mean().rename("dw_trees")
canopy = ee.ImageCollection("projects/sat-io/open-datasets/facebook/meta-canopy-height") \
          .filterBounds(aoi).mosaic().gt(3).rename("canopy_gt3m")   # fraction of area with trees > 3 m
no2 = ee.ImageCollection("COPERNICUS/S5P/OFFL/L3_NO2").filterBounds(aoi) \
          .filterDate("2025-10-01", "2026-10-01").select("tropospheric_NO2_column_number_density").mean().rename("no2")

stack = ndvi.addBands([ls, trees, canopy, no2])
stats = stack.reduceRegions(collection=agebs, reducer=ee.Reducer.mean(), scale=30, tileScale=4)
ee.batch.Export.table.toDrive(stats, description="mty_ageb_indicators", fileFormat="CSV").start()
# small AOIs: df = geemap.ee_to_df(stats)
```
Notes:
- Reducing everything at scale=30 averages the 1 m canopy and 10 m NDVI to 30 m. For canopy, run a separate `reduceRegions` at scale 1–2 m on a subset, or accept the 30 m approximation.
- NO2 at about 5 km is only meaningful at municipality scale.

**Getting started in 1 hour: local Python / Planetary Computer path (no quota)**
```python
# pip install pystac-client planetary-computer odc-stac rioxarray geopandas exactextract
import pystac_client, planetary_computer, odc.stac, geopandas as gpd
cat = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1",
                                modifier=planetary_computer.sign_inplace)
bbox = [-100.65, 25.45, -99.95, 26.05]
items = cat.search(collections=["sentinel-2-l2a"], bbox=bbox, datetime="2026-03-01/2026-05-31",
                   query={"eo:cloud_cover": {"lt": 20}}).item_collection()
ds = odc.stac.load(items, bands=["B04", "B08", "SCL"], bbox=bbox, crs="EPSG:32614",
                   resolution=10, chunks={"x": 2048, "y": 2048}, groupby="solar_day")
ok = ds.SCL.isin([4, 5, 6])                     # vegetation, bare, water (drop cloud/shadow)
red, nir = (ds.B04 - 1000).clip(0), (ds.B08 - 1000).clip(0)   # baseline >= 04.00 offset (all 2026 scenes)
ndvi = ((nir - red) / (nir + red)).where(ok).median("time").compute()
ndvi.rio.to_raster("mty_ndvi_2026_dry.tif")
# Landsat LST: collections=["landsat-c2-l2"], bands ["lwir11","qa_pixel"], K = lwir11*0.00341802+149.0
from exactextract import exact_extract
agebs = gpd.read_file("ageb_urbana_19.shp").to_crs(32614)
res = exact_extract("mty_ndvi_2026_dry.tif", agebs, ["mean", "count"], include_cols=["CVEGEO"], output="pandas")
```
Alternatives:
- `stackstac.stack(items, assets=[...], epsg=32614, resolution=10, bounds_latlon=bbox)` is an equivalent to odc-stac.
- `xee` opens GEE collections directly as xarray.

**Other 1-hour quick hits**
- Overture buildings/places: `overturemaps download --bbox=-100.65,25.45,-99.95,26.05 -f geoparquet --type=building -o mty_buildings.parquet` [K]
- FIRMS: request a MAP_KEY by email, then CSV via the area API URL in the terrain section [K]
- TEMPO via `earthaccess` [K]:
  ```python
  earthaccess.login()
  earthaccess.search_data(short_name="TEMPO_NO2_L3", bounding_box=(-100.65, 25.45, -99.95, 26.05), temporal=("2026-06-01", "2026-06-07"))
  ```
  Then open the NetCDF with xarray (group `product`). The short name/version may be V03 or V04; check Earthdata Search.
- OpenAQ v3: free key, then `GET /v3/locations?bbox=-100.65,25.45,-99.95,26.05` [K]

### Inferences
- **Recommended division of labor for a 48 h team:**
  - Person A: GEE indicators per AGEB (NDVI, LST, DW trees, canopy).
  - Person B: Overture/OSM vectors (parks, buildings, schools, hospitals) plus INEGI census join.
  - Person C: air (S5P monthly, TEMPO week, SIMA stations).
  - Person D: frontend (Mapbox/MapLibre with exported GeoJSON/PMTiles).
- **Strongest single narrative:** "heat-vulnerability index per AGEB" = LST (exposure) + low NDVI/canopy (lack of cooling) + census elderly/children/poverty (sensitivity) + distance to parks (adaptive capacity). Every input is free and computable within the first day.
- **Pre-event checklist (do 1+ week before):**
  - Register the GEE noncommercial project and choose the tier.
  - Create Earthdata Login, CDSE account, FIRMS MAP_KEY and OpenAQ key.
  - Pre-download the INEGI AGEB shapefile and the Overture extract.
  - Pre-export one LST and one NDVI composite as GeoTIFF in case GEE is throttled during the event.

### Gaps
- Code snippets were not executed in this session. Collection IDs marked [K] should be smoke-tested (one `ee.ImageCollection(ID).size().getInfo()` each) before the event.
- No measured EECU cost for the AGEB pipeline is available. Estimate it with a dry run in the GEE Code Editor task profiler.
