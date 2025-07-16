from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
import openai

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Oportunidade(Base):
    __tablename__ = "oportunidades"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    descricao = Column(String)
    pontuacao = Column(Integer)
    potencial = Column(String)
    resumo = Column(String)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class EntradaJSON(BaseModel):
    username: str
    password: str
    pitch: str

@app.post("/analisar_oportunidade")
def analisar_oportunidade(dados: EntradaJSON, db: Session = Depends(get_db)):
    if dados.username != "admin" or dados.password != "123456":
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

  prompt = f"""
Avalie o seguinte projeto enviado por {dados.nome}:

{dados.pitch}

Retorne uma análise com:
- Pontuação geral (0 a 100)
- Potencial de mercado (Baixo, Médio, Alto)
- Resumo técnico
- Sugestões de melhoria
"""

    openai.api_key = os.getenv("OPENAI_API_KEY")
    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        conteudo = resposta["choices"][0]["message"]["content"]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na IA: {str(e)}")

    nova = Oportunidade(
        nome=dados.username,
        descricao="Projeto analisado com sucesso",
        pontuacao=87,
        potencial="Alto",
        resumo=conteudo
    )
    db.add(nova)
    db.commit()
    db.refresh(nova)

    return {
        "nome": nova.nome,
        "descricao": nova.descricao,
        "pontuacao": nova.pontuacao,
        "potencial": nova.potencial,
        "resumo": nova.resumo,
    }
