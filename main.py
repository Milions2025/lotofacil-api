# FastAPI backend para conectar a IA da Lotofácil ao aplicativo mobile

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz
import random

app = FastAPI()

# CORS para permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Histórico das apostas
historico_apostas = []

# -------------------------------
# Funções de geração
# -------------------------------

def gerar_aposta(tipo="gerar-apostas"):
    dezenas_disponiveis = list(range(1, 26))
    aposta = sorted(random.sample(dezenas_disponiveis, 15))
    horario = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%Y-%m-%d %H:%M:%S")
    historico_apostas.append({
        "tipo": tipo,
        "dezenas": aposta,
        "horario": horario
    })
    return aposta

# -------------------------------
# Função de análise manual
# -------------------------------

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
# Modelo da aposta manual
# -------------------------------

class ApostaManual(BaseModel):
    dezenas: list[int]

# -------------------------------
# Rotas
# -------------------------------

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_aposta("gerar-apostas") for _ in range(3)]
    return {"origem": "gerar-apostas", "apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_aposta_bonus():
    return {"origem": "aposta-bonus", "aposta": gerar_aposta("aposta-bonus")}

@app.get("/gerar-aposta-experimental")
def gerar_aposta_experimental():
    return {"origem": "aposta-experimental", "aposta": gerar_aposta("aposta-experimental")}

@app.get("/gerar-aposta-refinada")
def gerar_aposta_refinada():
    return {"origem": "refinar", "aposta": gerar_aposta("refinar")}

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

@app.get("/ver-historico")
def ver_historico():
    return {"historico": list(reversed(historico_apostas))}
