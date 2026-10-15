"""API de Raíz NL: zonas con cupo, donaciones simbólicas, textos canónicos y publicación en X."""
from contextlib import asynccontextmanager
from datetime import timedelta

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from . import x_bot
from .db import Base, SessionLocal, engine, get_db
from .models import Donacion, Publicacion, Zona, ahora
from .seed import sembrar
from .settings import settings
from .textos import TextoInvalido, limpia_handle, texto_publicacion


@asynccontextmanager
async def lifespan(app):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        sembrar(db)
    yield


app = FastAPI(title="Raíz NL", version="0.1", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
                   allow_methods=["*"], allow_headers=["*"])


# ---------- Esquemas ----------
class DonacionIn(BaseModel):
    zona_id: str
    n_arboles: int = Field(1, ge=1)
    publicar: bool = False
    etiquetar: bool = False
    handle_x: str | None = None


class ConfirmarIn(BaseModel):
    texto_confirmado: str
    publicar: bool = False
    etiquetar: bool = False
    handle_x: str | None = None


class PublicadaIn(BaseModel):
    tweet_url: str


class OperadorZonaIn(BaseModel):
    arboles_plantados: int | None = Field(None, ge=0)
    vivos_12m: int | None = Field(None, ge=0)


# ---------- Utilidades ----------
def expira_reservas(db: Session):
    """Cancela reservas sin confirmar y devuelve su cupo (chequeo perezoso)."""
    vencidas = db.scalars(select(Donacion).where(Donacion.estado == "reservada", Donacion.expira_at < ahora())).all()
    for d in vencidas:
        d.estado = "expirada"
        db.execute(update(Zona).where(Zona.id == d.zona_id)
                   .values(arboles_comprometidos=Zona.arboles_comprometidos - d.n_arboles))
    if vencidas:
        db.commit()


def donados_por_zona(db: Session) -> dict[str, int]:
    filas = db.execute(select(Donacion.zona_id, func.sum(Donacion.n_arboles))
                       .where(Donacion.estado.in_(["confirmada", "plantada"])).group_by(Donacion.zona_id)).all()
    return {z: int(n) for z, n in filas}


def zona_out(z: Zona, donados: int) -> dict:
    try:
        ejemplo = texto_publicacion(z, 1)
    except TextoInvalido:
        ejemplo = None
    return dict(id=z.id, objetivo=z.objetivo, nombre=z.nombre, municipio=z.municipio, razon=z.razon,
                presa_destino=z.presa_destino, acuifero_destino=z.acuifero_destino, estacion_sima=z.estacion_sima,
                operador=z.operador, arboles_caben=z.arboles_caben, arboles_donados=donados,
                arboles_disponibles=z.arboles_caben - z.arboles_comprometidos,
                arboles_plantados=z.arboles_plantados, vivos_12m=z.vivos_12m,
                centro=[z.lat, z.lon] if z.lat is not None else None, texto_ejemplo=ejemplo, mock=z.mock)


def donacion_out(d: Donacion, publicacion: dict | None = None) -> dict:
    salida = dict(id=d.id, estado=d.estado, zona_id=d.zona_id, n_arboles=d.n_arboles,
                  texto_propuesto=d.texto_propuesto, texto_confirmado=d.texto_confirmado,
                  expira_at=d.expira_at.isoformat() + "Z", tweet_url=d.tweet_url, error_x=d.error_x)
    if publicacion is not None:
        salida["publicacion"] = publicacion
    return salida


def exige_operador(authorization: str | None = Header(None)):
    if not settings.operator_token or authorization != f"Bearer {settings.operator_token}":
        raise HTTPException(401, "Token de operador inválido")


def intenta_publicar(db: Session, d: Donacion) -> dict:
    if d.tweet_id or d.tweet_url:
        return {"ok": True, "tweet_url": d.tweet_url}
    if not d.consentimiento_at:
        raise HTTPException(403, "Sin visto bueno del texto no se publica")
    try:
        tweet_id, url = x_bot.publicar(d.texto_confirmado)
    except x_bot.BotDeshabilitado as e:
        d.error_x = str(e)
        db.commit()
        return {"ok": False, "pendiente": True, "error": str(e),
                "nota": "Queda en la cola /api/bot/pendientes para publicarse desde la cuenta del proyecto."}
    except Exception as e:  # X caído, 429, llaves malas: la donación sigue confirmada
        d.error_x = str(e)[:300]
        db.add(Publicacion(donacion_id=d.id, via="api_x", texto=d.texto_confirmado, ok=False, error=d.error_x))
        db.commit()
        return {"ok": False, "error": d.error_x}
    d.tweet_id, d.tweet_url, d.error_x = tweet_id, url, None
    db.add(Publicacion(donacion_id=d.id, via="api_x", texto=d.texto_confirmado, ok=True, tweet_id=tweet_id, tweet_url=url))
    db.commit()
    return {"ok": True, "tweet_url": url}


# ---------- Rutas ----------
@app.get("/api/salud")
def salud():
    return {"ok": True, "bot_x": settings.bot_enabled}


@app.get("/api/zonas")
def listar_zonas(objetivo: str | None = Query(None, pattern="^(agua|aire)$"), db: Session = Depends(get_db)):
    expira_reservas(db)
    q = select(Zona).where(Zona.descartada.is_(False))
    if objetivo:
        q = q.where(Zona.objetivo == objetivo)
    donados = donados_por_zona(db)
    return [zona_out(z, donados.get(z.id, 0)) for z in db.scalars(q.order_by(Zona.id)).all()]


@app.get("/api/zonas/{zona_id}")
def una_zona(zona_id: str, db: Session = Depends(get_db)):
    expira_reservas(db)
    z = db.get(Zona, zona_id)
    if not z or z.descartada:
        raise HTTPException(404, "Zona no encontrada")
    return zona_out(z, donados_por_zona(db).get(z.id, 0))


@app.post("/api/donaciones", status_code=201)
def donar(body: DonacionIn, db: Session = Depends(get_db)):
    if body.n_arboles > settings.max_arboles_por_donacion:
        raise HTTPException(422, f"Máximo {settings.max_arboles_por_donacion} árboles por donación")
    try:
        handle = limpia_handle(body.handle_x) if body.etiquetar else None
    except TextoInvalido as e:
        raise HTTPException(422, str(e))
    if body.etiquetar and not handle:
        raise HTTPException(422, "Para etiquetar hace falta el usuario de X")
    expira_reservas(db)
    z = db.get(Zona, body.zona_id)
    if not z or z.descartada:
        raise HTTPException(404, "Zona no encontrada")
    try:
        texto = texto_publicacion(z, body.n_arboles, handle)
    except TextoInvalido as e:
        raise HTTPException(422, str(e))
    # Reserva atómica: sólo descuenta si cabe
    r = db.execute(update(Zona).where(Zona.id == z.id,
                                      Zona.arboles_comprometidos + body.n_arboles <= Zona.arboles_caben)
                   .values(arboles_comprometidos=Zona.arboles_comprometidos + body.n_arboles))
    if r.rowcount == 0:
        db.rollback()
        raise HTTPException(409, "Ya no hay cupo en esta zona")
    d = Donacion(zona_id=z.id, n_arboles=body.n_arboles, publicar=body.publicar, etiquetar=bool(handle),
                 handle_x=handle, texto_propuesto=texto,
                 expira_at=ahora() + timedelta(minutes=settings.reserva_minutos))
    db.add(d)
    db.commit()
    return donacion_out(d)


@app.post("/api/donaciones/{donacion_id}/confirmar")
def confirmar(donacion_id: str, body: ConfirmarIn, db: Session = Depends(get_db)):
    expira_reservas(db)
    d = db.get(Donacion, donacion_id)
    if not d:
        raise HTTPException(404, "Donación no encontrada")
    if d.estado == "expirada":
        raise HTTPException(410, "La reserva expiró; vuelve a donar")
    if d.estado in ("confirmada", "plantada"):
        return donacion_out(d)                       # idempotente
    try:
        handle = limpia_handle(body.handle_x) if body.etiquetar else None
    except TextoInvalido as e:
        raise HTTPException(422, str(e))
    esperado = texto_publicacion(db.get(Zona, d.zona_id), d.n_arboles, handle)
    if body.texto_confirmado != esperado:
        raise HTTPException(422, {"error": "El texto no coincide con la plantilla", "esperado": esperado})
    d.estado, d.texto_confirmado = "confirmada", esperado
    d.publicar, d.etiquetar, d.handle_x = body.publicar, bool(handle), handle
    d.consentimiento_at = ahora() if body.publicar else None
    db.commit()
    publicacion = intenta_publicar(db, d) if d.publicar else None
    return donacion_out(d, publicacion)


@app.post("/api/donaciones/{donacion_id}/publicar")
def reintentar(donacion_id: str, db: Session = Depends(get_db)):
    d = db.get(Donacion, donacion_id)
    if not d:
        raise HTTPException(404, "Donación no encontrada")
    if d.estado not in ("confirmada", "plantada") or not d.publicar:
        raise HTTPException(409, "La donación no está confirmada para publicarse")
    return donacion_out(d, intenta_publicar(db, d))


@app.get("/api/resumen")
def resumen(db: Session = Depends(get_db)):
    expira_reservas(db)
    zonas = db.scalars(select(Zona).where(Zona.descartada.is_(False))).all()
    donados = donados_por_zona(db)
    vivos = [z.vivos_12m for z in zonas if z.vivos_12m is not None]
    por_obj = {}
    for z in zonas:
        o = por_obj.setdefault(z.objetivo, {"donados": 0, "plantados": 0, "zonas": 0})
        o["donados"] += donados.get(z.id, 0)
        o["plantados"] += z.arboles_plantados
        o["zonas"] += 1
    return {"mock": any(z.mock for z in zonas), "donados": sum(donados.values()),
            "plantados": sum(z.arboles_plantados for z in zonas), "vivos_12m": sum(vivos) if vivos else None,
            "por_objetivo": por_obj,
            "zonas": [{"id": z.id, "donados": donados.get(z.id, 0),
                       "disponibles": z.arboles_caben - z.arboles_comprometidos} for z in zonas]}


# ---------- Cola para Grok Bot (publica desde la cuenta del equipo sin llaves en el servidor) ----------
@app.get("/api/bot/pendientes", dependencies=[Depends(exige_operador)])
def pendientes(db: Session = Depends(get_db)):
    q = select(Donacion).where(Donacion.estado.in_(["confirmada", "plantada"]), Donacion.publicar.is_(True),
                               Donacion.consentimiento_at.is_not(None), Donacion.tweet_url.is_(None))
    return [{"id": d.id, "texto": d.texto_confirmado, "confirmada": d.consentimiento_at.isoformat() + "Z"}
            for d in db.scalars(q.order_by(Donacion.consentimiento_at)).all()]


@app.post("/api/bot/publicadas/{donacion_id}", dependencies=[Depends(exige_operador)])
def marcar_publicada(donacion_id: str, body: PublicadaIn, db: Session = Depends(get_db)):
    d = db.get(Donacion, donacion_id)
    if not d or not d.consentimiento_at:
        raise HTTPException(404, "Donación sin visto bueno o inexistente")
    if not d.tweet_url:
        d.tweet_url, d.error_x = body.tweet_url, None
        db.add(Publicacion(donacion_id=d.id, via="grok_bot", texto=d.texto_confirmado, ok=True, tweet_url=body.tweet_url))
        db.commit()
    return donacion_out(d)


# ---------- Operador ----------
@app.patch("/api/operador/zonas/{zona_id}", dependencies=[Depends(exige_operador)])
def operador_zona(zona_id: str, body: OperadorZonaIn, db: Session = Depends(get_db)):
    z = db.get(Zona, zona_id)
    if not z:
        raise HTTPException(404, "Zona no encontrada")
    if body.arboles_plantados is not None:
        z.arboles_plantados = body.arboles_plantados
    if body.vivos_12m is not None:
        z.vivos_12m = body.vivos_12m
    db.commit()
    return zona_out(z, donados_por_zona(db).get(z.id, 0))
