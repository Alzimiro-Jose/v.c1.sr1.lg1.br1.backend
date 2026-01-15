import requests
import json

# 🔹 CONFIGURAÇÃO: URL da sua API na Vercel
BASE_URL = "https://v-c1-sr1-lg1-br1-backend.vercel.app"

def testar_saude_api():
    print(f"\n🔍 Testando conexão com: {BASE_URL}")
    try:
        # Testando o endpoint de login com dados vazios apenas para ver a resposta do servidor
        response = requests.post(f"{BASE_URL}/login", json={"email": "teste@email.com", "senha": "123"})
        
        # Se receber 401 ou 200, a API está VIVA e conectada ao banco.
        # Se receber 500, a API está VIVA mas o BANCO está desconectado.
        if response.status_code in [200, 401]:
            print(f"✅ API Online e Banco Conectado! (Status: {response.status_code})")
        elif response.status_code == 500:
            print(f"❌ Erro 500: API Online, mas falhou ao falar com o Supabase.")
        else:
            print(f"⚠️ Resposta inesperada: {response.status_code}")
            print(f"Detalhe: {response.text}")
            
    except Exception as e:
        print(f"🔴 Erro crítico ao alcançar a Vercel: {e}")

if __name__ == "__main__":
    testar_saude_api()