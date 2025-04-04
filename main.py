from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
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

# Simulação do armazenamento interno
historico_apostas = []

class ApostaRequest(BaseModel):
    dezenas: List[int]
    tipo: str

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = []
    for _ in range(3):
        dezenas = sorted(random.sample(range(1, 26), 15))
        apostas.append(dezenas)
        salvar_aposta(dezenas, "Aposta Principal")
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_aposta_bonus():
    dezenas = sorted(random.sample(range(1, 26), 15))
    salvar_aposta(dezenas, "Aposta Bônus")
    return {"aposta": dezenas}

@app.get("/gerar-aposta-experimental")
def gerar_aposta_experimental():
    dezenas = sorted(random.sample(range(1, 26), 15))
    salvar_aposta(dezenas, "Aposta Experimental")
    return {"aposta": dezenas}

@app.get("/gerar-aposta-refinada")
def gerar_aposta_refinada():
    dezenas = sorted(random.sample(range(1, 26), 15))
    salvar_aposta(dezenas, "Aposta Refinada")
    return {"aposta": dezenas}

@app.get("/historico")
def ver_historico():
    return historico_apostas

@app.get("/frequencia")
def ver_frequencia():
    contagem = {}
    for item in historico_apostas:
        for dezena in item['dezenas']:
            contagem[dezena] = contagem.get(dezena, 0) + 1
    resultado = [{"dezena": k, "frequencia": v} for k, v in sorted(contagem.items())]
    return resultado

def salvar_aposta(dezenas: List[int], tipo: str):
    agora = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M")
    historico_apostas.append({
        "dezenas": dezenas,
        "tipo": tipo,
        "data": agora
    })
