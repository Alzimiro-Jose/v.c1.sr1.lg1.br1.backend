# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\routes\usuarios.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Optional

# 📌 Criar um roteador para cada entidade (copie e edite para cada caso)
router = APIRouter(prefix="/usuarios")  # Altere "entidade" para o nome correto

# 📌 Simulando banco de dados (Temporário)
dados_db: Dict[int, dict] = {}

# 📌 Modelo Base para qualquer entidade
class ModeloBase(BaseModel):
    nome: str
    descricao: Optional[str] = None

# 📌 Rota GET: Listar todos os registros
@router.get("/")
async def listar_registros():
    return {"dados": list(dados_db.values())}

# 📌 Rota POST: Criar novo registro
@router.post("/")
async def criar_registro(dados: ModeloBase):
    novo_id = len(dados_db) + 1
    dados_db[novo_id] = dados.model_dump()
    return {"id": novo_id, "message": "Registro criado com sucesso!"}

# 📌 Rota PUT: Atualizar registro por ID
@router.put("/{registro_id}")
async def atualizar_registro(registro_id: int, dados: ModeloBase):
    if registro_id not in dados_db:
        raise HTTPException(status_code=404, detail="Registro não encontrado")
    
    dados_db[registro_id] = dados.model_dump()
    return {"message": "Registro atualizado com sucesso!"}

# 📌 Rota DELETE: Deletar registro por ID
@router.delete("/{registro_id}")
async def deletar_registro(registro_id: int):
    if registro_id not in dados_db:
        raise HTTPException(status_code=404, detail="Registro não encontrado")

    del dados_db[registro_id]
    return {"message": "Registro deletado com sucesso!"}