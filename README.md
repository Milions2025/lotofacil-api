# IA da Lotofácil – API Oficial 🤖🎯

Este projeto é a API oficial da IA da Lotofácil, capaz de gerar apostas com base em inteligência estatística, cadeia de Markov, análise de frequência, padrões ocultos e refinamento pós-sorteio.

## 🚀 Funcionalidades

- Geração de apostas principais com alto score
- Aposta bônus baseada em frequência extrema
- Aposta experimental com dezenas frias e conexões ocultas
- Apostas refinadas com base no último sorteio
- Status de operação da IA

## 📦 Requisitos

- Python 3.9+
- FastAPI
- Uvicorn

Instale com:

```bash
pip install -r requirements.txt
```

## ▶️ Execução Local

```bash
uvicorn main:app --reload
```

Acesse em: `http://localhost:8000/docs` para a documentação interativa.

## 🌐 Endpoints Principais

| Rota         | Descrição                                      |
|--------------|-----------------------------------------------|
| `/gerar`     | Gera 3 apostas principais com score e análise |
| `/bonus`     | Gera a Aposta Bônus Fidedigna                 |
| `/experimental` | Gera uma aposta com dezenas frias ocultas |
| `/refinar`   | Gera apostas refinadas com base no último sorteio |
| `/status`    | Verifica status da IA da Lotofácil            |

## 🔐 Token de Segurança

Todos os endpoints exigem o header:
```
x-token: mestre-secreto
```

## ☁️ Deploy no Railway

1. Suba os arquivos no GitHub
2. Crie um projeto no [Railway](https://railway.app)
3. Clique em “Deploy from GitHub repo”
4. O deploy será automático 🎉

---

Desenvolvido com foco em máxima precisão para geração inteligente de apostas.  
