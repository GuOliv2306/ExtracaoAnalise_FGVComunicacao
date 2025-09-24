import requests
import json

# Configuração da API
API_BASE = "http://localhost:8001"

def testar_analise_ia():
    """
    Exemplo de como usar os endpoints de análise de IA
    """
    
    print("=== TESTANDO ENDPOINTS DE IA ===\n")
    
    # 1. Testar endpoint GET /IA (informações)
    print("1. Obtendo informações sobre análise de IA:")
    response = requests.get(f"{API_BASE}/IA")
    if response.status_code == 200:
        data = response.json()
        print(f"✅ Sucesso: {data['message']}")
        print(f"📊 Total de registros: {data['dataset_info']['total_registros']}")
        print(f"📋 Colunas: {', '.join(data['dataset_info']['colunas'])}\n")
    else:
        print(f"❌ Erro: {response.status_code}\n")
    
    # 2. Testar análise rápida via GET
    print("2. Testando análise rápida:")
    pergunta_rapida = "Qual a taxa de sobrevivência geral?"
    response = requests.get(f"{API_BASE}/analise_rapida/{pergunta_rapida}")
    if response.status_code == 200:
        data = response.json()
        print(f"❓ Pergunta: {data['pergunta']}")
        print(f"📈 Resposta: {data.get('resposta_rapida', 'N/A')[:200]}...")
        print(f"✅ Status: {data['status']}\n")
    else:
        print(f"❌ Erro na análise rápida: {response.status_code}\n")
    
    # 3. Testar análise completa via POST
    print("3. Testando análise completa:")
    payload = {
        "pergunta": "Analise a sobrevivência por classe social e gênero. Quais são os principais insights?",
        "contexto": "Dataset Titanic - análise detalhada de sobrevivência"
    }
    
    response = requests.post(f"{API_BASE}/analise_ia", json=payload)
    if response.status_code == 200:
        data = response.json()
        print(f"❓ Pergunta: {data['pergunta']}")
        print(f"🎯 Contexto: {data['contexto']}")
        print(f"📊 Resposta: {data.get('resposta', 'N/A')[:300]}...")
        print(f"⏰ Timestamp: {data['timestamp']}")
        print(f"✅ Status: {data['status']}\n")
    else:
        print(f"❌ Erro na análise completa: {response.status_code}")
        try:
            error_data = response.json()
            print(f"📝 Detalhes do erro: {error_data}\n")
        except:
            print(f"📝 Resposta do servidor: {response.text}\n")

def exemplos_perguntas():
    """
    Exemplos de perguntas que podem ser feitas à IA
    """
    print("=== EXEMPLOS DE PERGUNTAS PARA A IA ===\n")
    
    perguntas_exemplo = [
        "Qual a taxa de sobrevivência por classe social?",
        "Homens ou mulheres tiveram maior chance de sobreviver?",
        "Qual a idade média dos sobreviventes?",
        "Como o porto de embarque influenciou a sobrevivência?",
        "Quais são as principais estatísticas do dataset?",
        "Faça uma análise comparativa entre classes sociais",
        "Quais fatores mais influenciaram a sobrevivência?"
    ]
    
    for i, pergunta in enumerate(perguntas_exemplo, 1):
        print(f"{i}. {pergunta}")
    
    print(f"\n💡 Para testar: GET {API_BASE}/analise_rapida/[sua_pergunta]")
    print(f"💡 Para análise completa: POST {API_BASE}/analise_ia com JSON")

if __name__ == "__main__":
    # Primeiro mostrar exemplos
    exemplos_perguntas()
    print("\n" + "="*50 + "\n")
    
    # Depois testar (descomente para executar os testes)
    try:
        testar_analise_ia()
    except requests.exceptions.ConnectionError:
        print("❌ Erro: Não foi possível conectar à API.")
        print("🔧 Certifique-se de que a API está rodando em http://localhost:8001")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
