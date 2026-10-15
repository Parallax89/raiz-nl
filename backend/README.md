# Backend · Raíz NL

API de donaciones: zonas con cupo, donación simbólica, texto canónico con visto bueno y publicación en X.
Sin pagos. Plan y decisiones en [docs/BACKEND.md](../docs/BACKEND.md).

## Correr en local (demo)

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --port 8001          # crea raiz.db y siembra las zonas
# en otra terminal, desde la raíz del repo:
python3 -m http.server 8000 --directory web
# abrir http://localhost:8000  (el portal encuentra la API en el puerto 8001)
```

Desde otro origen: `https://c7b.github.io/raiz-nl/?api=https://<donde-corra-la-api>`.
Sin API, el portal sigue funcionando: guarda compromisos en el navegador y usa el mismo texto canónico.

Pruebas: `python -m pytest -q tests` (12 pruebas: textos, cupo concurrente, visto bueno, cola del bot, expiración, operador).

Volver a sembrar (por ejemplo, cuando el pipeline escriba `web/data/zonas.geojson`): `python -m app.seed --reset`.

## De dónde salen las zonas

1. `backend/data/fichas.json`, si existe (fichas curadas a mano).
2. `web/data/zonas.geojson` (pipeline): mapa y API comparten `id`.
3. `web/data/mock/zonas.geojson`, marcado `mock: true`.

Una zona de agua sin presa de abastecimiento (El Cuchillo, La Boca, Cerro Prieto) ni acuífero identificado
queda **descartada** y no se lista (hoy, con datos de ejemplo: AG-07 Rayones).

## Rutas

| Método | Ruta | Qué hace |
|---|---|---|
| GET | `/api/salud` | Estado y si el bot de X está activo |
| GET | `/api/zonas?objetivo=agua\|aire` | Fichas con `arboles_disponibles`, `arboles_donados`, `texto_ejemplo` |
| GET | `/api/zonas/{id}` | Una ficha |
| POST | `/api/donaciones` | Reserva atómica del cupo (409 si no cabe); devuelve `texto_propuesto`. La reserva vence a los 15 min |
| POST | `/api/donaciones/{id}/confirmar` | Visto bueno: el texto debe ser idéntico al de la plantilla (422 si no). Si `publicar`, intenta publicar |
| POST | `/api/donaciones/{id}/publicar` | Reintento de publicación |
| GET | `/api/resumen` | `donados` (sólo confirmados), `plantados`, `vivos_12m` |
| GET | `/api/bot/pendientes` | Cola de textos aprobados sin publicar (token de operador) |
| POST | `/api/bot/publicadas/{id}` | Marca publicada con `tweet_url` (token de operador) |
| PATCH | `/api/operador/zonas/{id}` | Plantados y vivos a 12 meses (token de operador) |

## Publicación en X: dos caminos

- **Con llaves de la API de X** (`BOT_ENABLED=true` y `X_API_KEY`, `X_API_SECRET`, `X_ACCESS_TOKEN`,
  `X_ACCESS_TOKEN_SECRET` en `backend/.env`): publica en el momento del visto bueno, una sola vez por donación.
- **Sin llaves (por defecto):** la donación se confirma y el texto queda en `/api/bot/pendientes`. Grok Bot,
  con la cuenta de X del equipo conectada, lo atiende con esta rutina:

```
Cada 5 minutos: GET <API>/api/bot/pendientes con el encabezado "Authorization: Bearer <OPERATOR_TOKEN>".
Publica en X cada "texto" tal cual, sin cambiar una letra. Después llama
POST <API>/api/bot/publicadas/<id> con {"tweet_url": "<enlace del post>"} y el mismo encabezado.
No publiques nada que no venga de esa cola.
```

Para que Grok Bot llegue a una API que corre en una laptop hace falta exponerla (por ejemplo, un túnel) o
desplegarla en un servicio con volumen. GitHub Pages sólo sirve `web/`.
