// Reto 3 · Aire de la ZMM — línea base satelital Sentinel-5P alrededor de las estaciones del SIMA.
// Pegar en code.earthengine.google.com. NO probado: los IDs y bandas se verificaron en el catálogo
// de GEE el 14-oct-2026, pero el script no se ha corrido.
//
// Salida: CSV largo (estación × contaminante × mes) con la media de columna en µmol/m² y el número
// de píxeles válidos. Las comparaciones por año de administración se hacen después en pandas/Sheets.
// Ojo: S5P mide columna atmosférica, no concentración a nivel de suelo.

// Coordenadas sacadas del mapa oficial del SIMA (aire.nl.gob.mx/airemapbing/airebing_icars_alt.php).
var estaciones = ee.FeatureCollection([
  ['CENTRO', 25.6760139, -100.338553, 'Monterrey'],
  ['SURESTE', 25.6654972, -100.243653, 'Guadalupe'],
  ['NORESTE', 25.74503, -100.25317, 'San Nicolás'],
  ['NOROESTE', 25.7629306, -100.369578, 'Monterrey'],
  ['SUROESTE', 25.6794444, -100.467831, 'Santa Catarina'],
  ['NOROESTE 2', 25.8004639, -100.585011, 'García'],
  ['NORTE', 25.7988361, -100.327164, 'Escobedo'],
  ['NORESTE 2', 25.777475, -100.1882, 'Apodaca'],
  ['SURESTE 2', 25.646126, -100.095616, 'Juárez'],
  ['SUROESTE 2', 25.665275, -100.412853, 'San Pedro'],
  ['SURESTE 3', 25.6008639, -99.9953028, 'Cadereyta'],
  ['NORTE 2', 25.7297587, -100.310019, 'San Nicolás'],
  ['SUR', 25.6169806, -100.273936, 'Monterrey'],
  ['ESTE', 25.7905833, -100.078411, 'Pesquería']
].map(function (e) {
  return ee.Feature(ee.Geometry.Point([e[2], e[1]]), {estacion: e[0], municipio: e[3]});
}));

var RADIO_M = 3000;  // el reto pide al menos 3 km; el píxel L3 es ~1.1 km pero el nativo de S5P es ~5.5×3.5 km
var zonas = estaciones.map(function (f) { return f.buffer(RADIO_M); });

var productos = [
  {nombre: 'NO2', col: 'COPERNICUS/S5P/OFFL/L3_NO2', banda: 'tropospheric_NO2_column_number_density'},
  {nombre: 'SO2', col: 'COPERNICUS/S5P/OFFL/L3_SO2', banda: 'SO2_column_number_density'},
  {nombre: 'CO',  col: 'COPERNICUS/S5P/OFFL/L3_CO',  banda: 'CO_column_number_density'}
];

// Desde jul-2018 (inicio de OFFL) para tener línea base previa al 4-oct-2021 (inicio de la administración).
var INICIO = ee.Date('2018-07-01');
var FIN = ee.Date('2026-10-01');
var meses = ee.List.sequence(0, FIN.difference(INICIO, 'month').round().subtract(1));
var reductor = ee.Reducer.mean().combine(ee.Reducer.count(), null, true);

function serieMensual(p) {
  var col = ee.ImageCollection(p.col).select(p.banda);
  return ee.FeatureCollection(meses.map(function (m) {
    var ini = INICIO.advance(m, 'month');
    var sub = col.filterDate(ini, ini.advance(1, 'month'));
    return ee.Algorithms.If(sub.size().gt(0),
      sub.mean().multiply(1e6)  // mol/m² → µmol/m²
        .reduceRegions({collection: zonas, reducer: reductor, scale: 1113.2})
        .map(function (f) { return f.set({contaminante: p.nombre, mes: ini.format('YYYY-MM')}); }),
      ee.FeatureCollection([]));
  })).flatten();
}

var tabla = ee.FeatureCollection(productos.map(serieMensual)).flatten();

Export.table.toDrive({
  collection: tabla,
  description: 'reto3_s5p_mensual_sima',
  fileFormat: 'CSV',
  selectors: ['estacion', 'municipio', 'contaminante', 'mes', 'mean', 'count']
});

// Vista rápida: NO2 mensual en todas las estaciones (compuestos mensuales para no pasar el tope de
// 5,000 elementos de ui.Chart).
var no2 = ee.ImageCollection(productos[0].col).select(productos[0].banda);
var no2Mensual = ee.ImageCollection(meses.map(function (m) {
  var ini = INICIO.advance(m, 'month');
  return no2.filterDate(ini, ini.advance(1, 'month')).mean().multiply(1e6)
    .set('system:time_start', ini.millis());
}));
print(ui.Chart.image.seriesByRegion({
  imageCollection: no2Mensual, regions: zonas, reducer: ee.Reducer.mean(), scale: 1113.2,
  xProperty: 'system:time_start', seriesProperty: 'estacion'
}).setOptions({title: 'NO2 troposférico (µmol/m²) a 3 km de cada estación SIMA', interpolateNulls: true}));

Map.centerObject(estaciones, 10);
Map.addLayer(no2.filterDate('2025-10-01', '2026-10-01').mean().multiply(1e6),
  {min: 20, max: 120, palette: ['black', 'blue', 'purple', 'cyan', 'green', 'yellow', 'red']}, 'NO2 oct-25→sep-26');
Map.addLayer(zonas, {color: 'white'}, 'Buffers 3 km');
