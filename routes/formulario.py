# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\routes\formulario.py
# ============================================================
# 🚀 Rota de Cadastro de Usuário - `formulario.py`
# ============================================================

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, constr
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import bcrypt
from database import SessionLocal
from models import Usuario

# ============================================================
# 🚀 Configuração do Router
# ============================================================
router = APIRouter()

# ============================================================
# 🚀 Modelo de Dados para Entrada da API (Pydantic)
# ============================================================
class UsuarioSchema(BaseModel):
    """
    Modelo de dados para validação do cadastro de usuário.
    """
    nome: constr(strip_whitespace=True, min_length=3, pattern="^[a-zA-Z\s]+$")
    email: EmailStr
    telefone: constr(strip_whitespace=True, min_length=11, max_length=11, regex="^\d{11}$")
    cpf: constr(strip_whitespace=True, min_length=11, max_length=11, regex="^\d{11}$")
    senha: constr(min_length=8, regex="^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$")
    repetirSenha: str

    class Config:
        orm_mode = True

# ============================================================
# 🚀 Dependência do banco de dados
# ============================================================
def get_db():
    """
    Gerencia a sessão do banco de dados para cada requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ============================================================
# 🚀 Rota para cadastrar um novo usuário
# ============================================================
@router.post("/cadastrar", status_code=200)
def cadastrar_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    """
    Endpoint para cadastro de um novo usuário no banco de dados.

    1️⃣ Valida os dados recebidos do frontend.
    2️⃣ Verifica se o e-mail ou CPF já estão cadastrados.
    3️⃣ Criptografa a senha antes de salvar.
    4️⃣ Insere o usuário no banco de dados.
    5️⃣ Retorna uma resposta adequada conforme o resultado.
    """

    # 1️⃣ Valida se as senhas coincidem
    if usuario.senha != usuario.repetirSenha:
        raise HTTPException(status_code=400, detail="As senhas não coincidem.")

    # 2️⃣ Verifica se o usuário já existe (email ou CPF)
    usuario_existente = db.query(Usuario).filter(
        (Usuario.email == usuario.email) | (Usuario.cpf == usuario.cpf)
    ).first()

    if usuario_existente:
        raise HTTPException(status_code=409, detail="Usuário já cadastrado.")

    # 3️⃣ Criptografar a senha antes de armazenar no banco
    hashed_senha = bcrypt.hashpw(usuario.senha.encode("utf-8"), bcrypt.gensalt())

    # 4️⃣ Criar novo usuário no banco de dados
    novo_usuario = Usuario(
        nome=usuario.nome,
        email=usuario.email,
        telefone=usuario.telefone,
        cpf=usuario.cpf,
        senha=hashed_senha.decode("utf-8")
    )

    try:
        db.add(novo_usuario)
        db.commit()
        db.refresh(novo_usuario)
        return {"message": "Cadastro realizado com sucesso!"}
    
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Usuário já cadastrado.")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erro interno no servidor: {str(e)}")

# ============================================================
# 🚀 Teste da API
# ============================================================
"""
Para testar esta rota, inicie o servidor com:

    uvicorn main:app --reload

Depois, use o Postman, cURL ou o frontend para enviar uma requisição POST para:

    http://127.0.0.1:8000/cadastrar

📌 Corpo esperado da requisição (JSON):

{
  "nome": "Ana Oliveira",
  "email": "ana@email.com",
  "telefone": "11999999999",
  "cpf": "11122233344",
  "senha": "Teste@123",
  "repetirSenha": "Teste@123"
}

📌 Respostas esperadas:

✅ 200 OK → { "message": "Cadastro realizado com sucesso!" }
❌ 400 Bad Request → { "detail": "As senhas não coincidem." }
❌ 400 Bad Request → { "detail": "Telefone inválido." } (ou outros erros de validação)
❌ 409 Conflict → { "detail": "Usuário já cadastrado." }
❌ 500 Internal Server Error → { "detail": "Erro interno no servidor." }
"""
