"""Configuración por variables de entorno (o backend/.env)."""
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND = Path(__file__).resolve().parents[1]
REPO = BACKEND.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=BACKEND / ".env", extra="ignore")

    database_url: str = f"sqlite:///{BACKEND / 'raiz.db'}"
    cors_origins: str = "http://localhost:8000,http://127.0.0.1:8000,https://c7b.github.io"
    operator_token: str = ""
    bot_enabled: bool = False
    x_api_key: str = ""
    x_api_secret: str = ""
    x_access_token: str = ""
    x_access_token_secret: str = ""
    reserva_minutos: int = 15
    max_arboles_por_donacion: int = 20
    cupo_por_zona: int = 50          # cupo de demostración si la ficha no trae uno
    fichas_path: str = str(BACKEND / "data" / "fichas.json")
    zonas_geojson: str = str(REPO / "web" / "data" / "zonas.geojson")
    zonas_geojson_mock: str = str(REPO / "web" / "data" / "mock" / "zonas.geojson")


settings = Settings()
