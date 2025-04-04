from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from collections import Counter

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

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
        [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 1, 3, 5],
        [5, 10, 15, 20, 25, 1, 6, 11, 16, 21, 2, 7, 12, 17, 22]
    ]
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    return {"aposta": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    return {"aposta": [5, 10, 15, 20, 25, 4, 9, 14, 19, 24, 3, 8, 13, 18, 23]}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    return {"aposta": [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 1, 3, 5]}

@app.post("/registrar-aposta")
def registrar_aposta(aposta: ApostaRequest):
    banco_apostas.append(aposta.dict())
    return {"status": "registrado", "aposta": aposta.dict()}

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
