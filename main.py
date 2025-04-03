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

# ----------------------------------------
# FUNÇÕES BASE DA IA LOTOFÁCIL
# ----------------------------------------

def gerar_aposta_padrao():
    dezenas = list(range(1, 26))
    random.shuffle(dezenas)
    return sorted(dezenas[:15])

def gerar_aposta_bonus():
    dezenas_quentes = [1, 3, 5, 8, 10, 11, 13, 14, 18, 20, 22, 23, 25]
    adicionais = random.sample([d for d in range(1, 26) if d not in dezenas_quentes], 2)
    aposta = sorted(random.sample(dezenas_quentes, 13) + adicionais)
    return aposta

def gerar_aposta_experimental():
    dezenas_frias = [2, 4, 6, 7, 9, 12, 15, 16, 17, 19, 21, 24]
    aposta = sorted(random.sample(dezenas_frias, 10) + random.sample([d for d in range(1, 26) if d not in dezenas_frias], 5))
    return aposta

def gerar_aposta_refinada():
    dezenas = list(range(1, 26))
    aposta = []
    while len(aposta) < 15:
        d = random.choice(dezenas)
        if d not in aposta and not (d % 5 == 0 and d in aposta):
            aposta.append(d)
    return sorted(aposta)

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

# ----------------------------------------
# ENDPOINTS
# ----------------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    return {"apostas": [gerar_aposta_padrao() for _ in range(3)]}

@app.get("/bonus")
def gerar_bonus():
    return {"apostas": [gerar_aposta_bonus() for _ in range(3)]}

@app.get("/experimental")
def gerar_experimental():
    return {"apostas": [gerar_aposta_experimental() for _ in range(3)]}

@app.get("/refinar")
def gerar_refinada():
    return {"apostas": [gerar_aposta_refinada() for _ in range(3)]}

class ApostaManual(BaseModel):
    aposta: list[int]

@app.post("/analisar")
def analisar(aposta: ApostaManual):
    try:
        return analisar_aposta_manual(aposta.aposta)
    except Exception as e:
        return {"erro": str(e)}
