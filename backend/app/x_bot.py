"""Publicación en X desde la cuenta oficial (API v2, OAuth 1.0a de usuario).

Si no hay llaves (BOT_ENABLED=false), la donación se confirma igual y la publicación
queda en la cola /api/bot/pendientes, que puede atender Grok Bot desde la cuenta del equipo.
"""
from .settings import settings


class BotDeshabilitado(RuntimeError):
    pass


def publicar(texto: str) -> tuple[str, str]:
    """Publica y devuelve (tweet_id, tweet_url)."""
    if not settings.bot_enabled:
        raise BotDeshabilitado("bot_disabled")
    if not all([settings.x_api_key, settings.x_api_secret, settings.x_access_token, settings.x_access_token_secret]):
        raise BotDeshabilitado("faltan llaves de X")
    import tweepy
    cliente = tweepy.Client(consumer_key=settings.x_api_key, consumer_secret=settings.x_api_secret,
                            access_token=settings.x_access_token, access_token_secret=settings.x_access_token_secret)
    r = cliente.create_tweet(text=texto)
    tweet_id = str(r.data["id"])
    return tweet_id, f"https://x.com/i/web/status/{tweet_id}"
