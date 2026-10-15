(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };

  var total = 0;
  try {
    var lista = JSON.parse(window.localStorage.getItem('raiznl.compromisos.v1') || '[]');
    if (Array.isArray(lista)) total = lista.length;
  } catch (e) { /* sin storage */ }

  var el = $('contador');
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || total === 0) {
    el.textContent = total.toLocaleString('es-MX');
  } else {
    var t0 = performance.now();
    (function paso(t) {
      var p = Math.min((t - t0) / 1200, 1);
      el.textContent = Math.round(total * p).toLocaleString('es-MX');
      if (p < 1) requestAnimationFrame(paso);
    })(t0);
  }

  function carga(url) { return fetch(url).then(function (r) { if (!r.ok) throw 0; return r.json(); }); }
  carga('data/resumen.json').catch(function () { return carga('data/mock/resumen.json'); }).then(function (r) {
    $('st-ha').textContent = Math.round(r.ha_quemadas_total).toLocaleString('es-MX');
    $('st-agua').textContent = r.zonas_agua;
    $('st-aire').textContent = r.zonas_aire;
  }).catch(function () { /* se quedan los guiones */ });
})();
