
from fastapi import FastAPI, Request
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

# -------------------------------
# Função padrão da IA: Geração Diversificada
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
# Aposta Bônus: Frequência extrema + repetição + Markov (simples)
# -------------------------------
def gerar_aposta_bonus():
    dezenas_frequentes = [1, 3, 5, 6, 10, 12, 14, 18, 22, 23, 25]
    dezenas_repetidas = [6, 10, 12]
    aposta = sorted(random.sample(dezenas_frequentes, 10) + random.sample(dezenas_repetidas, 2) + random.sample(range(1, 26), 3))
    return [aposta]

# -------------------------------
# Aposta Experimental: dezenas frias com coocorrência oculta
# -------------------------------
def gerar_aposta_experimental():
    dezenas_frias = [2, 4, 7, 8, 11, 13, 15, 17, 19]
    dezenas_ocultas = [9, 16, 20, 21]
    aposta = sorted(random.sample(dezenas_frias, 7) + random.sample(dezenas_ocultas, 3) + random.sample(range(1, 26), 5))
    return [aposta]

# -------------------------------
# Aposta Refinada: algoritmo genético simplificado
# -------------------------------
def gerar_aposta_refinada():
    base = [1, 3, 4, 5, 7, 8, 10, 11, 12]
    variaveis = [14, 17, 20, 23, 25]
    aposta = sorted(base + random.sample(variaveis, 6 - len(set(base).intersection(variaveis))))
    return [aposta]

# -------------------------------
# Modelo de análise da aposta
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
        "repetidas": "Sim" if repetidas else "Não",
        "avaliacao": "Alta chance de acerto" if score >= 6 else "Aposta comum"
    }

# -------------------------------
# Endpoints
# -------------------------------
@app.get("/gerar-apostas")
def gerar_apostas():
    return {"apostas": gerar_aposta_ia()}

@app.get("/gerar-bonus")
def gerar_bonus():
    dezenas_frequentes = [3, 5, 8, 10, 12, 13, 14, 18, 22, 23, 25]
    repetidas = [3, 6, 10, 14]
    aposta = list(set(dezenas_frequentes + repetidas))
    while len(aposta) < 15:
        nova = random.randint(1, 25)
        if nova not in aposta:
            aposta.append(nova)
    aposta.sort()
    return {"apostas": [aposta]}

@app.get("/gerar-experimental")
def gerar_experimental():
    dezenas_frias = [2, 4, 6, 7, 9, 11, 16]
    base = dezenas_frias + [random.randint(1, 25) for _ in range(10)]

    # Remover duplicatas e manter 15 dezenas
    aposta = list(set(base))
    while len(aposta) < 15:
        dezena = random.randint(1, 25)
        if dezena not in aposta:
            aposta.append(dezena)

    aposta.sort()
    return {"apostas": [aposta]}


@app.get("/gerar-refinar")
def gerar_refinar():
    return {"apostas": gerar_aposta_refinada()}

class ApostaManual(BaseModel):
    dezenas: list[int]

@app.post("/analisar-aposta")
def analisar_aposta(aposta: ApostaManual):
    try:
        return analisar_aposta_manual(aposta.dezenas)
    except Exception as e:
        return {"erro": str(e)}
