
from fastapi import FastAPI, Request
from pydantic import BaseModel
import openai
import os

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

class Projeto(BaseModel):
    nome: str
    pitch: str

@app.post("/avaliar")
async def avaliar_projeto(dados: Projeto):
    prompt = f'''
    Avalie o seguinte projeto enviado por {dados.nome}:

    {dados.pitch}

    Retorne uma análise com:
    - Pontuação geral (0 a 100)
    - Potencial de mercado (Baixo, Médio, Alto)
    - Resumo técnico
    - Sugestões de melhoria
    '''

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return {"analise": response.choices[0].message['content']}
