from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import openai
import os

DATABASE_URL = os.getenv("DATABASE_URL")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Avaliacao(Base):
    __tablename__ = "avaliacoes_ia"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(Text)
    segmento = Column(String)
    localizacao = Column(String)
    pontuacao = Column(Integer)
    potencial = Column(String)
    resumo = Column(Text)
    criado_em = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

app = FastAPI()

class AvaliacaoEntrada(BaseModel):
    nome: str
    descricao: str
    segmento: str
    localizacao: str

@app.post("/flowmindz/avaliar")
def avaliar_ia(entrada: AvaliacaoEntrada):
    openai.api_key = OPENAI_API_KEY

    prompt = f"""
    Avalie o seguinte projeto:
Nome: {entrada.nome}
Descrição: {entrada.descricao}
Segmento: {entrada.segmento}
Localização: {entrada.localizacao}
Forneça uma pontuação de 0 a 100, um nível de potencial (Baixo, Médio ou Alto) e um breve resumo do porquê."

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        conteudo = resposta['choices'][0]['message']['content']

        linhas = conteudo.split("\n")
        pontuacao = int([l for l in linhas if "pontuação" in l.lower()][0].split(":")[-1].strip())
        potencial = [l for l in linhas if "potencial" in l.lower()][0].split(":")[-1].strip()
        resumo = [l for l in linhas if "resumo" in l.lower()][0].split(":")[-1].strip()

        db = SessionLocal()
        nova = Avaliacao(
            nome=entrada.nome,
            descricao=entrada.descricao,
            segmento=entrada.segmento,
            localizacao=entrada.localizacao,
            pontuacao=pontuacao,
            potencial=potencial,
            resumo=resumo
        )
        db.add(nova)
        db.commit()
        db.refresh(nova)

        return {
            "nome": nova.nome,
            "pontuacao": nova.pontuacao,
            "potencial": nova.potencial,
            "resumo": nova.resumo
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
