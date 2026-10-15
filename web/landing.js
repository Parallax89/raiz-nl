(function () {
  'use strict';
  var $ = function (id) { return document.getElementById(id); };
  var STORAGE_KEY = 'raiznl.compromisos.v1';
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var orden = 'recientes';
  var mostrado = 0;

  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function arboles(c) { var n = parseInt(c && c.arboles, 10); return n > 0 ? n : 1; }
  function leer() {
    try {
      var lista = JSON.parse(window.localStorage.getItem(STORAGE_KEY) || '[]');
      return Array.isArray(lista) ? lista : [];
    } catch (e) { return []; }
  }

  /* Contador del hero: suma de árboles comprometidos */
  function pintarContador(lista) {
    var total = lista.reduce(function (s, c) { return s + arboles(c); }, 0);
    var el = $('contador');
    var desde = mostrado;
    mostrado = total;
    if (reduce || total === desde) { el.textContent = total.toLocaleString('es-MX'); return; }
    var t0 = performance.now();
    (function paso(t) {
      var p = Math.min((t - t0) / 1200, 1);
      el.textContent = Math.round(desde + (total - desde) * p).toLocaleString('es-MX');
      if (p < 1) requestAnimationFrame(paso);
    })(t0);
  }

  /* Ranking */
  function pintarRanking(lista) {
    var items = lista.slice();
    if (orden === 'arboles') items.sort(function (a, b) { return arboles(b) - arboles(a); });
    else items.sort(function (a, b) { return String(b.fecha).localeCompare(String(a.fecha)); });
    items = items.slice(0, 10);
    var ol = $('rank-lista');
    if (!items.length) {
      ol.innerHTML = '<li class="rank-vacio">Todavía no hay compromisos. ¡Sé la primera persona en plantar!</li>';
      return;
    }
    ol.innerHTML = items.map(function (c) {
      var n = arboles(c);
      var nombre = c.nombre || (c.usuario ? '@' + c.usuario : 'Anónimo');
      var fecha = c.fecha ? new Date(c.fecha).toLocaleString('es-MX', { dateStyle: 'medium', timeStyle: 'short' }) : '';
      var donde = c.zona_nombre || c.municipio || '';
      return '<li class="rank-item">' +
        '<span class="rank-icono" aria-hidden="true">' + (c.objetivo === 'aire' ? '🌬️' : '💧') + '</span>' +
        '<div class="rank-texto"><div class="rank-nombre">' + esc(nombre) + '</div>' +
        (c.mensaje ? '<p class="rank-mensaje">' + esc(c.mensaje) + '</p>' : '') +
        '<p class="rank-fecha">' + esc([donde, fecha].filter(Boolean).join(' · ')) + '</p></div>' +
        '<span class="rank-arboles">' + n.toLocaleString('es-MX') + (n === 1 ? ' árbol' : ' árboles') + '</span></li>';
    }).join('');
  }

  Array.prototype.forEach.call(document.querySelectorAll('.rank-tab'), function (b, _, todos) {
    b.addEventListener('click', function () {
      orden = b.getAttribute('data-orden');
      Array.prototype.forEach.call(todos, function (x) { x.setAttribute('aria-selected', String(x === b)); });
      pintarRanking(leer());
    });
  });

  // Con la API de donaciones (backend/), el contador es el total real de árboles donados
  var api = (function () {
    var q = new URLSearchParams(location.search).get('api');
    if (q) return q.replace(/\/$/, '');
    if (window.RAIZ_API) return window.RAIZ_API;
    return ['localhost', '127.0.0.1'].indexOf(location.hostname) >= 0 ? 'http://127.0.0.1:8001' : null;
  })();
  /* Tira deslizante del hero: ejemplos del demo + compromisos reales de este navegador */
  var EJEMPLOS = [
    { foto: 'img/donadores/d1.jpg', pos: 'center 15%', arboles: 250 },
    { foto: 'img/donadores/d2.jpg', pos: 'center 35%', arboles: 100 },
    { foto: 'img/donadores/d3.png', pos: 'center 25%', arboles: 500 },
    { foto: 'img/donadores/d4.png', pos: 'center 40%', arboles: 50 },
    { foto: 'img/donadores/d5.png', pos: '60% 30%', arboles: 150 },
    { foto: 'img/donadores/d6.avif', pos: 'center 30%', arboles: 75 }
  ];
  function iniciales(c) {
    var t = String(c.nombre || c.usuario || '').trim();
    if (!t) return '🌳';
    var p = t.replace(/^@/, '').split(/\s+/);
    return ((p[0] || '')[0] + ((p[1] || '')[0] || '')).toUpperCase();
  }
  function pintarDonadores(lista) {
    var reales = lista.slice().sort(function (a, b) { return String(b.fecha).localeCompare(String(a.fecha)); }).slice(0, 12);
    var items = reales.map(function (c) {
      return '<li class="donador"><span class="donador-foto">' + esc(iniciales(c)) + '</span>' +
        '<span class="donador-arboles">' + arboles(c).toLocaleString('es-MX') + ' <small>árboles</small></span></li>';
    }).concat(EJEMPLOS.map(function (d) {
      return '<li class="donador"><img class="donador-foto" src="' + d.foto + '" alt="" style="object-position:' + d.pos + '" loading="lazy">' +
        '<span class="donador-arboles">' + d.arboles.toLocaleString('es-MX') + ' <small>árboles</small></span></li>';
    }));
    // Se repite la lista para que el loop no tenga hueco (la animación mueve -50%)
    while (items.length < 8) items = items.concat(items);
    var pista = $('donadores-pista');
    pista.innerHTML = items.concat(items.map(function (h) { return h.replace('<li ', '<li aria-hidden="true" '); })).join('');
    pista.style.setProperty('--dur', (items.length * 4) + 's');
  }

  function pintar(lista) {
    pintarDonadores(lista);
    pintarRanking(lista);
    if (!api) { pintarContador(lista); return; }
    fetch(api + '/api/resumen').then(function (r) { if (!r.ok) throw 0; return r.json(); })
      .then(function (r) { pintarContador([{ arboles: r.donados }].filter(function () { return r.donados > 0; })); })
      .catch(function () { pintarContador(lista); });
  }
  pintar(leer());
  document.addEventListener('raiznl:compromiso', function (e) { pintar(e.detail || leer()); });

  /* Impacto */
  function carga(url) { return fetch(url).then(function (r) { if (!r.ok) throw 0; return r.json(); }); }
  carga('data/resumen.json').catch(function () { return carga('data/mock/resumen.json'); }).then(function (r) {
    if (r.ha_quemadas_total != null) $('st-ha').textContent = Math.round(r.ha_quemadas_total).toLocaleString('es-MX');
    if (r.incendios_total != null) $('st-incendios').textContent = Number(r.incendios_total).toLocaleString('es-MX');
    if (r.zonas_agua != null) $('st-agua').textContent = r.zonas_agua;
    if (r.zonas_aire != null) $('st-aire').textContent = r.zonas_aire;
  }).catch(function () { /* se quedan los guiones */ });
})();
