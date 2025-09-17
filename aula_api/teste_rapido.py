#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TESTE RÁPIDO: Verificação da API FastAPI

Este arquivo testa rapidamente se a API está funcionando corretamente.
Execute para verificar se tudo está configurado adequadamente.

Autor: LabExtracaoAnalise2025
Data: 2025
"""

import requests
import json
import time
from datetime import datetime

def testar_api_simples():
    """Testa a API simples de produtos"""
    print("🧪 TESTANDO API SIMPLES...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Teste 1: Endpoint raiz
        print("1. Testando endpoint raiz...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Endpoint raiz funcionando")
            print(f"   📝 Resposta: {response.json()}")
        else:
            print(f"   ❌ Erro no endpoint raiz: {response.status_code}")
            return False
        
        # Teste 2: Listar produtos
        print("\n2. Testando listagem de produtos...")
        response = requests.get(f"{base_url}/produtos")
        if response.status_code == 200:
            produtos = response.json()
            print(f"   ✅ Produtos listados: {len(produtos)} encontrados")
            for produto in produtos[:2]:  # Mostrar apenas os 2 primeiros
                print(f"      - {produto['nome']} (R$ {produto['preco']})")
        else:
            print(f"   ❌ Erro ao listar produtos: {response.status_code}")
            return False
        
        # Teste 3: Criar produto
        print("\n3. Testando criação de produto...")
        novo_produto = {
            "nome": "Produto de Teste",
            "preco": 99.99,
            "categoria": "Teste",
            "em_estoque": True
        }
        response = requests.post(f"{base_url}/produtos", json=novo_produto)
        if response.status_code == 201:
            produto_criado = response.json()
            print(f"   ✅ Produto criado com ID: {produto_criado['id']}")
            produto_id = produto_criado['id']
        else:
            print(f"   ❌ Erro ao criar produto: {response.status_code}")
            return False
        
        # Teste 4: Buscar produto específico
        print("\n4. Testando busca de produto específico...")
        response = requests.get(f"{base_url}/produtos/{produto_id}")
        if response.status_code == 200:
            produto = response.json()
            print(f"   ✅ Produto encontrado: {produto['nome']}")
        else:
            print(f"   ❌ Erro ao buscar produto: {response.status_code}")
            return False
        
        # Teste 5: Busca por termo
        print("\n5. Testando busca por termo...")
        response = requests.get(f"{base_url}/buscar?q=teste")
        if response.status_code == 200:
            resultados = response.json()
            print(f"   ✅ Busca funcionando: {len(resultados)} resultados")
        else:
            print(f"   ❌ Erro na busca: {response.status_code}")
            return False
        
        # Teste 6: Estatísticas
        print("\n6. Testando estatísticas...")
        response = requests.get(f"{base_url}/estatisticas")
        if response.status_code == 200:
            stats = response.json()
            print(f"   ✅ Estatísticas: {stats['total_produtos']} produtos")
        else:
            print(f"   ❌ Erro nas estatísticas: {response.status_code}")
            return False
        
        print("\n🎉 TODOS OS TESTES PASSARAM! API funcionando perfeitamente!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar à API")
        print("   Verifique se o servidor está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        return False

def testar_api_completa():
    """Testa a API completa com autenticação"""
    print("\n🧪 TESTANDO API COMPLETA...")
    
    base_url = "http://localhost:8000"
    
    try:
        # Teste 1: Endpoint raiz
        print("1. Testando endpoint raiz...")
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Endpoint raiz funcionando")
        else:
            print(f"   ❌ Erro no endpoint raiz: {response.status_code}")
            return False
        
        # Teste 2: Health check
        print("\n2. Testando health check...")
        response = requests.get(f"{base_url}/health")
        if response.status_code == 200:
            health = response.json()
            print(f"   ✅ Health check: {health['status']}")
        else:
            print(f"   ❌ Erro no health check: {response.status_code}")
            return False
        
        # Teste 3: Login
        print("\n3. Testando login...")
        credenciais = {
            "email": "admin@sistema.com",
            "senha": "123456"
        }
        response = requests.post(f"{base_url}/auth/login", json=credenciais)
        if response.status_code == 200:
            token_data = response.json()
            token = token_data['access_token']
            print(f"   ✅ Login realizado, token obtido")
        else:
            print(f"   ❌ Erro no login: {response.status_code}")
            return False
        
        # Teste 4: Criar usuário (sem autenticação)
        print("\n4. Testando criação de usuário...")
        novo_usuario = {
            "nome": "Usuário Teste",
            "email": "teste@exemplo.com",
            "idade": 25,
            "senha": "123456"
        }
        response = requests.post(f"{base_url}/usuarios", json=novo_usuario)
        if response.status_code == 201:
            usuario_criado = response.json()
            print(f"   ✅ Usuário criado: {usuario_criado['nome']}")
        else:
            print(f"   ❌ Erro ao criar usuário: {response.status_code}")
            return False
        
        # Teste 5: Criar tarefa (com autenticação)
        print("\n5. Testando criação de tarefa...")
        headers = {"Authorization": f"Bearer {token}"}
        nova_tarefa = {
            "titulo": "Tarefa de Teste",
            "descricao": "Descrição da tarefa de teste",
            "prioridade": "média"
        }
        response = requests.post(f"{base_url}/tarefas", json=nova_tarefa, headers=headers)
        if response.status_code == 201:
            tarefa_criada = response.json()
            print(f"   ✅ Tarefa criada: {tarefa_criada['titulo']}")
        else:
            print(f"   ❌ Erro ao criar tarefa: {response.status_code}")
            return False
        
        print("\n🎉 TODOS OS TESTES DA API COMPLETA PASSARAM!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ ERRO: Não foi possível conectar à API")
        print("   Verifique se o servidor está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"❌ ERRO INESPERADO: {e}")
        return False

def verificar_servidor():
    """Verifica se o servidor está rodando"""
    print("🔍 VERIFICANDO SE O SERVIDOR ESTÁ RODANDO...")
    
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Servidor está rodando em http://localhost:8000")
            return True
        else:
            print(f"⚠️  Servidor respondeu com status: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Servidor não está rodando")
        print("\n💡 Para iniciar o servidor:")
        print("   cd aula_api")
        print("   python exemplo_simples.py")
        print("   # ou")
        print("   uvicorn exemplo_simples:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Erro ao verificar servidor: {e}")
        return False

def main():
    """Função principal de teste"""
    print("🚀 TESTE RÁPIDO - FASTAPI")
    print("=" * 50)
    print(f"⏰ Iniciando testes em: {datetime.now().strftime('%H:%M:%S')}")
    
    # Verificar se o servidor está rodando
    if not verificar_servidor():
        return
    
    print("\n" + "=" * 50)
    
    # Testar API simples
    sucesso_simples = testar_api_simples()
    
    print("\n" + "=" * 50)
    
    # Testar API completa
    sucesso_completa = testar_api_completa()
    
    print("\n" + "=" * 50)
    
    # Resumo final
    print("📊 RESUMO DOS TESTES:")
    print(f"   API Simples: {'✅ PASSOU' if sucesso_simples else '❌ FALHOU'}")
    print(f"   API Completa: {'✅ PASSOU' if sucesso_completa else '❌ FALHOU'}")
    
    if sucesso_simples and sucesso_completa:
        print("\n🎉 PARABÉNS! Todas as APIs estão funcionando perfeitamente!")
        print("📚 Acesse a documentação em: http://localhost:8000/docs")
    else:
        print("\n⚠️  Alguns testes falharam. Verifique os logs acima.")
    
    print(f"\n⏰ Testes finalizados em: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()









