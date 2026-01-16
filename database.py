# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool


DATABASE_URL = "postgresql://postgres.gbjpgklizrfocjecuolh:4u5TNz6jnQCLMks0@db.gbjpgklizrfocjecuolh.supabase.co:6543/postgres?sslmode=require"

engine = create_engine(
    DATABASE_URL,
    poolclass=NullPool, # Impede que a Vercel trave conexões
    connect_args={
        "connect_timeout": 30,
        "prepare_threshold": None # OBRIGATÓRIO para Pooler Transaction Mode
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