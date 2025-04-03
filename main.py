from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Liberação de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# MODELO PRINCIPAL DE GERAÇÃO
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
# Variações da IA
# -------------------------------

def gerar_aposta_bonus():
    return {"apostas": gerar_aposta_ia()}

def gerar_aposta_experimental():
    return {"apostas": gerar_aposta_ia()}

def gerar_aposta_refinada():
    return {"apostas": gerar_aposta_ia()}

# -------------------------------
# Análise da Aposta
# -------------------------------

def analisar_aposta_manual(dezenas):
    pares = len([d for d in dezenas if d % 2 == 0])
    primos = len([d for d in dezenas if d in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
    repetidas = len(set(dezenas)) != len(dezenas)
    score = round((15 + primos + pares) / 5.5, 2)
    return {
        "dezenas": dezenas,
        "pares": pares,
        "primos": primos,
        "repetidas": repetidas,
        "avaliacao": "Alta chance de acerto" if score >= 6 else "Aposta comum"
    }

# -------------------------------
# ROTAS / ENDPOINTS
# -------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    return {"apostas": gerar_aposta_ia()}

@app.get("/bonus")
def gerar_bonus():
    return gerar_aposta_bonus()

@app.get("/experimental")
def gerar_experimental():
    return gerar_aposta_experimental()

@app.get("/refinar")
def gerar_refinada():
    return gerar_aposta_refinada()

class ApostaManual(BaseModel):
    aposta: list[int]  # ⚠️ Nome do campo agora igual ao que o frontend envia

@app.post("/analisar")
def analisar(aposta: ApostaManual):
    try:
        return analisar_aposta_manual(aposta.aposta)
    except Exception as e:
        return {"erro": str(e)}
