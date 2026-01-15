# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\models.py
# ============================================================
# 🚀 Definição do Modelo de Usuário - `models.py`
# ============================================================

from sqlalchemy import TIMESTAMP, Column, Integer, String, Text, func
from sqlalchemy.ext.declarative import declarative_base 
from database import Base, engine

# ============================================================
# 🚀 Modelo ORM para a Tabela `usuarios`
# ============================================================
class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    telefone = Column(String(11), nullable=False)
    cpf = Column(String(11), unique=True, nullable=False)
    senha = Column(Text, nullable=False)  # Senha será armazenada criptografada
    data_criacao = Column(TIMESTAMP, server_default=func.current_timestamp())  # Data automáticamente preenchida
    

# ============================================================
# 🚀 Criar a tabela no banco de dados
# ============================================================
def criar_tabelas():
    print("🔍 Verificando/criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tabelas verificadas e criadas com sucesso!")

# ============================================================
# 🚀 Executa a criação das tabelas ao rodar o script
# ============================================================
if __name__ == "__main__":
    criar_tabelas()
