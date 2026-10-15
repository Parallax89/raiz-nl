// Configuración pública del front. La llave de MapTiler es de frontend: restringirla por origen en
// cloud.maptiler.com/account/keys (raiz-nl.netlify.app, c7b.github.io).
window.RAIZ_CONFIG = {
  maptilerKey: 'b33pPHWjqHIcuvRYOYxb'
};

// Capas base compartidas: MapTiler si hay llave, Esri/CARTO si no.
window.raizBases = function (L) {
  const key = (window.RAIZ_CONFIG || {}).maptilerKey;
  const mt = (estilo, ext) => L.tileLayer(`https://api.maptiler.com/maps/${estilo}/256/{z}/{x}/{y}.${ext}?key=${key}`, {
    maxZoom: 19, crossOrigin: true,
    attribution: '<a href="https://www.maptiler.com/copyright/" target="_blank">&copy; MapTiler</a> <a href="https://www.openstreetmap.org/copyright" target="_blank">&copy; OpenStreetMap</a>'
  });
  if (key) {
    return {
      'Mapa': mt('dataviz-light', 'png'),
      'Calles': mt('streets-v2', 'png'),
      'Satélite (ver la sierra)': mt('satellite', 'jpg')
    };
  }
  return {
    'Mapa': L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      subdomains: 'abcd', maxZoom: 19,
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>'
    }),
    'Satélite (ver la sierra)': L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      maxZoom: 19, attribution: 'Imágenes &copy; Esri, Maxar, Earthstar Geographics'
    })
  };
};
