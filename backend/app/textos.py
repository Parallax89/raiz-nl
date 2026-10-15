"""Única fábrica de textos para X. El front sólo muestra y reenvía lo que sale de aquí."""
import re

HANDLE_RE = re.compile(r"^[A-Za-z0-9_]{1,15}$")

# Frases que prometen lo que un árbol no cumple (Contexto_Arbol.md): nunca se generan ni se aceptan
PROHIBIDAS = ("acaban de donar", "mejorar el suministro de agua", "suministro de agua en el área metropolitana")


class TextoInvalido(ValueError):
    pass


def limpia_handle(handle: str | None) -> str | None:
    if not handle:
        return None
    h = handle.strip().lstrip("@")
    if not HANDLE_RE.fullmatch(h):
        raise TextoInvalido("Usuario de X inválido: 1 a 15 letras, números o guion bajo.")
    return h


def texto_publicacion(zona, n: int, handle: str | None = None) -> str:
    arboles = "un árbol" if n == 1 else f"{n} árboles"
    if zona.objetivo == "agua":
        if zona.presa_destino:
            texto = f"Donaron {arboles} para restaurar {zona.nombre_texto}, cuenca que aporta a {zona.presa_destino}."
        elif zona.acuifero_destino:
            texto = (f"Donaron {arboles} para restaurar {zona.nombre_texto}, "
                     f"zona de recarga del acuífero {zona.acuifero_destino}.")
        else:
            raise TextoInvalido("Zona de agua sin presa ni acuífero de destino: no se publica.")
    elif zona.objetivo == "aire":
        texto = (f"Donaron {arboles} para arbolado en {zona.nombre_texto}, una zona de {zona.municipio} "
                 "con poca sombra y mala calidad del aire.")
    else:
        raise TextoInvalido(f"Objetivo desconocido: {zona.objetivo}")
    if handle:
        texto += f" @{handle}"
    if any(p in texto.lower() for p in PROHIBIDAS):
        raise TextoInvalido("El texto contiene una promesa prohibida.")
    if len(texto) > 280:
        raise TextoInvalido("El texto rebasa 280 caracteres.")
    return texto
