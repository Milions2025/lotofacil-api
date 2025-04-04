
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import pytz

app = FastAPI()

# Configuração de CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Memória temporária para simulação
historico_apostas = []
frequencia_dezenas = {}

# Modelos de dados
class ApostaInput(BaseModel):
    origem: str
    dezenas: list[int]

class ResultadoInput(BaseModel):
    dezenas: list[int]

# Função para horário de Brasília
def horario_brasilia():
    fuso_brasilia = pytz.timezone("America/Sao_Paulo")
    return datetime.now(fuso_brasilia).strftime("%Y-%m-%d %H:%M:%S")

# Registrar aposta
@app.post("/gerar-apostas")
def gerar_aposta(aposta: ApostaInput):
    registro = {
        "tipo": "gerar-apostas",
        "origem": aposta.origem,
        "dezenas": aposta.dezenas,
        "data": horario_brasilia(),
    }
    historico_apostas.append(registro)
    return {"status": "ok", "aposta": registro}

# Refinar aposta
@app.post("/refinar-apostas")
def refinar_aposta(aposta: ApostaInput):
    registro = {
        "tipo": "refinar-apostas",
        "origem": aposta.origem,
        "dezenas": aposta.dezenas,
        "data": horario_brasilia(),
    }
    historico_apostas.append(registro)
    return {"status": "ok", "aposta": registro}

# Consultar status
@app.get("/status")
def consultar_status():
    return {"status": "ativo", "quantidade_apostas": len(historico_apostas)}

# Enviar resultado real
@app.post("/resultado")
def enviar_resultado(resultado: ResultadoInput):
    for dezena in resultado.dezenas:
        frequencia_dezenas[dezena] = frequencia_dezenas.get(dezena, 0) + 1
    return {"status": "resultado registrado"}

# Histórico
@app.get("/historico")
def obter_historico():
    return historico_apostas

# Frequência
@app.get("/frequencia")
def obter_frequencia():
    return dict(sorted(frequencia_dezenas.items(), key=lambda item: item[1], reverse=True))
