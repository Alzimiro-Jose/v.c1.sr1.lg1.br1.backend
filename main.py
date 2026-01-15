# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\main.py
#==================================================================================================
# Importações Necessárias atualizadas - 28.03.25 - Trecho 1 - Início
#==================================================================================================

# 📌 Importação de Bibliotecas Necessárias
from sqlalchemy import text  
from pydantic import Field, conint
from fastapi import FastAPI, HTTPException, Depends, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import Date, create_engine, Column, Integer, String, TIMESTAMP, func, insert
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel, EmailStr, constr
import bcrypt
import re
import jwt  # Biblioteca para gerar tokens JWT
from datetime import date, datetime, timedelta  # Para definir expiração do token
from datetime import timezone
from typing import Optional, List
import json
import sys
from starlette.routing import Router
from datetime import timedelta
from tabulate import tabulate
from sqlalchemy import Date, create_engine, Column, Integer, String, TIMESTAMP, func
from datetime import time

#==================================================================================================
#Importações atualizadas - 28.03.25 - Trecho 1 - Fim
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
# Configurações de Segurança - atualizadas - 28.03.25 - Trecho 2 - Início
#==================================================================================================

SECRET_KEY = "Bento1801?"  # Troque por uma chave forte
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1200  # Tempo de expiração do token



# 📌 Configuração da API
app = FastAPI()

# 📌 Função para criar token de acesso
def criar_token_acesso(dados: dict, expira_em: int = ACCESS_TOKEN_EXPIRE_MINUTES):
    dados_copia = dados.copy()
    expira = datetime.now(timezone.utc) + timedelta(minutes=expira_em)
    dados_copia.update({"exp": expira})
    token_jwt = jwt.encode(dados_copia, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

# 📌 Esquema de autenticação com OAuth2
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def verificar_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"erro": "token_expirado", "redirect": "/login"}
    except jwt.InvalidTokenError:
        return {"erro": "token_invalido", "redirect": "/login"}





# Permitir requisições do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


#==================================================================================================
# Configurações de Segurança - atualizadas - 28.03.25 - Trecho 2 - Fim
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
# Conexão/Reconexão automática Supabase - atualizadas - 28.03.25 - Trecho 3 - Início
#==================================================================================================


# 📌 Conexão com o Banco de Dados MySQL
DATABASE_URL = "mysql+pymysql://root:Bento1801?@localhost/salao_inteligente"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#==================================================================================================
# Conexão/Reconexão automática Supabase - atualizadas - 28.03.25 - Trecho 3 - Fim
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
# Modelo de Tabela usuarios - Supabase - atualizadas - 28.03.25 - Trecho 4 - Início
#==================================================================================================


# 📌 Modelo da Tabela `usuarios`
class UsuarioDB(Base):
    __tablename__ = "usuarios"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True, autoincrement=True)
    nome: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    telefone: Mapped[str] = mapped_column(String(11), nullable=False)
    cpf: Mapped[str] = mapped_column(String(11), unique=True, nullable=False)
    senha: Mapped[str] = mapped_column(String(255), nullable=False)
    data_criacao: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.current_timestamp())

Base.metadata.create_all(bind=engine)  # Criar a tabela no banco


#==================================================================================================
# Modelo de Tabela usuarios - Supabase - atualizadas - 28.03.25 - Trecho 4 - Fim
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
# Schema de Tabela usuarios - Supabase - atualizadas - 28.03.25 - Trecho 5 - Início
#==================================================================================================


# 📌 Validação de Dados com Pydantic
from typing import Annotated
from pydantic import BaseModel, EmailStr, Field, StringConstraints, model_validator

class UsuarioSchema(BaseModel):
    nome: Annotated[str,StringConstraints(min_length=3, max_length=255, pattern=r'^[A-Za-z\s]+$')]
    email: EmailStr
    telefone: Annotated[str,StringConstraints(min_length=11, max_length=11, pattern=r'^[0-9]+$')]
    cpf: Annotated[str,StringConstraints(min_length=11, max_length=11, pattern=r'^[0-9]+$')]
    senha: Annotated[str,StringConstraints(min_length=8)]
    repetirSenha: str


    @model_validator(mode="after")
    def senha_confere(self) -> "UsuarioSchema":
        if self.senha != self.repetirSenha:
            raise ValueError("As senhas não conferem")
        if not re.search(r'[A-Za-z]', self.senha):
            raise ValueError("A senha deve conter pelo menos uma letra")
        if not re.search(r'\d', self.senha):
            raise ValueError("A senha deve conter pelo menos um número")
        if not re.search(r'[@$!%*?&]', self.senha):
            raise ValueError("A senha deve conter pelo menos um caractere especial (@$!%*?&)")
        return self

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str


#==================================================================================================
# Schema de Tabela usuarios - Supabase - atualizadas - 28.03.25 - Trecho 5 - Fim
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
# Rotas para Cadastro de Usuários - atualizadas - 28.03.25 - Trecho 6 - Início
#==================================================================================================


@app.post("/cadastrar")
def cadastrar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    usuario = usuario.senha_confere()  # Validar e reatribuir

    # Verificar se o email ou CPF já existem
    if db.query(UsuarioDB).filter(UsuarioDB.email == usuario.email).first():
        raise HTTPException(status_code=409, detail="Email já cadastrado")
    if db.query(UsuarioDB).filter(UsuarioDB.cpf == usuario.cpf).first():
        raise HTTPException(status_code=409, detail="CPF já cadastrado")
    
    # Criptografar senha
    hashed_senha = bcrypt.hashpw(usuario.senha.encode('utf-8'), bcrypt.gensalt())
    
    # Criar novo usuário no banco
    novo_usuario = UsuarioDB(
        nome=usuario.nome,
        email=usuario.email,
        telefone=usuario.telefone,
        cpf=usuario.cpf,
        senha=hashed_senha.decode('utf-8')
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    
    return {"mensagem": "Cadastro realizado com sucesso"}

@app.get("/cadastrar")
def get_cadastrar():
    return {"mensagem": "Endpoint para cadastro de usuários. Use o método POST para enviar dados."}

@app.put("/cadastrar")
def put_cadastrar():
    return {"mensagem": "Método PUT não implementado para este endpoint."}

@app.delete("/cadastrar")
def delete_cadastrar():
    return {"mensagem": "Método DELETE não implementado para este endpoint."}

@app.patch("/cadastrar")
def patch_cadastrar():
    return {"mensagem": "Método PATCH não implementado para este endpoint."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

#==================================================================================================
# Rotas para Cadastro de Usuários - atualizadas - 28.03.25 - Trecho 6 - Fim
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
#==================================================================================================
# Incluir Nome do Trecho - atualizadas - 28.03.25 - Trecho 7 - Início
#==================================================================================================


from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints


class LoginSchema(BaseModel):
    email: EmailStr
    senha: Annotated[str,StringConstraints(min_length=8, strip_whitespace=True)]


def criar_token(dados: dict):
    expiracao = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados["exp"] = expiracao
    return jwt.encode(dados, SECRET_KEY, algorithm=ALGORITHM)

@app.post("/login")
def login(login: LoginSchema, db: Session = Depends(get_db)):
    # Buscar usuário no banco de dados
    usuario = db.query(UsuarioDB).filter(UsuarioDB.email == login.email).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")

    # Verificar senha usando bcrypt
    if not bcrypt.checkpw(login.senha.encode('utf-8'), usuario.senha.encode('utf-8')):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    
    # Criar token JWT
    token = criar_token({
         "sub": usuario.email,
         "id": usuario.id,  # 👈 Agora o ID será incluso no token
         "nome": usuario.nome  # (opcional) você pode adicionar mais dados se quiser
    })

    return {"token": token}



@app.get("/usuario_logado")
def usuario_logado(token_data: dict = Depends(verificar_token)):
    usuario_email = token_data.get("sub")
    return {"email_usuario": usuario_email, "status": "Autenticado ✅"}

#==================================================================================================
# Incluir Nome do Trecho - atualizadas - 28.03.25 - Trecho 7 - Fim
#==================================================================================================
