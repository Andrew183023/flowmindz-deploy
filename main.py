from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI()

class Oportunidade(BaseModel):
    nome: str
    descricao: str

@app.post("/flowmindz/avaliar")
def avaliar_oportunidade(dados: Oportunidade):
    # Aqui entra lógica real de IA — simulação abaixo
    if "verde" in dados.descricao.lower():
        score = 95
        resumo = "Alto potencial ESG e inovação sustentável."
    elif "logística" in dados.descricao.lower():
        score = 92
        resumo = "Alta aplicabilidade no ecossistema PortFlow."
    else:
        score = 76
        resumo = "Oportunidade promissora, mas com riscos moderados."

    return {
        "nome": dados.nome,
        "pontuacao": score,
        "resumo": resumo
    }