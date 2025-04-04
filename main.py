# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Banco de dados em memória
historico_apostas = []
frequencia_dezenas = {}

class ApostaRequest(BaseModel):
    dezenas: list[int]

# Utilitários
fuso_brasilia = pytz.timezone("America/Sao_Paulo")

def gerar_aposta(tipo: str) -> list[int]:
    aposta = sorted(random.sample(range(1, 26), 15))
    data = datetime.now(fuso_brasilia).strftime("%d/%m/%Y %H:%M:%S")
    historico_apostas.append({"tipo": tipo, "data": data, "dezenas": aposta})
    for dezena in aposta:
        frequencia_dezenas[dezena] = frequencia_dezenas.get(dezena, 0) + 1
    return aposta

@app.get("/")
def raiz():
    return {"mensagem": "API da Lotofácil Online!"}

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_aposta("Aposta Principal") for _ in range(3)]
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_aposta_bonus():
    aposta = gerar_aposta("Aposta Bônus")
    return {"aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_aposta_experimental():
    dezenas = random.sample(range(1, 26), 20)
    aposta = sorted(dezenas[:15])
    data = datetime.now(fuso_brasilia).strftime("%d/%m/%Y %H:%M:%S")
    historico_apostas.append({"tipo": "Aposta Experimental", "data": data, "dezenas": aposta})
    for dezena in aposta:
        frequencia_dezenas[dezena] = frequencia_dezenas.get(dezena, 0) + 1
    return {"aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_aposta_refinada():
    dezenas_comuns = sorted(frequencia_dezenas, key=frequencia_dezenas.get, reverse=True)[:10]
    dezenas_restantes = list(set(range(1, 26)) - set(dezenas_comuns))
    aposta = sorted(random.sample(dezenas_comuns, 10) + random.sample(dezenas_restantes, 5))
    data = datetime.now(fuso_brasilia).strftime("%d/%m/%Y %H:%M:%S")
    historico_apostas.append({"tipo": "Aposta Refinada", "data": data, "dezenas": aposta})
    for dezena in aposta:
        frequencia_dezenas[dezena] = frequencia_dezenas.get(dezena, 0) + 1
    return {"aposta": aposta}

@app.get("/historico")
def ver_historico():
    return historico_apostas

@app.get("/frequencia")
def ver_frequencia():
    return sorted(
        [{"dezena": k, "frequencia": v} for k, v in frequencia_dezenas.items()],
        key=lambda x: x["frequencia"],
        reverse=True
    )
