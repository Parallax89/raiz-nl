# Plan de backend · Raíz NL

Documento para construir el backend completo del portal. Alinea `Contexto_Arbol.md` (discurso y reglas) con el contrato de datos del README. **No hay pasarela de pago.** Sí hay bot de X con publicación automática, solo después del visto bueno.

El portal estático (`web/`) no basta para donar ni para publicar: hay que reservar árboles contra la meta de cada zona y emitir el post desde una cuenta oficial.

## Ajustes al plan (14-oct, 19:30) · lo que ya está construido

El plan original suma de 4 a 5 horas de cortes. Para la demostración se construyó todo junto, con estos cambios:

1. **Cupo separado de donados.** `arboles_comprometidos` (reservados + confirmados) controla el cupo; `donados` en el
   resumen cuenta sólo confirmados. Así una reserva sin confirmar no infla el contador público.
2. **Acuífero además de presa.** El reto 1 habla de infiltración del acuífero: una zona de agua se acepta si aporta a
   una presa de abastecimiento **o** recarga un acuífero identificado. Texto: «Donaron un árbol para restaurar
   {zona}, zona de recarga del acuífero {acuífero}.» Sin ninguno de los dos, la zona queda descartada.
3. **Las zonas se siembran del mismo GeoJSON que pinta el mapa** (`web/data/zonas.geojson` o el mock), para que mapa
   y API compartan `id` y nombre. `backend/data/fichas.json`, si existe, manda.
4. **Bot de X sin llaves en el servidor.** Además de la API de X (tweepy), hay una cola
   (`/api/bot/pendientes` → `/api/bot/publicadas/{id}`) que atiende Grok Bot con la cuenta del equipo. Es el
   camino natural en un build day de Grok y evita depender del acceso pagado a la API de X.
5. **El portal funciona con o sin API.** Con API reserva, confirma y muestra cupo; sin API guarda en el navegador.
   En ambos casos el texto es el canónico y el texto prohibido desapareció de `web/app.js` y del README.
6. **Fuera del corte:** despliegue en un servicio con volumen, expiración por tarea programada (hoy es perezosa) y
   panel de operador.

Pruebas: `backend/tests` (12). Cómo correrlo: [backend/README.md](../backend/README.md).

## Qué cubre este backend

1. Servir las zonas (5–8 agua, 5–8 aire) con ficha, capacidad y avance.
2. Registrar donaciones simbólicas y restar del cupo.
3. Armar el texto canónico, pedir confirmación y publicar con el bot de X.
4. Exponer un contador público: `donados` ahora; `plantados` y `vivos_12m` cuando un operador verifique.

## Qué no entra (todavía)

- Cobro, recibos fiscales, donataria autorizada.
- Inventario de emisiones ni Sentinel-5P en el runtime.
- Mapa de todos los incendios del estado.
- Cuentas de usuario / login ciudadano.
- Verificación satelital NDVI. El campo existe en el modelo; el job no.

El pipeline (`pipeline/`) sigue siendo **generación de capas**, no el API. El backend **lee** GeoJSON/fichas; no recalcula scores en cada request.

---

## Stack

| Pieza | Elección | Por qué |
|---|---|---|
| API | FastAPI + Pydantic v2 | El equipo ya está en Python (`pipeline/`). Tipado, CORS, OpenAPI para el front. |
| Persistencia | SQLite en el hackathon; el esquema es el de Postgres | Un archivo, cero ops. Misma SQL. |
| ORM | SQLAlchemy 2.x | Transacciones al reservar cupo. |
| Geo | GeoJSON estático en `web/data/` + tabla `zonas` | El mapa lee polígonos; el API lee cupo y fichas. |
| X | API v2, OAuth 1.0a de la **cuenta oficial** | El bot publica el texto confirmado. Sin bot no hay post. |
| Auth | Ninguna para el ciudadano. Token de operador (`OPERATOR_TOKEN`) para marcar plantado. | Hackathon: donar no pide cuenta. |
| Hosting | Un servicio (Railway / Render / Fly) + SQLite en volumen, o Postgres del mismo host | GitHub Pages solo sirve `web/`. El API vive aparte. |
| Front | Sigue estático; apunta `API_BASE` | En local: `http://127.0.0.1:8000`. |

Dependencias previstas: `fastapi`, `uvicorn[standard]`, `sqlalchemy`, `pydantic-settings`, `httpx`, `python-dotenv`. Cliente de X: `tweepy` (API v2 + OAuth 1.0a user context).

Árbol de código:

```
backend/
  app/
    main.py              # FastAPI, CORS, lifespan (create tables)
    settings.py          # env
    db.py                # engine + Session
    models.py
    schemas.py
    seed.py              # carga fichas → tabla zonas
    routers/
      zonas.py
      donaciones.py
      salud.py
    services/
      cupo.py            # reserva atómica
      texto.py           # plantillas canónicas (nunca el texto prohibido)
      x_bot.py           # POST tweets
    templates/
      textos.py
  data/
    fichas.json          # fuente de verdad de las 10–16 zonas
  tests/
    test_cupo.py
    test_texto.py
    test_donaciones.py
  requirements.txt
  README.md
```

---

## Modelo de datos

### Zona (`zonas`)

Sembrada desde `backend/data/fichas.json`. El GeoJSON del mapa usa el mismo `id`.

| Campo | Tipo | Notas |
|---|---|---|
| `id` | text PK | `AG-01` … / `AI-01` … |
| `objetivo` | `agua` \| `aire` | |
| `nombre` | text | p. ej. Los Cuartones |
| `municipio` | text | |
| `razon` | text | Una frase. Lo que ve la gente. |
| `presa_destino` | text null | Solo agua. El Cuchillo / La Boca / Cerro Prieto. |
| `estacion_sima` | text null | Solo aire. Nombre de estación. |
| `operador` | text | Quién planta. |
| `arboles_caben` | int | Meta. |
| `arboles_donados` | int | Suma de donaciones `confirmada`. Default 0. |
| `arboles_plantados` | int | Lo pone el operador. Default 0. |
| `vivos_12m` | int null | Vacío hasta verificación. |
| `descartada` | bool | Si true, no se lista. Motivo en `motivo_descarte`. |
| `geom` | JSON null | Opcional; el polígono puede vivir solo en `web/data/zonas.geojson`. |

Regla de cupo: `donados + n <= caben`. Si no cabe, 409.

### Donación (`donaciones`)

| Campo | Tipo | Notas |
|---|---|---|
| `id` | uuid PK | Se lo queda el front (no hay login). |
| `zona_id` | FK | |
| `n_arboles` | int ≥ 1 | Tope por request: 20. |
| `estado` | enum | `reservada` → `confirmada` → (`plantada` más adelante) |
| `publicar` | bool | ¿Quiere post? |
| `etiquetar` | bool | ¿Mencionar handle? |
| `handle_x` | text null | Sin `@`. Solo si `etiquetar`. |
| `texto_propuesto` | text | Lo que vio en pantalla. |
| `texto_confirmado` | text null | Exactamente lo que se tuitea. Debe coincidir con plantilla. |
| `consentimiento_at` | timestamptz null | Obligatorio para publicar. |
| `tweet_id` | text null | |
| `tweet_url` | text null | |
| `error_x` | text null | Si el bot falla, la donación **sigue confirmada**. |
| `created_at` | timestamptz | |

Estados:

1. `POST /donaciones` → `reservada` (cupo ya descontado).
2. `POST /donaciones/{id}/confirmar` → `confirmada`. Si `publicar`, el bot corre **después** de persistir el consentimiento.
3. Si el bot falla: estado sigue `confirmada`, `error_x` lleno, el front ofrece reintento `POST .../publicar`.
4. Operador: `PATCH /operador/donaciones/{id}` → `plantada` (fase 4; endpoint existe, UI no es crítica hoy).

Expiración: una `reservada` sin confirmar a los **15 minutos** se cancela y se devuelve el cupo (job o chequeo lazy en el GET de zona).

### Publicación (`publicaciones`) — log del bot

Una fila por intento: `donacion_id`, `texto`, `ok`, `tweet_id`, `error`, `created_at`. Sirve para no tuitear dos veces (único parcial en `donacion_id` donde `ok=true`).

### Contador público

`GET /resumen` agrega:

- `donados` = suma `n_arboles` de donaciones `confirmada` + `plantada`
- `plantados` = suma de zonas o de donaciones `plantada` (lo que el operador haya marcado)
- `vivos_12m` = null o suma; **no se muestra** si es null

El copy del portal usa esas tres palabras y no otras.

---

## Contrato HTTP

Base: `/api`. JSON. CORS: origen del Pages (`https://<org>.github.io`) y `http://localhost:8000`.

### Salud

`GET /api/salud` → `{ "ok": true }`

### Zonas

`GET /api/zonas?objetivo=agua|aire`

Lista 5–8 no descartadas. Cada item:

```json
{
  "id": "AG-01",
  "objetivo": "agua",
  "nombre": "Los Cuartones",
  "municipio": "Santiago",
  "razon": "Cicatriz reciente en ladera que escurre hacia El Cuchillo.",
  "presa_destino": "El Cuchillo",
  "estacion_sima": null,
  "operador": "a definir",
  "arboles_caben": 400,
  "arboles_donados": 12,
  "arboles_disponibles": 388,
  "arboles_plantados": 0,
  "vivos_12m": null
}
```

`GET /api/zonas/{id}` — igual, una ficha.

No se exponen descartadas. Esas viven en `docs/sitios_descartados.md` (fase 1), no en el API público.

### Donar

`POST /api/donaciones`

```json
{
  "zona_id": "AG-01",
  "n_arboles": 1,
  "publicar": true,
  "etiquetar": false,
  "handle_x": null
}
```

Respuesta 201:

```json
{
  "id": "uuid",
  "estado": "reservada",
  "zona_id": "AG-01",
  "n_arboles": 1,
  "texto_propuesto": "Donaron un árbol para restaurar Los Cuartones, cuenca que aporta a El Cuchillo.",
  "expira_at": "..."
}
```

Errores: 404 zona, 409 sin cupo, 422 handle inválido o `etiquetar` sin handle.

### Confirmar (visto bueno del texto)

`POST /api/donaciones/{id}/confirmar`

```json
{
  "texto_confirmado": "Donaron un árbol para restaurar Los Cuartones, cuenca que aporta a El Cuchillo.",
  "publicar": true,
  "etiquetar": true,
  "handle_x": "alguien"
}
```

Reglas:

- `texto_confirmado` **debe ser byte-a-byte** el que arma `services/texto.py` para esa zona y `n`. Si el cliente manda otro, 422. Así no se cuela el texto prohibido.
- Sin este POST el bot **no corre**.
- Idempotente: segundo confirm ya `confirmada` devuelve 200 con el mismo cuerpo.

Si `publicar=true`, el servidor llama al bot en el mismo request (timeout ~8 s) o encola; para el demo, **síncrono** es más simple. Si X falla, 201/200 de donación confirmada más `"publicacion": { "ok": false, "error": "..." }`.

### Reintento de post

`POST /api/donaciones/{id}/publicar` — solo si ya `confirmada`, `publicar` y aún no hay `tweet_id`.

### Resumen

`GET /api/resumen` → totas, por objetivo y por zona (id, donados, disponibles).

### Operador (después del demo, mismo código)

`PATCH /api/operador/zonas/{id}` header `Authorization: Bearer $OPERATOR_TOKEN`

Cuerpo: `{ "arboles_plantados": 10, "vivos_12m": null }`.

---

## Textos (el backend es el dueño)

`services/texto.py` es la única fábrica. El front solo muestra y reenvía.

Agua, 1 árbol:

`Donaron un árbol para restaurar {nombre}, cuenca que aporta a {presa_destino}.`

Agua, n>1: `Donaron {n} árboles para restaurar ...`

Aire, 1:

`Donaron un árbol para arbolado en {nombre}, una zona de {municipio} con poca sombra y mala calidad del aire.`

Si `etiquetar` y hay handle: se añade ` @{handle}` al final. El handle se valida: `^[A-Za-z0-9_]{1,15}$`.

**Prohibido** generar o aceptar:

`Acaban de donar un árbol para mejorar el suministro de agua en el área metropolitana.`

Tests unitarios: el prohibido nunca sale; n=1 vs n>1; agua sin presa → no se permite sembrar esa ficha.

---

## Bot de X

Cuenta oficial del proyecto. Credenciales en env, nunca en git.

```
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
X_BEARER_TOKEN=          # opcional, lectura
BOT_ENABLED=true         # false en local sin llaves: confirma donación y deja error_x="bot_disabled"
```

Flujo:

1. Ciudadano ve `texto_propuesto`.
2. Confirma. Se guarda `consentimiento_at`.
3. `x_bot.publicar(texto)` → `POST /2/tweets`.
4. Se guarda `tweet_id`. Un único tweet exitoso por donación.

Sin consentimiento → 403. Texto distinto a la plantilla → 422. Bot deshabilitado → donación ok, post no.

Rate limit: si X responde 429, no reintentar en bucle en el request; dejar `error_x` y que el front llame `/publicar`.

En tests: httpx mock / tweepy stub. Un test de contrato verifica que no se llama a X si `consentimiento_at` es null.

---

## Semilla de zonas (bloqueante)

El API no arranca útil sin `backend/data/fichas.json`. Eso es la fase 1 del contexto. Mientras las fichas reales no existan, semilla **explícitamente mock** (campo `"mock": true` en resumen) con 6 agua + 6 aire, ids estables, textos ya canónicos, cupos chicos (p. ej. 50) para demo de 409.

Cada ficha mock debe poder sustituirse por la real sin cambiar el contrato HTTP.

Campos mínimos por ficha: los de la tabla `zonas` salvo contadores (esos salen en 0).

Sitios de agua candidatos a revisar (no sembrar hasta filtrar cuenca): tabla de `Contexto_Arbol.md`. Lampazos no entra. Puerto de Dolores, Vacas, Galeana: fuera hasta confirmar presa.

---

## Orden de implementación

Hacerlo en este orden; cada corte deja el API usable.

### Corte B0 — esqueleto (30–40 min)

- `backend/` con FastAPI, settings, SQLite, `GET /api/salud`.
- CORS. `uvicorn app.main:app --reload --app-dir backend` o paquete `backend.app`.
- README de cómo correr.

### Corte B1 — zonas (40 min)

- Modelos `Zona`, seed desde JSON mock.
- `GET /api/zonas` y `GET /api/zonas/{id}` con `arboles_disponibles`.
- Test: agua y aire se filtran; descartada no aparece.

### Corte B2 — cupo y donación (45 min)

- `POST /donaciones` con transacción: `UPDATE zonas SET arboles_donados = arboles_donados + :n WHERE id=:id AND arboles_donados + :n <= arboles_caben`.
- Si rowcount 0 → 409.
- Expiración lazy de reservas.
- Tests de carrera: dos reservas que suman más que el cupo; una gana.

### Corte B3 — textos (20 min)

- Plantillas + tests del prohibido.
- El POST de donación ya devuelve `texto_propuesto`.

### Corte B4 — confirmar + bot (45–60 min)

- `POST /confirmar` con igualdad estricta de texto.
- `services/x_bot.py` detrás de `BOT_ENABLED`.
- Log `publicaciones`, idempotencia.
- Test: sin confirmación no hay llamada a X; con confirmación sí.

### Corte B5 — resumen y enganche al front (30 min)

- `GET /api/resumen`.
- Variable `API_BASE` en `web/`. El mapa sigue leyendo GeoJSON; donar y contador pegan al API.
- CORS de GitHub Pages.

### Corte B6 — operador (opcional el mismo día)

- Token + PATCH plantados. El contador público ya distingue donados vs plantados.

---

## Variables de entorno

```
DATABASE_URL=sqlite:///./raiz.db
CORS_ORIGINS=http://localhost:8000,http://127.0.0.1:8000
OPERATOR_TOKEN=
BOT_ENABLED=false
X_API_KEY=
X_API_SECRET=
X_ACCESS_TOKEN=
X_ACCESS_TOKEN_SECRET=
RESERVA_MINUTOS=15
MAX_ARBOLES_POR_DONACION=20
```

`.env` en `.gitignore` (ya está).

---

## Cómo se relaciona con el resto del repo

| Pieza | Rol respecto al backend |
|---|---|
| `docs/Contexto_Arbol.md` | Reglas de discurso y de qué zona existe. |
| `docs/FUENTES.md` | Inputs del **pipeline**, no del API. |
| `pipeline/` | Escribe `web/data/*.geojson`. El seed de fichas puede copiar nombre/id de ahí cuando exista `zonas.geojson` real. |
| `web/` | UI y mapa. Llama `/api` para lista viva, donar, confirmar, resumen. |
| GitHub Pages | Solo `web/`. El API no se despliega ahí. |

Contrato GeoJSON del README (`score`, celdas 2 km) es para el mapa/dashboard. El backend de donación trabaja sobre **fichas** (pocos sitios), no sobre cada celda. Si más adelante se dona a una celda, se añade `celda_id`; no es v0.

---

## Criterio de “backend completo” para el demo

- Elegir agua o aire → 5–8 fichas con cupo.
- Donar n árboles → cupo baja.
- Ver el texto correcto (nunca el prohibido) → confirmar → tweet en la cuenta oficial **o** `error_x` visible si las llaves no están.
- Resumen: donados ≠ plantados.
- Sin llaves de X, el resto funciona (`BOT_ENABLED=false`).

Cuando eso corre en local contra SQLite, el backend está listo para cablear el front y, después, subir el API a un host con volumen y secretos de X.
