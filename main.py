from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import random
from datetime import datetime
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de dados temporário em memória
historico_apostas = []

# Utilidade para fuso horário de Brasília
def horario_brasilia():
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(fuso_brasilia)
    return agora.strftime("%d/%m/%Y %H:%M:%S")

# Funções de geração

def gerar_aposta(tipo: str):
    dezenas_disponiveis = list(range(1, 26))
    random.shuffle(dezenas_disponiveis)
    aposta = sorted(dezenas_disponiveis[:15])
    historico_apostas.append({
        "origem": tipo,
        "dezenas": aposta,
        "data": horario_brasilia()
    })
    return aposta

def gerar_apostas_ia():
    apostas = []
    for _ in range(3):
        aposta = gerar_aposta("gerar-apostas")
        apostas.append(aposta)
    return apostas

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

# Modelo para POST
class ApostaManual(BaseModel):
    dezenas: List[int]

# Endpoints principais
@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = gerar_apostas_ia()
    return {"origem": "gerar-apostas", "apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_aposta("aposta-bonus")
    return {"origem": "aposta-bonus", "aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_aposta("aposta-experimental")
    return {"origem": "aposta-experimental", "aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_aposta("refinar")
    return {"origem": "refinar", "aposta": aposta}

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        analise = analisar_aposta_manual(aposta.dezenas)
        return {
            "origem": "analisar-aposta",
            "dezenas": aposta.dezenas,
            **analise
        }
    except Exception as e:
        return {"erro": str(e)}

@app.get("/historico")
def ver_historico():
    return {"total": len(historico_apostas), "dados": historico_apostas}
