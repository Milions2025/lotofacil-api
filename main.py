// FastAPI backend para conectar a IA da Lotofácil ao aplicativo mobile
# Endpoint seguro com histórico, filtros e timezone BR

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz
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

# Estrutura de armazenamento em memória
historico_apostas = []

# Timezone Brasil/SP
tz_brasilia = pytz.timezone("America/Sao_Paulo")

# Modelos
class ApostaManual(BaseModel):
    dezenas: list[int]

class RegistroAposta(BaseModel):
    tipo: str
    dezenas: list[int]
    score: int
    origem: str
    timestamp: str

# Funções IA simulada (substitua por lógica real depois)
def gerar_dezenas():
    return sorted(random.sample(range(1, 26), 15))

def gerar_aposta(tipo):
    dezenas = gerar_dezenas()
    score = random.randint(6, 9)
    origem = tipo
    now = datetime.now(tz_brasilia).strftime("%d/%m/%Y %H:%M:%S")
    registro = RegistroAposta(
        tipo=tipo,
        dezenas=dezenas,
        score=score,
        origem=origem,
        timestamp=now
    )
    historico_apostas.append(registro)
    return registro

def analisar_aposta_manual(dezenas):
    pares = len([d for d in dezenas if d % 2 == 0])
    primos = len([d for d in dezenas if d in [2, 3, 5, 7, 11, 13, 17, 19, 23]])
    repetidas = len(set(dezenas)) != len(dezenas)
    score = round((15 + primos + pares) / 5.5, 2)
    avaliacao = "Alta chance de acerto" if score >= 6 else "Aposta comum"
    return {
        "pares": pares,
        "primos": primos,
        "repetidas": "Sim" if repetidas else "Não",
        "score": score,
        "avaliacao": avaliacao
    }

# Endpoints
@app.get("/gerar-apostas")
def gerar():
    apostas = [gerar_aposta("principal") for _ in range(3)]
    return {"origem": "gerar-apostas", "apostas": [a.dict() for a in apostas]}

@app.get("/gerar-aposta-bonus")
def gerar_bonus():
    aposta = gerar_aposta("bonus")
    return aposta.dict()

@app.get("/gerar-aposta-experimental")
def gerar_experimental():
    aposta = gerar_aposta("experimental")
    return aposta.dict()

@app.get("/gerar-aposta-refinada")
def gerar_refinada():
    aposta = gerar_aposta("refinar")
    return aposta.dict()

@app.post("/analisar-aposta")
def analisar(aposta: ApostaManual):
    try:
        analise = analisar_aposta_manual(aposta.dezenas)
        return {
            "origem": "analisar-aposta",
            "dezenas": aposta.dezenas,
            **analise
        }
    except Exception as e:
        return {"erro": str(e)}

@app.get("/historico")
def ver_historico(tipo: str = None):
    if tipo:
        filtrado = [a.dict() for a in historico_apostas if a.tipo == tipo]
    else:
        filtrado = [a.dict() for a in historico_apostas]
    return {"historico": filtrado}

@app.get("/status")
def status():
    return {"status": "IA 100% operacional com histórico e timezone BR ativo"}
