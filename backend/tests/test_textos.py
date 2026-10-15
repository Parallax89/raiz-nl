from types import SimpleNamespace as Z

import pytest

from app.textos import PROHIBIDAS, TextoInvalido, limpia_handle, texto_publicacion

AGUA = Z(objetivo="agua", nombre_texto="Los Cuartones", presa_destino="El Cuchillo", acuifero_destino=None, municipio="Santiago")
RECARGA = Z(objetivo="agua", nombre_texto="Cañón de la Huasteca", presa_destino=None, acuifero_destino="Campo Buenos Aires", municipio="Santa Catarina")
AIRE = Z(objetivo="aire", nombre_texto="los alrededores de la estación Sureste 2 del SIMA", presa_destino=None, acuifero_destino=None, municipio="Juárez")


def test_plantillas_del_contexto():
    assert texto_publicacion(AGUA, 1) == "Donaron un árbol para restaurar Los Cuartones, cuenca que aporta a El Cuchillo."
    assert texto_publicacion(AGUA, 3).startswith("Donaron 3 árboles para restaurar")
    assert texto_publicacion(RECARGA, 1).endswith("zona de recarga del acuífero Campo Buenos Aires.")
    assert texto_publicacion(AIRE, 1) == ("Donaron un árbol para arbolado en los alrededores de la estación Sureste 2 "
                                          "del SIMA, una zona de Juárez con poca sombra y mala calidad del aire.")
    assert texto_publicacion(AGUA, 1, "alguien").endswith(" @alguien")


def test_nunca_sale_el_texto_prohibido():
    for z in (AGUA, RECARGA, AIRE):
        for n in (1, 5):
            t = texto_publicacion(z, n).lower()
            assert not any(p in t for p in PROHIBIDAS)


def test_agua_sin_destino_no_se_publica():
    with pytest.raises(TextoInvalido):
        texto_publicacion(Z(objetivo="agua", nombre_texto="X", presa_destino=None, acuifero_destino=None, municipio=""), 1)


def test_handle():
    assert limpia_handle("@raiz_nl") == "raiz_nl"
    for malo in ("con espacio", "a" * 16, "ñandú"):
        with pytest.raises(TextoInvalido):
            limpia_handle(malo)
