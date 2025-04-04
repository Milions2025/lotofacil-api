from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz
import random
import json
import os

app = FastAPI()

# Liberação de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho para salvar apostas
HISTORICO_PATH = "historico_apostas.json"

# -------------------------------
# FUNÇÕES INTERNAS
# -------------------------------

def salvar_aposta(tipo, aposta):
    zona = pytz.timezone("America/Sao_Paulo")
    data_hora = datetime.now(zona).strftime("%Y-%m-%d %H:%M:%S")
    nova_aposta = {"tipo": tipo, "aposta": aposta, "data": data_hora}

    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
            historico = json.load(f)
    else:
        historico = []

    historico.insert(0, nova_aposta)
    with open(HISTORICO_PATH, "w", encoding="utf-8") as f:
        json.dump(historico, f, indent=2, ensure_ascii=False)

def carregar_historico():
    if os.path.exists(HISTORICO_PATH):
        with open(HISTORICO_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def gerar_dezenas():
    return sorted(random.sample(range(1, 26), 15))

def dezenas_repetidas(historico):
    contagem = {}
    for entrada in historico:
        for dezena in entrada["aposta"]:
            contagem[dezena] = contagem.get(dezena, 0) + 1
    return sorted(contagem.items(), key=lambda x: x[1], reverse=True)

# -------------------------------
# MODELOS
# -------------------------------

class ApostaManual(BaseModel):
    dezenas: list[int]

# -------------------------------
# ENDPOINTS
# -------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_dezenas() for _ in range(3)]
    for aposta in apostas:
        salvar_aposta("gerar-apostas", aposta)
    return {"origem": "gerar-apostas", "apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_aposta_bonus():
    aposta = gerar_dezenas()
    salvar_aposta("aposta-bonus", aposta)
    return {"origem": "aposta-bonus", "aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_aposta_experimental():
    aposta = gerar_dezenas()
    salvar_aposta("aposta-experimental", aposta)
    return {"origem": "aposta-experimental", "aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_aposta_refinada():
    aposta = gerar_dezenas()
    salvar_aposta("refinar", aposta)
    return {"origem": "refinar", "aposta": aposta}

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    pares = len([d for d in aposta.dezenas if d % 2 == 0])
    primos = len([d for d in aposta.dezenas if d in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
    repetidas = len(set(aposta.dezenas)) != len(aposta.dezenas)
    score = round((15 + primos + pares) / 5.5, 2)
    return {
        "origem": "analisar-aposta",
        "dezenas": aposta.dezenas,
        "pares": pares,
        "primos": primos,
        "repetidas": "Sim" if repetidas else "Não",
        "score": score,
        "avaliacao": "Alta chance de acerto" if score >= 6 else "Aposta comum"
    }

@app.get("/historico-apostas")
def historico_apostas():
    return {"historico": carregar_historico()}

@app.get("/frequencia-dezenas")
def frequencia_dezenas():
    historico = carregar_historico()
    repetidas = dezenas_repetidas(historico)
    return {"frequencia": repetidas}
