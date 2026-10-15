/* Raíz NL — lo que empuja a donar más: impacto de cada monto y equipos. */
(function () {
  'use strict';
  const $ = (s) => document.querySelector(s);
  const $$ = (s) => Array.from(document.querySelectorAll(s));
  const CLAVE_EQUIPO = 'raiznl.equipo.v1';
  const SUGERIDOS = ['Tec de Monterrey', 'UANL', 'UDEM', 'Mi empresa', 'Mi colonia'];
  const num = (n) => Math.round(n).toLocaleString('es-MX');

  /* ---------- #4 Monto → impacto ----------
     Estimaciones de ejemplo, a validar con Pronatura:
     agua ≈ 1,000 árboles por hectárea en la sierra (10 m² cada uno); aire ≈ 25 m² de copa adulta por árbol. */
  function impacto(objetivo, n) {
    return objetivo === 'aire'
      ? { corto: `≈ ${num(n * 25)} m² de sombra`, largo: `≈ ${num(n * 25)} m² de sombra cuando crezcan, donde la ciudad respira peor` }
      : { corto: `≈ ${num(n * 10)} m² de ladera`, largo: `≈ ${num(n * 10)} m² de ladera restaurada en la sierra que alimenta las presas` };
  }
  function objetivoCard() {
    const b = $('.obj-btn[aria-pressed="true"]');
    return b ? b.dataset.cardObjetivo : 'agua';
  }
  function arbolesCard() {
    const otro = parseInt(($('#monto-otro') || {}).value, 10);
    if (otro > 0) return otro;
    const b = $('.monto[aria-pressed="true"]');
    return b ? parseInt(b.dataset.arboles, 10) : 1;
  }
  function pintarMontos() {
    const obj = objetivoCard();
    $$('.monto').forEach((b) => {
      let s = b.querySelector('.monto-sub');
      if (!s) { s = document.createElement('small'); s.className = 'monto-sub'; b.appendChild(s); }
      s.textContent = impacto(obj, parseInt(b.dataset.arboles, 10)).corto;
    });
    const n = arbolesCard();
    const el = $('#monto-impacto');
    if (el) el.innerHTML = `<b>${n === 1 ? 'Tu árbol' : 'Tus ' + num(n) + ' árboles'}</b> ${impacto(obj, n).largo}.<span class="monto-fuente">Estimación de ejemplo.</span>`;
  }
  document.addEventListener('click', (e) => {
    if (e.target.closest('.obj-btn, .monto')) setTimeout(pintarMontos, 0);
  });
  const otro = $('#monto-otro');
  if (otro) otro.addEventListener('input', () => setTimeout(pintarMontos, 0));
  pintarMontos();

  /* ---------- Equipos ---------- */
  function leerEquipo() { try { return localStorage.getItem(CLAVE_EQUIPO) || ''; } catch (e) { return ''; } }
  function guardarEquipo(v) { try { v ? localStorage.setItem(CLAVE_EQUIPO, v) : localStorage.removeItem(CLAVE_EQUIPO); } catch (e) { /* sin storage */ } }
  function compromisos() {
    try { const l = JSON.parse(localStorage.getItem('raiznl.compromisos.v1') || '[]'); return Array.isArray(l) ? l : []; } catch (e) { return []; }
  }
  function equiposExistentes() {
    const vistos = new Map();
    compromisos().forEach((c) => { const t = String(c.equipo || '').trim(); if (t) vistos.set(t.toLowerCase(), t); });
    return Array.from(vistos.values());
  }
  function pintarEquipos() {
    const actual = leerEquipo();
    const lista = equiposExistentes();
    const todos = lista.concat(SUGERIDOS.filter((s) => !lista.some((x) => x.toLowerCase() === s.toLowerCase())));
    $('#equipos-lista').innerHTML = todos.map((t) => `<option value="${t.replace(/"/g, '&quot;')}">`).join('');
    $('#equipos-sugeridos').innerHTML = todos.slice(0, 6).map((t) =>
      `<button type="button" class="chip-equipo" aria-pressed="${t === actual}">${window.raizLogo && window.raizLogo(t) ? `<img src="${window.raizLogo(t)}" alt="">` : ''}<span>${t.replace(/[<>&]/g, '')}</span></button>`).join('');
    $('#equipo-actual').innerHTML = actual
      ? `Estás en el equipo <b>${actual.replace(/[<>&]/g, '')}</b>: tus donaciones suman para él. <button type="button" class="link-btn" id="btn-salir-equipo">Salir</button>`
      : '';
    const salir = $('#btn-salir-equipo');
    if (salir) salir.addEventListener('click', () => { guardarEquipo(''); pintarEquipos(); });
  }
  function unirse(nombre) {
    const t = String(nombre || '').trim().slice(0, 40);
    if (!t) return;
    guardarEquipo(t);
    $('#equipo-nombre').value = '';
    pintarEquipos();
    const unete = $('#unete');
    if (unete) unete.scrollIntoView({ behavior: 'smooth', block: 'start' });
  }
  $('#form-equipo').addEventListener('submit', (e) => { e.preventDefault(); unirse($('#equipo-nombre').value); });
  $('#equipos-sugeridos').addEventListener('click', (e) => {
    const b = e.target.closest('.chip-equipo');
    if (b) unirse(b.querySelector('span').textContent);
  });
  document.addEventListener('raiznl:compromiso', pintarEquipos);
  pintarEquipos();
})();
