from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def gerar_aposta_ia():
    dezenas_disponiveis = list(range(1, 26))
    apostas = []
    for _ in range(3):
        random.shuffle(dezenas_disponiveis)
        aposta = sorted(dezenas_disponiveis[:15])
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
        "repetidas": repetidas,
        "score": score,
        "aviso": "Alta chance de acerto" if score >= 6 else "Aposta comum"
    }

@app.get("/gerar-apostas")
def gerar_apostas():
    return {"apostas": gerar_aposta_ia()}

@app.get("/gerar-bonus")
def gerar_bonus():
    return {"apostas": gerar_aposta_ia()}

@app.get("/gerar-experimental")
def gerar_experimental():
    return {"apostas": gerar_aposta_ia()}

@app.get("/gerar-refinar")
def gerar_refinar():
    return {"apostas": gerar_aposta_ia()}

class ApostaManual(BaseModel):
    dezenas: list[int]

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        return analisar_aposta_manual(aposta.dezenas)
    except Exception as e:
        return {"erro": str(e)}
