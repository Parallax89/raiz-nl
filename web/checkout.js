/* Raíz NL — pago simulado y diploma con mapa (demo). app.js llama a window.RaizCheckout. */
(function () {
  'use strict';

  const PRECIO = 150; // MXN por árbol, precio de ejemplo
  const EJEMPLO = { nombre: 'Ana Garza', correo: 'ana.garza@ejemplo.mx', tarjeta: '4242 4242 4242 4242', vence: '12/29', cvc: '123' };
  const PASOS = ['Validando tarjeta…', 'Procesando pago…', 'Asignando tu lugar en la zona…', '¡Pago aprobado!'];
  const lento = !window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const $ = (s) => document.querySelector(s);
  const espera = (ms) => new Promise((r) => setTimeout(r, lento ? ms : 0));
  const dinero = (n) => '$' + n.toLocaleString('es-MX') + ' MXN';

  let form = null;
  let ultimo = null; // datos del diploma para el PDF

  /* ---------- Formulario ---------- */
  function actualizarTotal() {
    const n = Math.max(1, Math.min(10000, parseInt(form.arboles.value, 10) || 1));
    $('#pago-total').textContent = dinero(n * PRECIO);
  }

  async function teclear(input, texto, ms) {
    input.value = '';
    input.classList.add('tecleando');
    for (const c of texto) {
      input.value += c;
      input.dispatchEvent(new Event('input', { bubbles: true }));
      await espera(ms);
    }
    input.classList.remove('tecleando');
  }

  let llenando = null;
  function llenarEjemplo(todo) {
    if (llenando) return llenando;
    llenando = (async () => {
      if (todo || !form.nombre.value.trim()) await teclear(form.nombre, EJEMPLO.nombre, 45);
      if (todo || !form.correo.value.trim()) await teclear(form.correo, EJEMPLO.correo, 30);
      await teclear(form.tarjeta, EJEMPLO.tarjeta, 35);
      await teclear(form.vence, EJEMPLO.vence, 60);
      await teclear(form.cvc, EJEMPLO.cvc, 80);
    })().finally(() => { llenando = null; });
    return llenando;
  }

  function abrir() {
    form = form || $('#form-donar');
    $('#dlg-pagando').hidden = true;
    actualizarTotal();
  }

  // Se llama al enviar: llena la tarjeta si falta y muestra la animación de pago.
  async function pagar() {
    if (!form.tarjeta.value) await llenarEjemplo(false);
    form.hidden = true;
    $('#dlg-pagando').hidden = false;
    $('#dlg-pagando').classList.remove('ok');
    for (let i = 0; i < PASOS.length; i++) {
      $('#pagando-texto').textContent = PASOS[i];
      if (i === PASOS.length - 1) $('#dlg-pagando').classList.add('ok');
      await espera(i === PASOS.length - 1 ? 700 : 850);
    }
  }
  function cancelarPago() {
    $('#dlg-pagando').hidden = true;
    form.hidden = false;
  }

  /* ---------- Coordenadas ---------- */
  function semilla(str) {
    let h = 2166136261;
    for (const c of str) h = Math.imul(h ^ c.charCodeAt(0), 16777619);
    return () => {
      h = Math.imul(h ^ (h >>> 15), 2246822507);
      h = Math.imul(h ^ (h >>> 13), 3266489909);
      return ((h ^= h >>> 16) >>> 0) / 4294967296;
    };
  }
  function dentro(lon, lat, anillo) {
    let si = false;
    for (let i = 0, j = anillo.length - 1; i < anillo.length; j = i++) {
      const [xi, yi] = anillo[i], [xj, yj] = anillo[j];
      if ((yi > lat) !== (yj > lat) && lon < ((xj - xi) * (lat - yi)) / (yj - yi) + xi) si = !si;
    }
    return si;
  }
  // Punto al azar (reproducible por folio) dentro del polígono de la zona.
  function puntoEnZona(f, folio) {
    const g = f.geometry || {};
    const anillo = g.type === 'Polygon' ? g.coordinates[0] : g.type === 'MultiPolygon' ? g.coordinates[0][0] : null;
    const c = f.properties.centro;
    if (!anillo) return c ? { lat: c[0], lon: c[1] } : null;
    const xs = anillo.map((p) => p[0]), ys = anillo.map((p) => p[1]);
    const [x0, x1, y0, y1] = [Math.min(...xs), Math.max(...xs), Math.min(...ys), Math.max(...ys)];
    const rnd = semilla(folio);
    for (let i = 0; i < 500; i++) {
      const lon = x0 + rnd() * (x1 - x0), lat = y0 + rnd() * (y1 - y0);
      if (dentro(lon, lat, anillo)) return { lat, lon };
    }
    return c ? { lat: c[0], lon: c[1] } : { lat: (y0 + y1) / 2, lon: (x0 + x1) / 2 };
  }
  function textoCoords(p) {
    return `${Math.abs(p.lat).toFixed(5)}° ${p.lat >= 0 ? 'N' : 'S'}, ${Math.abs(p.lon).toFixed(5)}° ${p.lon >= 0 ? 'E' : 'O'}`;
  }

  /* ---------- Mapa en canvas (mosaicos satelitales de Esri) ---------- */
  const TILE = 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}';
  function cargarImg(url) {
    return new Promise((ok) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => ok(img);
      img.onerror = () => ok(null);
      img.src = url;
    });
  }
  async function pintarMapa(canvas, p, z) {
    const ctx = canvas.getContext('2d');
    const W = canvas.width, H = canvas.height, n = 2 ** z;
    const px = ((p.lon + 180) / 360) * n * 256;
    const rad = (p.lat * Math.PI) / 180;
    const py = ((1 - Math.log(Math.tan(rad) + 1 / Math.cos(rad)) / Math.PI) / 2) * n * 256;
    const ox = px - W / 2, oy = py - H / 2;
    ctx.fillStyle = '#2f4a2a';
    ctx.fillRect(0, 0, W, H);
    const tareas = [];
    for (let tx = Math.floor(ox / 256); tx <= Math.floor((ox + W) / 256); tx++) {
      for (let ty = Math.floor(oy / 256); ty <= Math.floor((oy + H) / 256); ty++) {
        const url = TILE.replace('{z}', z).replace('{x}', tx).replace('{y}', ty);
        tareas.push(cargarImg(url).then((img) => { if (img) ctx.drawImage(img, tx * 256 - ox, ty * 256 - oy); }));
      }
    }
    await Promise.all(tareas);
    // Pin
    const cx = W / 2, cy = H / 2;
    ctx.beginPath(); ctx.arc(cx, cy, 34, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(111, 186, 13, 0.25)'; ctx.fill();
    ctx.beginPath(); ctx.moveTo(cx, cy);
    ctx.bezierCurveTo(cx - 16, cy - 20, cx - 16, cy - 40, cx, cy - 40);
    ctx.bezierCurveTo(cx + 16, cy - 40, cx + 16, cy - 20, cx, cy);
    ctx.fillStyle = '#dc582a'; ctx.fill();
    ctx.lineWidth = 3; ctx.strokeStyle = '#fff'; ctx.stroke();
    ctx.beginPath(); ctx.arc(cx, cy - 27, 6, 0, Math.PI * 2); ctx.fillStyle = '#fff'; ctx.fill();
    ctx.font = '600 12px Montserrat, Arial, sans-serif';
    ctx.fillStyle = 'rgba(255,255,255,0.85)';
    ctx.fillText('Imágenes © Esri, Maxar', 8, H - 8);
  }
  function mapaComoImagen(canvas) {
    try { return canvas.toDataURL('image/jpeg', 0.82); } catch (e) { return null; } // canvas contaminado: sin mapa
  }

  /* ---------- Diploma ---------- */
  const TXT_ARBOLES = (n) => n === 1 ? '1 árbol' : n.toLocaleString('es-MX') + ' árboles';
  // Mismas estimaciones de ejemplo que impulso.js
  const IMPACTO = (obj, n) => obj === 'aire'
    ? `≈ ${(n * 25).toLocaleString('es-MX')} m² de sombra cuando crezcan`
    : `≈ ${(n * 10).toLocaleString('es-MX')} m² de ladera restaurada`;

  async function diploma(f, d) {
    const folio = 'RNL-' + (d.id || Date.now().toString(36)).toUpperCase();
    const punto = puntoEnZona(f, folio);
    const p = f.properties;
    ultimo = {
      folio, punto, nombre: d.nombre || 'Persona donante', arboles: d.arboles || 1, equipo: d.equipo || null,
      zona: p.nombre, municipio: p.municipio, objetivo: p.objetivo,
      fecha: new Date().toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' })
    };
    $('#diploma-nombre').textContent = ultimo.nombre;
    $('#diploma-coords').textContent = punto ? textoCoords(punto) : 'Por asignar';
    $('#diploma-zona').textContent = `${TXT_ARBOLES(ultimo.arboles)} · ${p.nombre} · ${p.municipio} · Folio ${folio}`;
    if (punto) await pintarMapa($('#diploma-mapa'), punto, 15);
    await tarjeta(ultimo);
  }

  /* ---------- Tarjeta para redes (1200×675, formato de imagen de X) ---------- */
  function envolver(ctx, texto, max) {
    const palabras = String(texto).split(/\s+/), lineas = [];
    let l = '';
    for (const w of palabras) {
      const t = l ? l + ' ' + w : w;
      if (ctx.measureText(t).width > max && l) { lineas.push(l); l = w; } else l = t;
    }
    if (l) lineas.push(l);
    return lineas;
  }
  function rect(ctx, x, y, w, h, r) {
    ctx.beginPath(); ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  async function tarjeta(d) {
    const cv = $('#share-card');
    if (!cv) return;
    try { await document.fonts.ready; } catch (e) { /* sin Font Loading API */ }
    const ctx = cv.getContext('2d'), W = cv.width, H = cv.height;
    const agua = d.objetivo !== 'aire';
    ctx.fillStyle = '#113259'; ctx.fillRect(0, 0, W, H);
    // cerros
    ctx.fillStyle = '#196d4a';
    ctx.beginPath(); ctx.moveTo(0, H - 70);
    ctx.bezierCurveTo(260, H - 120, 520, H - 40, 760, H - 90); ctx.bezierCurveTo(960, H - 130, 1100, H - 60, W, H - 95);
    ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.fill();
    const F = 'Montserrat, Arial, sans-serif';
    ctx.textBaseline = 'alphabetic';
    ctx.fillStyle = '#dc582a'; ctx.font = `900 30px ${F}`; ctx.fillText('#RAÍZNL', 64, 90);
    ctx.fillStyle = '#ffffff'; ctx.font = `900 150px ${F}`; ctx.fillText(d.arboles.toLocaleString('es-MX'), 58, 250);
    ctx.font = `900 44px ${F}`; ctx.fillText(d.arboles === 1 ? 'ÁRBOL' : 'ÁRBOLES', 64, 305);
    ctx.fillStyle = agua ? '#b4dbe1' : '#ffd08a'; ctx.font = `700 30px ${F}`;
    ctx.fillText(agua ? '💧 para el agua de Monterrey' : '🌬️ para el aire de Monterrey', 64, 355);
    ctx.fillStyle = '#ffffff'; ctx.font = `500 24px ${F}`;
    envolver(ctx, `${d.zona} · ${d.municipio}`, 500).slice(0, 2).forEach((l, i) => ctx.fillText(l, 64, 405 + i * 32));
    ctx.fillStyle = '#b4dbe1'; ctx.font = `700 22px ${F}`;
    ctx.fillText(IMPACTO(d.objetivo, d.arboles) + (d.equipo ? ` · Equipo ${d.equipo}` : ''), 64, 485);
    // mapa del punto
    const mx = 640, my = 64, mw = 496, mh = 400;
    ctx.save(); rect(ctx, mx, my, mw, mh, 18); ctx.clip();
    ctx.fillStyle = '#2f4a2a'; ctx.fillRect(mx, my, mw, mh);
    const mapa = $('#diploma-mapa');
    if (mapa && d.punto) {
      const s = Math.max(mw / mapa.width, mh / mapa.height), sw = mw / s, sh = mh / s;
      ctx.drawImage(mapa, (mapa.width - sw) / 2, (mapa.height - sh) / 2, sw, sh, mx, my, mw, mh);
    }
    ctx.restore();
    ctx.lineWidth = 4; ctx.strokeStyle = '#ffffff'; rect(ctx, mx, my, mw, mh, 18); ctx.stroke();
    if (d.punto) {
      ctx.fillStyle = '#ffffff'; ctx.font = `700 20px ${F}`;
      ctx.fillText(textoCoords(d.punto), mx, my + mh + 34);
    }
    ctx.fillStyle = '#ffffff'; ctx.font = `900 30px ${F}`; ctx.fillText('¿Quién me sigue? 🌳', 64, H - 40);
    ctx.font = `700 22px ${F}`; ctx.textAlign = 'right'; ctx.fillText(location.host || 'raiz-nl.netlify.app', W - 64, H - 40);
    ctx.textAlign = 'left';
  }
  function blobTarjeta() {
    return new Promise((ok) => { try { $('#share-card').toBlob((b) => ok(b), 'image/png'); } catch (e) { ok(null); } });
  }
  async function descargarTarjeta() {
    const b = await blobTarjeta();
    if (!b) { alert('No se pudo generar la imagen (el mapa no dejó exportarse).'); return; }
    const a = document.createElement('a');
    a.href = URL.createObjectURL(b); a.download = `raiznl-${(ultimo && ultimo.folio) || 'arbol'}.png`;
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(() => URL.revokeObjectURL(a.href), 5000);
  }
  async function compartirTarjeta() {
    const b = await blobTarjeta();
    if (!b) return descargarTarjeta();
    const archivo = new File([b], `raiznl-${(ultimo && ultimo.folio) || 'arbol'}.png`, { type: 'image/png' });
    const texto = ultimo ? `Planté ${TXT_ARBOLES(ultimo.arboles)} en ${ultimo.zona} con #RaízNL. ¿Quién me sigue?` : '#RaízNL';
    try { await navigator.share({ files: [archivo], text: texto }); } catch (e) { /* cancelado */ }
  }

  /* ---------- PDF ---------- */
  async function descargarPDF() {
    if (!ultimo) return;
    const jsPDF = window.jspdf && window.jspdf.jsPDF;
    if (!jsPDF) { alert('No se pudo cargar el generador de PDF. Revisa tu conexión.'); return; }
    const d = ultimo;
    const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'letter', compress: true });
    doc.setProperties({ title: `Certificado #RaízNL ${d.folio}`, subject: 'Certificado de árbol (demo)', creator: 'Raíz NL' });
    const W = 279.4, H = 215.9;
    const spruce = [17, 50, 89], sunset = [220, 88, 42], fern = [111, 186, 13], gris = [95, 100, 110];
    const acento = d.objetivo === 'aire' ? [214, 140, 20] : [37, 120, 190];

    // marco y banda superior
    doc.setFillColor(...spruce); doc.rect(0, 0, W, H, 'F');
    doc.setFillColor(255, 255, 255); doc.roundedRect(8, 8, W - 16, H - 16, 3, 3, 'F');
    doc.setFillColor(...spruce); doc.rect(8, 8, W - 16, 22, 'F');
    doc.setTextColor(255, 255, 255); doc.setFont('helvetica', 'bold'); doc.setFontSize(13);
    doc.text('#RAÍZNL', 20, 22.5);
    doc.setFont('helvetica', 'normal'); doc.setFontSize(10);
    doc.text(`CERTIFICADO DE ÁRBOL · FOLIO ${d.folio}`, W - 20, 22.5, { align: 'right' });

    // columna izquierda
    const x = 22;
    doc.setTextColor(...sunset); doc.setFont('helvetica', 'bold'); doc.setFontSize(11);
    doc.text('GRACIAS POR PLANTAR', x, 46);
    doc.setTextColor(...spruce); doc.setFontSize(28);
    const nombre = doc.splitTextToSize(d.nombre, 125).slice(0, 2);
    doc.text(nombre, x, 59);
    let y = 59 + nombre.length * 11;
    doc.setFontSize(54); doc.text(d.arboles.toLocaleString('es-MX'), x, y + 14);
    const ancho = doc.getTextWidth(d.arboles.toLocaleString('es-MX'));
    doc.setFontSize(16); doc.text(d.arboles === 1 ? 'árbol' : 'árboles', x + ancho + 3, y + 14);
    y += 24;
    // etiqueta de objetivo
    doc.setFillColor(...acento); doc.roundedRect(x, y, 62, 8, 2, 2, 'F');
    doc.setTextColor(255, 255, 255); doc.setFontSize(9.5);
    doc.text(d.objetivo === 'aire' ? 'PARA EL AIRE DE MONTERREY' : 'PARA EL AGUA DE MONTERREY', x + 31, y + 5.4, { align: 'center' });
    y += 17;
    doc.setTextColor(...gris); doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5);
    doc.text(d.arboles === 1 ? 'Tu árbol se plantará en:' : 'Tus árboles se plantarán en:', x, y);
    doc.setTextColor(...spruce); doc.setFont('helvetica', 'bold'); doc.setFontSize(17);
    doc.text(d.punto ? textoCoords(d.punto) : 'Por asignar', x, y + 8);
    y += 18;
    doc.setFont('helvetica', 'normal'); doc.setFontSize(10.5); doc.setTextColor(40, 40, 40);
    const fin = d.objetivo === 'agua'
      ? 'Sujeta el suelo y ayuda a que el agua se infiltre en una ladera que perdió su cobertura.'
      : 'Da sombra y baja el calor y el polvo donde la gente respira peor.';
    const filas = [
      ['Zona', d.zona], ['Municipio', d.municipio], ['Impacto estimado', IMPACTO(d.objetivo, d.arboles).replace('≈', 'aprox.')],
      ['Para qué sirve', fin]
    ].concat(d.equipo ? [['Equipo', d.equipo]] : []).concat([['Fecha', d.fecha]]);
    filas.forEach(([k, v]) => {
      doc.setFont('helvetica', 'bold'); doc.setTextColor(...spruce); doc.text(k, x, y);
      doc.setFont('helvetica', 'normal'); doc.setTextColor(40, 40, 40);
      const l = doc.splitTextToSize(String(v), 92);
      doc.text(l, x + 34, y);
      y += Math.max(1, l.length) * 5 + 2;
    });

    // columna derecha: mapa + qué sigue
    const mx = 160, my = 40, mw = 100, mh = 62;
    const img = mapaComoImagen($('#diploma-mapa'));
    if (img) {
      doc.addImage(img, 'JPEG', mx, my, mw, mh, undefined, 'MEDIUM');
      doc.setDrawColor(...spruce); doc.setLineWidth(0.6); doc.rect(mx, my, mw, mh);
    } else {
      doc.setFillColor(235, 240, 235); doc.rect(mx, my, mw, mh, 'F');
    }
    if (d.punto) {
      const url = `https://www.google.com/maps?q=${d.punto.lat.toFixed(5)},${d.punto.lon.toFixed(5)}`;
      doc.setFontSize(9.5); doc.setTextColor(...sunset); doc.setFont('helvetica', 'bold');
      doc.textWithLink('Ver el punto en Google Maps >', mx, my + mh + 6, { url });
    }
    let sy = my + mh + 18;
    doc.setTextColor(...spruce); doc.setFontSize(11); doc.text('QUÉ SIGUE', mx, sy);
    doc.setDrawColor(...fern); doc.setLineWidth(0.8); doc.line(mx, sy + 2, mx + 22, sy + 2);
    sy += 9;
    doc.setFont('helvetica', 'normal'); doc.setFontSize(9.5); doc.setTextColor(40, 40, 40);
    ['1. El equipo que planta confirma el punto exacto en temporada de lluvias.',
      '2. Recibes una foto geolocalizada de tu árbol.',
      '3. A los 12 meses verificamos con imagen satelital que siga vivo.'].forEach((t) => {
      const l = doc.splitTextToSize(t, mw); doc.text(l, mx, sy); sy += l.length * 4.6 + 2;
    });

    // pie
    doc.setDrawColor(225, 228, 232); doc.setLineWidth(0.3); doc.line(22, H - 32, W - 22, H - 32);
    doc.setFontSize(8.5); doc.setTextColor(...gris);
    doc.text(doc.splitTextToSize('DEMO del Grok Monterrey Build Day. El pago fue simulado: no hubo cobro y este certificado no tiene valor fiscal. Impacto estimado con supuestos de ejemplo (aprox. 1,000 árboles por hectárea en la sierra; 25 m² de copa por árbol adulto).', W - 90), 22, H - 25);
    doc.setTextColor(...sunset); doc.setFont('helvetica', 'bold'); doc.setFontSize(9.5);
    const sitio = location.origin && location.origin.startsWith('http') ? location.origin : 'https://raiz-nl.netlify.app';
    const etiqueta = sitio.replace(/^https?:\/\//, '');
    doc.textWithLink(etiqueta, W - 22 - doc.getTextWidth(etiqueta), H - 25, { url: sitio });
    doc.save(`certificado-raiznl-${d.folio}.pdf`);
  }

  document.addEventListener('DOMContentLoaded', () => {
    form = $('#form-donar');
    if (!form) return;
    form.arboles.addEventListener('input', actualizarTotal);
    $('#btn-ejemplo').addEventListener('click', () => llenarEjemplo(true));
    $('#btn-pdf').addEventListener('click', descargarPDF);
    $('#btn-share-dl').addEventListener('click', descargarTarjeta);
    const sh = $('#btn-share');
    try {
      if (navigator.canShare && navigator.canShare({ files: [new File([''], 'x.png', { type: 'image/png' })] })) {
        sh.hidden = false; sh.addEventListener('click', compartirTarjeta);
      }
    } catch (e) { /* sin Web Share */ }
  });

  window.RaizCheckout = { abrir, pagar, cancelarPago, diploma };
})();
