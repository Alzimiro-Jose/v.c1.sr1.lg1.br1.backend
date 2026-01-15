# // C:\Users\User\Desktop\Modelos com Pipelines\v.w1.c1.sr1.lg1.br1\backend\test_endpoints.py
import requests
import random
import string
import json

# 🔹 CONFIGURAÇÃO
BASE_URL = "http://127.0.0.1:8000"

# 🔹 Lista de entidades e seus campos para teste
ENTIDADES = {
    "usuarios": ["nome", "descricao", "email", "senha", "id", "dados"],
    # Para adicionar uma nova entidade, basta incluir aqui:
    # "estabelecimentos": ["nome", "telefone", "categorias"],
}

# 🔹 Função para gerar strings aleatórias cobrindo TODOS os tipos de caracteres
def gerar_string_aleatoria(tamanho=12, incluir_espacos=True):
    caracteres = string.ascii_letters + string.digits + string.punctuation + "😃🎉🔥✅🚀"
    if incluir_espacos:
        caracteres += " \n\t"
    return ''.join(random.choices(caracteres, k=tamanho))

# 🔹 Função para gerar payloads dinamicamente com base na entidade
def gerar_payload(entidade):
    payload = {}
    if entidade in ENTIDADES:
        for campo in ENTIDADES[entidade]:
            payload[campo] = gerar_string_aleatoria(10)
    return payload

# 🔹 Teste dos endpoints para cada entidade detectada
def testar_endpoints():
    print("\n🚀 Iniciando testes automatizados dos endpoints...\n")

    for entidade, campos in ENTIDADES.items():
        url = f"{BASE_URL}/{entidade}"

        print(f"\n🔍 **Testando entidade: {entidade.upper()}**")
        print(f"📌 Campos detectados: {', '.join(campos)}")

        # 🔹 Teste GET
        response = requests.get(url)
        print(f"🔹 Testando GET para {entidade}...")
        if response.status_code == 200:
            print(f"✅ GET {url} - Sucesso (200)")
        else:
            print(f"❌ GET {url} - Falha ({response.status_code}): {response.text}")

        # 🔹 Teste POST com caracteres especiais
        payload = gerar_payload(entidade)
        for campo in payload.keys():
            payload[campo] += " 😃🔥\n\t"  # Adicionando caracteres especiais
        
        response = requests.post(url, json=payload)
        print(f"🔹 Testando POST para {entidade} com caracteres especiais...")
        if response.status_code in [200, 201]:
            print(f"✅ POST {url} - Sucesso ({response.status_code})")
            novo_id = response.json().get("id", 1)
        else:
            print(f"❌ POST {url} - Falha ({response.status_code}): {response.text}")
            novo_id = None

        # 🔹 Teste PUT (Se o POST teve sucesso)
        if novo_id:
            payload = gerar_payload(entidade)  # Gera novo payload
            response = requests.put(f"{url}/{novo_id}", json=payload)
            print(f"🔹 Testando PUT para {entidade}...")
            if response.status_code == 200:
                print(f"✅ PUT {url}/{novo_id} - Sucesso (200)")
            else:
                print(f"❌ PUT {url}/{novo_id} - Falha ({response.status_code}): {response.text}")

        # 🔹 Teste DELETE (Se o POST teve sucesso)
        if novo_id:
            response = requests.delete(f"{url}/{novo_id}")
            print(f"🔹 Testando DELETE para {entidade}...")
            if response.status_code == 200:
                print(f"✅ DELETE {url}/{novo_id} - Sucesso (200)")
            else:
                print(f"❌ DELETE {url}/{novo_id} - Falha ({response.status_code}): {response.text}")

        print("\n" + "-" * 60)

    print("\n✅ **Todos os testes concluídos!**\n")

if __name__ == "__main__":
    testar_endpoints()
