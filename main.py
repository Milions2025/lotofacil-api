from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Base de dados simulada
historico = []
frequencia = {i: 0 for i in range(1, 26)}

# Modelos de resposta
class ApostaResponse(BaseModel):
    aposta: list

class ApostasResponse(BaseModel):
    apostas: list

def gerar_aposta():
    aposta = sorted(random.sample(range(1, 26), 15))
    for d in aposta:
        frequencia[d] += 1
    historico.append({
        "tipo": "Aposta Normal",
        "data": datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M"),
        "dezenas": aposta
    })
    return aposta

@app.get("/gerar-apostas", response_model=ApostasResponse)
def gerar_apostas():
    apostas = [gerar_aposta() for _ in range(3)]
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus", response_model=ApostaResponse)
def gerar_aposta_bonus():
    aposta = gerar_aposta()
    historico[-1]["tipo"] = "Aposta Bônus"
    return {"aposta": aposta}

@app.get("/gerar-aposta-experimental", response_model=ApostaResponse)
def gerar_aposta_experimental():
    aposta = gerar_aposta()
    historico[-1]["tipo"] = "Aposta Experimental"
    return {"aposta": aposta}

@app.get("/gerar-aposta-refinada", response_model=ApostaResponse)
def gerar_aposta_refinada():
    aposta = gerar_aposta()
    historico[-1]["tipo"] = "Aposta Refinada"
    return {"aposta": aposta}

@app.get("/historico")
def obter_historico():
    return historico

@app.get("/frequencia")
def obter_frequencia():
    return [{"dezena": k, "frequencia": v} for k, v in frequencia.items()]
