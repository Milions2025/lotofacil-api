from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import random
from datetime import datetime

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
# MODELOS E MEMÓRIA TEMPORÁRIA
# -------------------------------
historico_apostas = []

def registrar_aposta(origem, aposta):
    historico_apostas.append({
        "origem": origem,
        "dezenas": aposta,
        "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    })

def gerar_aposta_ia():
    dezenas_disponiveis = list(range(1, 26))
    apostas = []
    for _ in range(3):
        random.shuffle(dezenas_disponiveis)
        aposta = sorted(dezenas_disponiveis[:15])
        apostas.append(aposta)
        registrar_aposta("gerar-apostas", aposta)
    return apostas

def gerar_aposta_bonus():
    dezenas_disponiveis = list(range(1, 26))
    random.shuffle(dezenas_disponiveis)
    aposta = sorted(dezenas_disponiveis[:15])
    registrar_aposta("aposta-bonus", aposta)
    return aposta

def gerar_aposta_experimental():
    dezenas_disponiveis = list(range(1, 26))
    aposta = sorted(random.sample(dezenas_disponiveis, 15))
    registrar_aposta("aposta-experimental", aposta)
    return aposta

def gerar_aposta_refinada():
    dezenas_disponiveis = list(range(1, 26))
    aposta = sorted(random.sample(dezenas_disponiveis, 15))
    registrar_aposta("refinar", aposta)
    return aposta

def analisar_aposta_manual(dezenas):
    pares = len([d for d in dezenas if d % 2 == 0])
    primos = len([d for d in dezenas if d in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
    repetidas = len(set(dezenas)) != len(dezenas)
    score = round((15 + primos + pares) / 5.5, 2)
    return {
        "pares": pares,
        "primos": primos,
        "repetidas": "Sim" if repetidas else "Não",
        "score": score,
        "avaliacao": "Alta chance de acerto" if score >= 6 else "Aposta comum"
    }

# -------------------------------
# MODELO PARA APOSTA MANUAL
# -------------------------------

class ApostaManual(BaseModel):
    dezenas: list[int]

# -------------------------------
# ENDPOINTS
# -------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = gerar_aposta_ia()
    return {"origem": "gerar-apostas", "apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_aposta_bonus()
    return {"origem": "aposta-bonus", "aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_aposta_experimental()
    return {"origem": "aposta-experimental", "aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_aposta_refinada()
    return {"origem": "refinar", "aposta": aposta}

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        analise = analisar_aposta_manual(aposta.dezenas)
        return {
            "origem": "analisar-aposta",
            "dezenas": aposta.dezenas,
            **analise
        }
    except Exception as e:
        return {"erro": str(e)}

@app.get("/historico-apostas")
def listar_historico():
    return {"historico": historico_apostas[::-1]}  # ordem decrescente
