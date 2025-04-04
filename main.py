from fastapi import FastAPI
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

# Simulação de pesos baseados em frequência de sorteios (exemplo fictício)
pesos_dezenas = {
    i: random.randint(1, 100) for i in range(1, 26)
}

def gerar_aposta_coerente():
    return sorted(random.choices(
        population=list(pesos_dezenas.keys()),
        weights=list(pesos_dezenas.values()),
        k=15
    ))

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_aposta_coerente() for _ in range(3)]
    for ap in apostas:
        banco_apostas.append({
            "dezenas": ap,
            "tipo": "gerar-apostas",
            "data": datetime.now().strftime("%Y-%m-%d")
        })
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_aposta_coerente()
    banco_apostas.append({
        "dezenas": aposta,
        "tipo": "aposta-bonus",
        "data": datetime.now().strftime("%Y-%m-%d")
    })
    return {"aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_aposta_coerente()
    banco_apostas.append({
        "dezenas": aposta,
        "tipo": "aposta-experimental",
        "data": datetime.now().strftime("%Y-%m-%d")
    })
    return {"aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_aposta_coerente()
    banco_apostas.append({
        "dezenas": aposta,
        "tipo": "aposta-refinada",
        "data": datetime.now().strftime("%Y-%m-%d")
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
    registros = [r for r in banco_apostas if r["tipo"] == "resultado-real"]
    todas = [dezena for reg in registros for dezena in reg["dezenas"]]
    contagem = Counter(todas)
    resultado = [
        {"dezena": i, "frequencia": contagem.get(i, 0)} for i in range(1, 26)
    ]
    return resultado
