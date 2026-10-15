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
    try { return canvas.toDataURL('image/jpeg', 0.9); } catch (e) { return null; } // canvas contaminado: sin mapa
  }

  /* ---------- Diploma ---------- */
  async function diploma(f, d) {
    const folio = 'RNL-' + (d.id || Date.now().toString(36)).toUpperCase();
    const punto = puntoEnZona(f, folio);
    const p = f.properties;
    ultimo = {
      folio, punto, nombre: d.nombre || 'Persona donante', arboles: d.arboles || 1,
      zona: p.nombre, municipio: p.municipio, objetivo: p.objetivo,
      fecha: new Date().toLocaleDateString('es-MX', { day: 'numeric', month: 'long', year: 'numeric' })
    };
    $('#diploma-nombre').textContent = ultimo.nombre;
    $('#diploma-coords').textContent = punto ? textoCoords(punto) : 'Por asignar';
    $('#diploma-zona').textContent = `${ultimo.arboles === 1 ? '1 árbol' : ultimo.arboles.toLocaleString('es-MX') + ' árboles'} · ${p.nombre} · ${p.municipio} · Folio ${folio}`;
    if (punto) await pintarMapa($('#diploma-mapa'), punto, 15);
  }

  async function descargarPDF() {
    if (!ultimo) return;
    const jsPDF = window.jspdf && window.jspdf.jsPDF;
    if (!jsPDF) { alert('No se pudo cargar el generador de PDF. Revisa tu conexión.'); return; }
    const d = ultimo;
    const doc = new jsPDF({ orientation: 'landscape', unit: 'mm', format: 'letter' });
    const W = 279.4, H = 215.9;
    const spruce = [17, 50, 89], sunset = [220, 88, 42], fern = [111, 186, 13];
    doc.setFillColor(...spruce); doc.rect(0, 0, W, H, 'F');
    doc.setFillColor(255, 255, 255); doc.rect(8, 8, W - 16, H - 16, 'F');
    doc.setDrawColor(...fern); doc.setLineWidth(1.2); doc.rect(12, 12, W - 24, H - 24);

    doc.setTextColor(...sunset); doc.setFont('helvetica', 'bold'); doc.setFontSize(11);
    doc.text('#RAÍZNL · CERTIFICADO DE ÁRBOL', 22, 28);
    doc.setTextColor(...spruce); doc.setFontSize(26);
    doc.text('Gracias por plantar', 22, 42);
    doc.setFontSize(30); doc.text(doc.splitTextToSize(d.nombre, 120), 22, 58);

    doc.setFont('helvetica', 'normal'); doc.setFontSize(12); doc.setTextColor(40, 40, 40);
    const arboles = d.arboles === 1 ? 'Tu árbol va' : `Tus ${d.arboles.toLocaleString('es-MX')} árboles van`;
    doc.text(doc.splitTextToSize(`${arboles} a estar plantado${d.arboles === 1 ? '' : 's'} en estas coordenadas:`, 120), 22, 78);
    doc.setFont('helvetica', 'bold'); doc.setFontSize(18); doc.setTextColor(...spruce);
    doc.text(d.punto ? textoCoords(d.punto) : 'Por asignar', 22, 92);

    doc.setFont('helvetica', 'normal'); doc.setFontSize(11); doc.setTextColor(60, 60, 60);
    const fin = d.objetivo === 'agua'
      ? 'Zona de restauración hídrica: ayuda a sujetar el suelo y a que el agua se infiltre.'
      : 'Zona de arbolado urbano: da sombra y mejora el aire donde la gente respira peor.';
    const lineas = [`Zona: ${d.zona}`, `Municipio: ${d.municipio}`, fin, `Fecha: ${d.fecha}`, `Folio: ${d.folio}`];
    doc.text(doc.splitTextToSize(lineas.join('\n'), 120), 22, 106, { lineHeightFactor: 1.5 });

    const img = mapaComoImagen($('#diploma-mapa'));
    if (img) {
      doc.addImage(img, 'JPEG', 152, 26, 108, 60.75);
      doc.setDrawColor(...spruce); doc.setLineWidth(0.6); doc.rect(152, 26, 108, 60.75);
    }
    if (d.punto) {
      const url = `https://www.google.com/maps?q=${d.punto.lat.toFixed(5)},${d.punto.lon.toFixed(5)}`;
      doc.setFontSize(10); doc.setTextColor(...sunset);
      doc.textWithLink('Ver el punto en el mapa', 152, 94, { url });
    }

    doc.setFontSize(9); doc.setTextColor(120, 120, 120);
    doc.text(doc.splitTextToSize('DEMO del Grok Monterrey Build Day. El pago fue simulado: no hubo cobro y este certificado no tiene valor. El punto exacto lo confirma el equipo que planta.', W - 44), 22, H - 30);
    doc.save(`diploma-raiznl-${d.folio}.pdf`);
  }

  document.addEventListener('DOMContentLoaded', () => {
    form = $('#form-donar');
    if (!form) return;
    form.arboles.addEventListener('input', actualizarTotal);
    $('#btn-ejemplo').addEventListener('click', () => llenarEjemplo(true));
    $('#btn-pdf').addEventListener('click', descargarPDF);
  });

  window.RaizCheckout = { abrir, pagar, cancelarPago, diploma };
})();
