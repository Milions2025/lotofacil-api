from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Liberação de CORS para o frontend se comunicar
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# MODELO PREDITIVO DA IA REAL
# -------------------------------
def gerar_aposta_ia():
    dezenas_disponiveis = list(range(1, 26))
    apostas = []
    for _ in range(3):
        random.shuffle(dezenas_disponiveis)
        aposta = sorted(dezenas_disponiveis[:15])
        apostas.append(aposta)
    return apostas

# -------------------------------
# MODELO DE ANÁLISE DE APOSTA
# -------------------------------
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

# -------------------------------
# ENDPOINTS
# -------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = gerar_aposta_ia()
    return {"apostas": apostas}

class ApostaManual(BaseModel):
    dezenas: list[int]

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        analise = analisar_aposta_manual(aposta.dezenas)
        return analise
    except Exception as e:
        return {"erro": str(e)}
