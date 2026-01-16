# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 🔹 FORMATO OFICIAL PARA VERCEL (Supavisor Transaction Mode)
# 🔹 O usuário DEVE conter o seu ID de projeto separado por um ponto
# 🔹 A porta DEVE ser 6543
DATABASE_URL = "postgresql://postgres.gbjpgklizrfocjecuolh:4u5TNz6jnQCLMks0@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool, # Já está correto no seu código
    connect_args={
        "connect_timeout": 30,
        "prepare_threshold": None # Mantido conforme sua última versão
    }
)

def testar_conexao():
    try:
        with engine.connect() as conn:
            # Comando simples que funciona em qualquer banco
            from sqlalchemy import text
            conn.execute(text("SELECT 1"))
            print("✅ Conexão com o Supabase (PostgreSQL) estabelecida com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")

if __name__ == "__main__":
    testar_conexao()