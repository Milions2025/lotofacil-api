
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random

app = FastAPI()

# Liberação de CORS para comunicação com frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Funções da IA da Lotofácil
# -------------------------------

def gerar_apostas_gerais():
    dezenas = list(range(1, 26))
    apostas = []
    for _ in range(3):
        random.shuffle(dezenas)
        aposta = sorted(dezenas[:15])
        apostas.append(aposta)
    return apostas

def gerar_aposta_bonus():
    dezenas = list(range(1, 26))
    random.shuffle(dezenas)
    aposta = sorted(dezenas[:15])
    return [aposta]

def gerar_aposta_experimental():
    dezenas = list(range(1, 26))
    random.shuffle(dezenas)
    aposta = sorted(dezenas[:15])
    return [aposta]

def gerar_aposta_refinada():
    dezenas = list(range(1, 26))
    random.shuffle(dezenas)
    aposta = sorted(dezenas[:15])
    return [aposta]

def analisar_aposta_manual(dezenas):
    pares = len([d for d in dezenas if d % 2 == 0])
    primos = len([d for d in dezenas if d in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
    repetidas = len(set(dezenas)) != len(dezenas)
    score = round((15 + primos + pares) / 5.5, 2)
    aviso = "Alta chance de acerto" if score >= 6 else "Aposta comum"

    return {
        "origem": "Análise Manual",
        "dezenas": dezenas,
        "pares": pares,
        "primos": primos,
        "repetidas": "Sim" if repetidas else "Não",
        "score": score,
        "aviso": aviso
    }

# -------------------------------
# Endpoints da API
# -------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = gerar_apostas_gerais()
    return {"origem": "Gerar Apostas", "apostas": apostas}

@app.get("/aposta-bonus")
def aposta_bonus():
    apostas = gerar_aposta_bonus()
    return {"origem": "Aposta Bônus", "apostas": apostas}

@app.get("/experimental")
def experimental():
    apostas = gerar_aposta_experimental()
    return {"origem": "Aposta Experimental", "apostas": apostas}

@app.get("/refinar-apostas")
def refinar_apostas():
    apostas = gerar_aposta_refinada()
    return {"origem": "Refinar Apostas", "apostas": apostas}

class ApostaManual(BaseModel):
    dezenas: list[int]

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        return analisar_aposta_manual(aposta.dezenas)
    except Exception as e:
        return {"erro": str(e), "origem": "Erro na Análise Manual"}
