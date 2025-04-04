from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from collections import Counter
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ApostaRequest(BaseModel):
    dezenas: list[int]
    tipo: str
    data: str

# Banco de dados temporário
banco_apostas = []

# Função simulada baseada em estrutura da IA
# Simula pesos, diversidade e filtros básicos coerentes com a IA real
def gerar_aposta_estrategica():
    dezenas_com_peso = [
        (1, 9), (2, 8), (3, 8), (4, 7), (5, 7),
        (6, 6), (7, 6), (8, 5), (9, 5), (10, 5),
        (11, 4), (12, 4), (13, 4), (14, 3), (15, 3),
        (16, 2), (17, 2), (18, 2), (19, 2), (20, 2),
        (21, 1), (22, 1), (23, 1), (24, 1), (25, 1)
    ]
    dezenas_com_peso.sort(key=lambda x: -x[1])  # ordena por peso
    pool = [d for d, p in dezenas_com_peso for _ in range(p)]
    aposta = sorted(random.sample(set(pool), 15))
    return aposta

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_aposta_estrategica() for _ in range(3)]
    data_atual = datetime.now().strftime("%Y-%m-%d")
    for a in apostas:
        banco_apostas.append({
            "dezenas": a,
            "tipo": "gerada",
            "data": data_atual
        })
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_aposta_estrategica()
    data_atual = datetime.now().strftime("%Y-%m-%d")
    banco_apostas.append({
        "dezenas": aposta,
        "tipo": "bonus",
        "data": data_atual
    })
    return {"aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_aposta_estrategica()
    data_atual = datetime.now().strftime("%Y-%m-%d")
    banco_apostas.append({
        "dezenas": aposta,
        "tipo": "experimental",
        "data": data_atual
    })
    return {"aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_aposta_estrategica()
    data_atual = datetime.now().strftime("%Y-%m-%d")
    banco_apostas.append({
        "dezenas": aposta,
        "tipo": "refinada",
        "data": data_atual
    })
    return {"aposta": aposta}

@app.post("/registrar-aposta")
def registrar_aposta(aposta: ApostaRequest):
    banco_apostas.append(aposta.dict())
    return {"status": "registrado"}

@app.get("/historico")
def listar_historico():
    return banco_apostas

@app.get("/frequencia")
def calcular_frequencia():
    # Considera apenas apostas registradas do tipo resultado-real
    registros = [r for r in banco_apostas if r["tipo"] == "resultado-real"]
    todas = [dezena for reg in registros for dezena in reg["dezenas"]]
    contagem = Counter(todas)
    resultado = [
        {"dezena": i, "frequencia": contagem.get(i, 0)} for i in range(1, 26)
    ]
    return resultado
