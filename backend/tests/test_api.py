from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta

from app import x_bot
from app.db import SessionLocal
from app.models import Donacion, ahora
from app.settings import settings

OP = {"Authorization": "Bearer tok"}


def test_zonas_y_descartadas(client):
    agua = client.get("/api/zonas", params={"objetivo": "agua"}).json()
    aire = client.get("/api/zonas", params={"objetivo": "aire"}).json()
    assert agua and aire and all(z["objetivo"] == "agua" for z in agua)
    assert all(z["presa_destino"] or z["acuifero_destino"] for z in agua)   # máscara de cuenca o acuífero
    ids = {z["id"] for z in agua}
    assert "AG-07" not in ids            # Rayones: sin presa ni acuífero → descartada
    assert all(z["texto_ejemplo"].startswith("Donaron un árbol") for z in agua + aire)
    assert client.get("/api/zonas/AG-07").status_code == 404


def test_cupo_y_409(client):
    zona = client.get("/api/zonas/AG-01").json()
    cupo = zona["arboles_disponibles"]
    r = client.post("/api/donaciones", json={"zona_id": "AG-01", "n_arboles": 20})
    assert r.status_code == 201
    assert client.get("/api/zonas/AG-01").json()["arboles_disponibles"] == cupo - 20
    client.post("/api/donaciones", json={"zona_id": "AG-01", "n_arboles": 20})
    r = client.post("/api/donaciones", json={"zona_id": "AG-01", "n_arboles": 20})
    assert r.status_code == 409 if cupo < 60 else 201


def test_reservas_concurrentes_no_rebasan_el_cupo(client):
    cupo = client.get("/api/zonas/AI-01").json()["arboles_disponibles"]
    def reserva(_):
        return client.post("/api/donaciones", json={"zona_id": "AI-01", "n_arboles": 10}).status_code
    with ThreadPoolExecutor(8) as ex:
        codigos = list(ex.map(reserva, range(cupo // 10 + 4)))
    assert codigos.count(201) == cupo // 10
    assert client.get("/api/zonas/AI-01").json()["arboles_disponibles"] == cupo % 10


def test_confirmar_exige_el_texto_exacto(client):
    d = client.post("/api/donaciones", json={"zona_id": "AG-01", "n_arboles": 1}).json()
    malo = client.post(f"/api/donaciones/{d['id']}/confirmar",
                       json={"texto_confirmado": "Acaban de donar un árbol para mejorar el suministro de agua en el área metropolitana.",
                             "publicar": True})
    assert malo.status_code == 422
    ok = client.post(f"/api/donaciones/{d['id']}/confirmar",
                     json={"texto_confirmado": d["texto_propuesto"], "publicar": False})
    assert ok.status_code == 200 and ok.json()["estado"] == "confirmada"
    # idempotente
    assert client.post(f"/api/donaciones/{d['id']}/confirmar",
                       json={"texto_confirmado": d["texto_propuesto"]}).json()["estado"] == "confirmada"
    # sin visto bueno para publicar, no hay reintento de publicación
    assert client.post(f"/api/donaciones/{d['id']}/publicar").status_code == 409


def test_sin_llaves_queda_en_cola_para_grok_bot(client):
    d = client.post("/api/donaciones", json={"zona_id": "AI-02", "n_arboles": 1, "etiquetar": True,
                                             "handle_x": "@alguien"}).json()
    assert d["texto_propuesto"].endswith(" @alguien")
    r = client.post(f"/api/donaciones/{d['id']}/confirmar",
                    json={"texto_confirmado": d["texto_propuesto"], "publicar": True, "etiquetar": True,
                          "handle_x": "alguien"}).json()
    assert r["publicacion"]["pendiente"] is True
    assert client.get("/api/bot/pendientes").status_code == 401
    cola = client.get("/api/bot/pendientes", headers=OP).json()
    assert [c["texto"] for c in cola if c["id"] == d["id"]] == [d["texto_propuesto"]]
    client.post(f"/api/bot/publicadas/{d['id']}", json={"tweet_url": "https://x.com/raiz/status/1"}, headers=OP)
    assert all(c["id"] != d["id"] for c in client.get("/api/bot/pendientes", headers=OP).json())


def test_bot_con_llaves_publica_una_sola_vez(client, monkeypatch):
    llamadas = []
    monkeypatch.setattr(x_bot, "publicar", lambda t: llamadas.append(t) or ("99", "https://x.com/i/web/status/99"))
    d = client.post("/api/donaciones", json={"zona_id": "AG-02", "n_arboles": 2}).json()
    r = client.post(f"/api/donaciones/{d['id']}/confirmar",
                    json={"texto_confirmado": d["texto_propuesto"], "publicar": True}).json()
    assert r["publicacion"]["ok"] and r["tweet_url"].endswith("/99")
    client.post(f"/api/donaciones/{d['id']}/publicar")
    assert llamadas == [d["texto_propuesto"]]


def test_reserva_vencida_devuelve_cupo_y_resumen_cuenta_solo_confirmadas(client):
    antes = client.get("/api/zonas/AI-03").json()["arboles_disponibles"]
    d = client.post("/api/donaciones", json={"zona_id": "AI-03", "n_arboles": 5}).json()
    assert client.get("/api/resumen").json()["donados"] == 0          # reservada no cuenta como donada
    with SessionLocal() as db:
        db.get(Donacion, d["id"]).expira_at = ahora() - timedelta(minutes=1)
        db.commit()
    assert client.get("/api/zonas/AI-03").json()["arboles_disponibles"] == antes
    assert client.post(f"/api/donaciones/{d['id']}/confirmar",
                       json={"texto_confirmado": d["texto_propuesto"]}).status_code == 410


def test_operador(client):
    assert client.patch("/api/operador/zonas/AG-01", json={"arboles_plantados": 3}).status_code == 401
    z = client.patch("/api/operador/zonas/AG-01", json={"arboles_plantados": 3}, headers=OP).json()
    assert z["arboles_plantados"] == 3
    assert client.get("/api/resumen").json()["plantados"] == 3
