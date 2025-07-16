# FlowMindz Deploy

Projeto backend com FastAPI + PostgreSQL.

## 🚀 Como usar no Railway:

1. Faça fork deste repositório
2. Acesse [https://railway.app](https://railway.app)
3. Clique em "New Project" > Deploy from GitHub
4. Adicione a variável `DATABASE_URL` com o valor do PostgreSQL
5. Railway detecta `main.py` e roda com `uvicorn main:app --host 0.0.0.0 --port 10000`

## 🔐 Rota protegida

POST `/analisar_oportunidade`

```json
{
  "username": "admin",
  "password": "123456"
}
```
