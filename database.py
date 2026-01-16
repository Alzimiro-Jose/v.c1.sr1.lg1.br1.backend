# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import NullPool

# 🔹 Voltamos ao usuário 'postgres' puro
# 🔹 Adicionamos o parâmetro 'options=-c project=gbjpgklizrfocjecuolh'
# 🔹 Isso força o Pooler a identificar o seu projeto (Tenant)
DATABASE_URL = "postgresql://postgres:4u5TNz6jnQCLMks0@aws-0-sa-east-1.pooler.supabase.com:6543/postgres?sslmode=require&options=-c%20project=gbjpgklizrfocjecuolh"

engine = create_engine(DATABASE_URL, poolclass=NullPool)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

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