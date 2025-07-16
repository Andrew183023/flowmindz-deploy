from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

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

@app.post("/analisar_oportunidade")
def analisar_oportunidade(dados: EntradaJSON, db: Session = Depends(get_db)):
    if dados.username != "admin" or dados.password != "123456":
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    prompt = f"""
    Avalie o seguinte projeto:

    Nome: {dados.username}
    Descrição: Login realizado com sucesso

    Dê uma nota de 0 a 100, identifique o potencial (Baixo, Médio ou Alto) e escreva um breve resumo com base nos dados.
    """

    # Aqui ainda está mockado — IA real pode ser integrada
    nova = Oportunidade(
        nome=dados.username,
        descricao="Login realizado com sucesso",
        pontuacao=87,
        potencial="Alto",
        resumo="Oportunidade com alto potencial, recomendada para investimento."
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

