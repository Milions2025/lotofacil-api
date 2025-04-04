from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from datetime import datetime
import pytz
import random
import os
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# MODELOS E UTILITÁRIOS
# -------------------------------

def salvar_historico(tipo, dezenas):
    historico_path = "historico_apostas.json"
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(fuso_brasilia)
    registro = {
        "tipo": tipo,
        "dezenas": dezenas,
        "data_hora": agora.strftime("%Y-%m-%d %H:%M:%S")
    }

    if os.path.exists(historico_path):
        with open(historico_path, "r") as f:
            historico = json.load(f)
    else:
        historico = []

    historico.insert(0, registro)

    with open(historico_path, "w") as f:
        json.dump(historico, f, indent=4)


def gerar_aposta():
    dezenas_disponiveis = list(range(1, 26))
    return sorted(random.sample(dezenas_disponiveis, 15))


def analisar_aposta_manual(dezenas):
    pares = len([d for d in dezenas if d % 2 == 0])
    primos = len([d for d in dezenas if d in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
    repetidas = len(set(dezenas)) != len(dezenas)
    score = round((15 + primos + pares) / 5.5, 2)
    return {
        "pares": pares,
        "primos": primos,
        "repetidas": "Sim" if repetidas else "Não",
        "score": score,
        "avaliacao": "Alta chance de acerto" if score >= 6 else "Aposta comum"
    }

# -------------------------------
# MODELO PARA APOSTA MANUAL
# -------------------------------

class ApostaManual(BaseModel):
    dezenas: List[int]

# -------------------------------
# ENDPOINTS
# -------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_aposta() for _ in range(3)]
    for aposta in apostas:
        salvar_historico("gerar-apostas", aposta)
    return {"origem": "gerar-apostas", "apostas": apostas}


@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_aposta()
    salvar_historico("aposta-bonus", aposta)
    return {"origem": "aposta-bonus", "aposta": aposta}


@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_aposta()
    salvar_historico("aposta-experimental", aposta)
    return {"origem": "aposta-experimental", "aposta": aposta}


@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_aposta()
    salvar_historico("refinar", aposta)
    return {"origem": "refinar", "aposta": aposta}


@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        analise = analisar_aposta_manual(aposta.dezenas)
        salvar_historico("analisar-aposta", aposta.dezenas)
        return {"origem": "analisar-aposta", "dezenas": aposta.dezenas, **analise}
    except Exception as e:
        return {"erro": str(e)}


@app.get("/historico")
def ver_historico(tipo: str = None, data: str = None):
    historico_path = "historico_apostas.json"
    if not os.path.exists(historico_path):
        return []

    with open(historico_path, "r") as f:
        historico = json.load(f)

    if tipo:
        historico = [h for h in historico if h["tipo"] == tipo]

    if data:
        historico = [h for h in historico if data in h["data_hora"]]

    return historico
