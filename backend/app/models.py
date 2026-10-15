import uuid
from datetime import datetime, timezone

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


def ahora():
    return datetime.now(timezone.utc).replace(tzinfo=None)   # UTC sin zona (SQLite)


class Zona(Base):
    __tablename__ = "zonas"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    objetivo: Mapped[str] = mapped_column(String)                 # agua | aire
    nombre: Mapped[str] = mapped_column(String)                   # como aparece en el mapa
    nombre_texto: Mapped[str] = mapped_column(String)             # como se nombra en la publicación
    municipio: Mapped[str] = mapped_column(String)
    razon: Mapped[str] = mapped_column(Text)
    presa_destino: Mapped[str | None] = mapped_column(String, nullable=True)
    acuifero_destino: Mapped[str | None] = mapped_column(String, nullable=True)
    estacion_sima: Mapped[str | None] = mapped_column(String, nullable=True)
    operador: Mapped[str] = mapped_column(String)
    arboles_caben: Mapped[int] = mapped_column(Integer)
    # Reservados + confirmados: es lo que se descuenta del cupo
    arboles_comprometidos: Mapped[int] = mapped_column(Integer, default=0)
    arboles_plantados: Mapped[int] = mapped_column(Integer, default=0)
    vivos_12m: Mapped[int | None] = mapped_column(Integer, nullable=True)
    descartada: Mapped[bool] = mapped_column(Boolean, default=False)
    motivo_descarte: Mapped[str | None] = mapped_column(String, nullable=True)
    mock: Mapped[bool] = mapped_column(Boolean, default=False)
    lat: Mapped[float | None] = mapped_column(Float, nullable=True)
    lon: Mapped[float | None] = mapped_column(Float, nullable=True)


class Donacion(Base):
    __tablename__ = "donaciones"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    zona_id: Mapped[str] = mapped_column(ForeignKey("zonas.id"))
    n_arboles: Mapped[int] = mapped_column(Integer)
    estado: Mapped[str] = mapped_column(String, default="reservada")   # reservada|confirmada|expirada|plantada
    publicar: Mapped[bool] = mapped_column(Boolean, default=False)
    etiquetar: Mapped[bool] = mapped_column(Boolean, default=False)
    handle_x: Mapped[str | None] = mapped_column(String, nullable=True)
    texto_propuesto: Mapped[str] = mapped_column(Text)
    texto_confirmado: Mapped[str | None] = mapped_column(Text, nullable=True)
    consentimiento_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    tweet_id: Mapped[str | None] = mapped_column(String, nullable=True)
    tweet_url: Mapped[str | None] = mapped_column(String, nullable=True)
    error_x: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=ahora)
    expira_at: Mapped[datetime] = mapped_column(DateTime)


class Publicacion(Base):
    """Bitácora del bot: una fila por intento. Sirve para no publicar dos veces."""
    __tablename__ = "publicaciones"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    donacion_id: Mapped[str] = mapped_column(ForeignKey("donaciones.id"))
    via: Mapped[str] = mapped_column(String)            # api_x | grok_bot
    texto: Mapped[str] = mapped_column(Text)
    ok: Mapped[bool] = mapped_column(Boolean)
    tweet_id: Mapped[str | None] = mapped_column(String, nullable=True)
    tweet_url: Mapped[str | None] = mapped_column(String, nullable=True)
    error: Mapped[str | None] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=ahora)
