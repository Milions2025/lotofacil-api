
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

historico_data = []
frequencia_data = [{"dezena": i, "frequencia": (25 - i)} for i in range(1, 26)]  # Exemplo

def gerar_dezenas():
    from random import sample
    return sorted(sample(range(1, 26), 15))

def registrar(tipo, dezenas):
    data = datetime.now(pytz.timezone("America/Sao_Paulo")).strftime("%d/%m/%Y %H:%M:%S")
    historico_data.append({"tipo": tipo, "data": data, "dezenas": dezenas})
    return {"tipo": tipo, "data": data, "dezenas": dezenas}

@app.get("/")
def raiz():
    return {"mensagem": "API da IA Lotofácil Online"}

@app.get("/gerar-apostas")
def gerar_apostas():
    apostas = [gerar_dezenas() for _ in range(3)]
    for jogo in apostas:
        registrar("Aposta Normal", jogo)
    return {"apostas": apostas}

@app.get("/gerar-aposta-bonus")
def gerar_aposta_bonus():
    dezenas = gerar_dezenas()
    registrar("Aposta Bônus", dezenas)
    return {"aposta": dezenas}

@app.get("/gerar-aposta-experimental")
def gerar_aposta_experimental():
    dezenas = gerar_dezenas()
    registrar("Aposta Experimental", dezenas)
    return {"aposta": dezenas}

@app.get("/gerar-aposta-refinada")
def gerar_aposta_refinada():
    dezenas = gerar_dezenas()
    registrar("Aposta Refinada", dezenas)
    return {"aposta": dezenas}

@app.get("/historico")
def obter_historico():
    return historico_data

@app.get("/frequencia")
def obter_frequencia():
    return frequencia_data
