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

def gerar_aposta_ia():
    return sorted(random.sample(range(1, 25), 15))

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_aposta_ia() for _ in range(3)]
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    return {"aposta": gerar_aposta_ia()}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    return {"aposta": gerar_aposta_ia()}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    return {"aposta": gerar_aposta_ia()}

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
        {"dezena": i, "frequencia": contagem.get(i, 0)} for i in range(1, 25)
    ]
    return resultado
