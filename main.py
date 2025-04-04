from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz
import random

app = FastAPI()

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Modelos Preditivos
# -------------------------------
def gerar_aposta_ia():
    dezenas = list(range(1, 26))
    apostas = []
    for _ in range(3):
        random.shuffle(dezenas)
        apostas.append(sorted(dezenas[:15]))
    return apostas

def gerar_aposta_bonus():
    dezenas = list(range(1, 26))
    random.shuffle(dezenas)
    return sorted(dezenas[:15])

def gerar_aposta_experimental():
    dezenas = list(range(1, 26))
    return sorted(random.sample(dezenas, 15))

def gerar_aposta_refinada():
    dezenas = list(range(1, 26))
    return sorted(random.sample(dezenas, 15))

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

# Histórico temporário
historico_apostas = []

# -------------------------------
# Modelos de Dados
# -------------------------------
class ApostaManual(BaseModel):
    dezenas: list[int]

# -------------------------------
# Endpoints
# -------------------------------
@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = gerar_aposta_ia()
    registrar_historico("gerar-apostas", apostas)
    return {"origem": "gerar-apostas", "apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_aposta_bonus()
    registrar_historico("aposta-bonus", [aposta])
    return {"origem": "aposta-bonus", "aposta": aposta}

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_aposta_experimental()
    registrar_historico("aposta-experimental", [aposta])
    return {"origem": "aposta-experimental", "aposta": aposta}

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_aposta_refinada()
    registrar_historico("refinar", [aposta])
    return {"origem": "refinar", "aposta": aposta}

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        analise = analisar_aposta_manual(aposta.dezenas)
        return {"origem": "analisar-aposta", "dezenas": aposta.dezenas, **analise}
    except Exception as e:
        return {"erro": str(e)}

# -------------------------------
# Registro e Visualização
# -------------------------------
def registrar_historico(origem, apostas):
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    agora = datetime.now(fuso_brasilia).strftime("%Y-%m-%d %H:%M:%S")
    for aposta in apostas:
        historico_apostas.append({
            "tipo": origem,
            "aposta": aposta,
            "horario": agora
        })

@app.get("/ver-historico")
def ver_historico():
    html = "<h2>📋 Histórico de Apostas</h2>"
    for item in historico_apostas[-50:][::-1]:
        html += f"<div><strong>Tipo:</strong> {item['tipo'].upper()} | "
        html += f"<strong>🕛 Horário:</strong> {item['horario']}<br>"
        html += f"<strong>🔢 Dezenas:</strong> {item['aposta']}</div><hr>"
    return html

@app.get("/ver-frequencia")
def ver_frequencia():
    freq = {}
    for item in historico_apostas:
        for dezena in item['aposta']:
            freq[dezena] = freq.get(dezena, 0) + 1
    freq_ordenada = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    html = "<h3>⭐ Dezenas Mais Repetidas</h3><ul>"
    for dez, qtde in freq_ordenada[:15]:
        html += f"<li>Dezena {dez:02d}: {qtde}x</li>"
    html += "</ul>"
    return html
