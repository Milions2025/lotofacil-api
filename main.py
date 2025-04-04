from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz
import random
import json
import os

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Caminho para salvar o histórico
HISTORICO_PATH = "historico_apostas.json"

# Inicializa arquivo de histórico se não existir
if not os.path.exists(HISTORICO_PATH):
    with open(HISTORICO_PATH, "w") as f:
        json.dump([], f)

# Modelo para Análise Manual
class ApostaManual(BaseModel):
    dezenas: list[int]

# Utilitário para obter hora atual em SP
def hora_brasil():
    fuso = pytz.timezone("America/Sao_Paulo")
    return datetime.now(fuso).strftime("%Y-%m-%d %H:%M:%S")

# Salva aposta no histórico
def salvar_aposta(tipo, dezenas):
    with open(HISTORICO_PATH, "r") as f:
        historico = json.load(f)
    historico.append({
        "tipo": tipo,
        "dezenas": dezenas,
        "horario": hora_brasil()
    })
    with open(HISTORICO_PATH, "w") as f:
        json.dump(historico, f)

# Lógicas de Geração

def gerar_dezenas():
    return sorted(random.sample(range(1, 26), 15))

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_dezenas() for _ in range(3)]
    for aposta in apostas:
        salvar_aposta("gerar", aposta)
    return {"origem": "gerar-apostas", "apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_dezenas()
    salvar_aposta("bonus", aposta)
    return {"origem": "aposta-bonus", "aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_dezenas()
    salvar_aposta("experimental", aposta)
    return {"origem": "aposta-experimental", "aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_dezenas()
    salvar_aposta("refinar", aposta)
    return {"origem": "refinar", "aposta": aposta}

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        dezenas = aposta.dezenas
        pares = len([d for d in dezenas if d % 2 == 0])
        primos = len([d for d in dezenas if d in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
        repetidas = len(set(dezenas)) != len(dezenas)
        score = round((15 + primos + pares) / 5.5, 2)
        analise = {
            "pares": pares,
            "primos": primos,
            "repetidas": "Sim" if repetidas else "Não",
            "score": score,
            "avaliacao": "Alta chance de acerto" if score >= 6 else "Aposta comum"
        }
        salvar_aposta("manual", dezenas)
        return {"origem": "analisar-aposta", "dezenas": dezenas, **analise}
    except Exception as e:
        return {"erro": str(e)}

@app.get("/historico")
def ver_historico():
    with open(HISTORICO_PATH, "r") as f:
        historico = json.load(f)
    return historico

@app.get("/estatisticas")
def estatisticas():
    with open(HISTORICO_PATH, "r") as f:
        historico = json.load(f)
    todas_dezenas = []
    for item in historico:
        todas_dezenas.extend(item["dezenas"])
    contagem = {str(i): todas_dezenas.count(i) for i in range(1, 26)}
    mais_frequentes = sorted(contagem.items(), key=lambda x: x[1], reverse=True)[:5]
    return {"mais_frequentes": mais_frequentes}
