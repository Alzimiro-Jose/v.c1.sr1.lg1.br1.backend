# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL corrigida (sem https:// e com a senha que você inseriu)
DATABASE_URL = "postgresql://postgres:k2ukutacP3O4KDPX@db.gbjpgklizrfocjecuolh.supabase.co:5432/postgres"

# Engine para PostgreSQL
engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Use apenas UMA vez
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