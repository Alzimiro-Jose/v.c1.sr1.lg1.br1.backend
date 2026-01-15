# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\main.py

# 📌 Importação de Bibliotecas
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column, declarative_base
from pydantic import BaseModel, EmailStr, StringConstraints, model_validator
import bcrypt
import re
import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, List

# --- CONFIGURAÇÕES DE SEGURANÇA ---
SECRET_KEY = "Bento1801?"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1200

# --- CONFIGURAÇÃO DA API ---
app = FastAPI()

# ✅ AJUSTE CORS: Permitir o seu domínio da Vercel e Localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://v-w1-c1-sr1-lg1-br1.vercel.app" # Substitua pela sua URL real do frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONEXÃO SUPABASE ---
# ✅ AJUSTE: URL do Supabase (A mesma do seu database.py)
DATABASE_URL = "postgresql://postgres:k2ukutacP3O4KDPX@db.gbjpgklizrfocjecuolh.supabase.co:5432/postgres"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- MODELO DE TABELA ---
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(11), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    data_criacao: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

# --- SCHEMAS DE VALIDAÇÃO ---
class UsuarioSchema(BaseModel):
    nome: Annotated[str, StringConstraints(min_length=3, max_length=255, pattern=r'^[A-Za-z\s]+$')]
    email: EmailStr
    telefone: Annotated[str, StringConstraints(min_length=11, max_length=11, pattern=r'^[0-9]+$')]
    cpf: Annotated[str, StringConstraints(min_length=11, max_length=11, pattern=r'^[0-9]+$')]
    senha: Annotated[str, StringConstraints(min_length=8)]
    repetirSenha: str

    @model_validator(mode="after")
    def senha_confere(self) -> "UsuarioSchema":
        if self.senha != self.repetirSenha:
            raise ValueError("As senhas não conferem")
        return self

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str

# --- FUNÇÕES AUXILIARES ---
def criar_token_acesso(dados: dict):
    expira = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados.update({"exp": expira})
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

def verificar_token(token: str = Depends(jwt.decode)): # Simplificado para o exemplo
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except:
        raise HTTPException(status_code=401, detail="Token inválido")

# --- ROTAS ---
@app.post("/cadastrar")
def cadastrar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    if db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    
    hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
    novo_usuario = UsuarioDB(
        nome=usuario.nome,
        email=usuario.email,
        telefone=usuario.telefone,
        cpf=usuario.cpf,
        senha=hashed_senha.decode('utf-8')
    )
    db.add(novo_usuario)
    db.commit()
    return {"mensagem": "Cadastro realizado com sucesso"}

@app.post("/login")
def login(login: LoginSchema, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == login.email).first()
    if not usuario or not bcrypt.checkpw(login.senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    
    token = criar_token_acesso({"sub": usuario.email, "id": usuario.id, "nome": usuario.nome})
    return {"token": token}

# ✅ AJUSTE PARA VERCEL: O Uvicorn não é chamado manualmente na Vercel
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)