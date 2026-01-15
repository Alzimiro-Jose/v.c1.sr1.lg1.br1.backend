# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\main.py

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, func
from sqlalchemy.orm import sessionmaker, Session, Mapped, mapped_column, declarative_base
from pydantic import BaseModel, EmailStr, StringConstraints, model_validator
import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated
from sqlalchemy.pool import NullPool # Importação necessária

# --- CONFIGURAÇÕES DE SEGURANÇA ---
SECRET_KEY = "Bento1801?"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1200

# --- CONFIGURAÇÃO DA API ---
app = FastAPI()

# ✅ CORS: Mantido aberto para validar a comunicação inicial
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- CONFIGURAÇÃO DO BANCO DE DADOS ---


# 🔹 FORMATO RADICAL: Trocamos o nome do host pelo IP do Pooler do Supabase no Brasil
# 🔹 Isso força a Vercel a usar IPv4 e ignora o erro de "address"
DATABASE_URL = "postgresql://postgres:4u5TNz6jnQCLMks0@15.229.150.166:6543/postgres?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool, # Garante que cada requisição seja uma conexão nova e limpa
    connect_args={
        "connect_timeout": 15
    }
)


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


@app.get("/teste-simples")
def teste():
    return {"status": "A API está funcionando e o CORS permite isso!"}




@app.get("/debug-db")
def debug_db():
    try:
        from sqlalchemy import text
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            return {"status": "Sucesso!", "detalhe": "O Backend conseguiu falar com o Supabase!"}
    except Exception as e:
        return {"status": "Erro de Conexão", "mensagem_real": str(e)}