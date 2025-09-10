#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AULA: Trabalhando com APIs em Python
=====================================

Esta aula ensina como:
1. Fazer requisições HTTP usando a biblioteca requests
2. Trabalhar com dados JSON
3. Converter dados JSON para DataFrames do Pandas
4. Exportar dados para diferentes formatos
5. Aplicar esses conceitos em diferentes APIs

Autor: Prof. Matheus C. Pestana
Data: 2025
"""

# =============================================================================
# IMPORTAÇÕES NECESSÁRIAS
# =============================================================================

import requests
import pandas as pd
import json
from datetime import datetime
import time

# =============================================================================
# CONCEITOS BÁSICOS DE APIs
# =============================================================================

print("🎓 AULA: Trabalhando com APIs em Python")
print("=" * 50)

print("""
O QUE É UMA API?
================

API (Application Programming Interface) é uma interface que permite que diferentes
softwares se comuniquem entre si. No contexto web, APIs REST permitem que você
faça requisições HTTP para obter dados de servidores.

TIPOS DE REQUISIÇÕES HTTP:
- GET: Buscar dados ----> O MAIS UTILIZADO!
- POST: Enviar dados
- PUT: Atualizar dados
- DELETE: Deletar dados

CÓDIGOS DE STATUS HTTP:
- 200: Sucesso
- 404: Não encontrado
- 500: Erro interno do servidor
- 401: Não autorizado
""")

# =============================================================================
# EXEMPLO PRÁTICO: API HARRY POTTER (EM SCRIPT DIRETO)
# =============================================================================

print("\n" + "="*60)
print("EXEMPLO PRÁTICO: API HARRY POTTER")
print("="*60)

# URL base da API
url_base = "https://potterapi-fedeperin.vercel.app/pt"

# 1. BUSCAR LIVROS
print("\n📚 1. Buscando livros...")
url_livros = f"{url_base}/books"

try:
    print(f"Fazendo requisição para: {url_livros}")
    response = requests.get(url_livros)
    
    if response.status_code == 200:
        print("✅ Requisição realizada com sucesso!")
        livros_json = response.json()
        print(f"Encontrados {len(livros_json)} livros")
        print("Primeiro livro:", livros_json[0]['title'] if livros_json else "N/A")
        
        # Converter para DataFrame
        df_livros = pd.DataFrame(livros_json)
        print(f"✅ Dados convertidos para DataFrame: {df_livros.shape[0]} linhas, {df_livros.shape[1]} colunas")
        print("\nDataFrame dos livros:")
        print(df_livros.head())
        
        # Exportar dados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo = f"harry_potter_livros_{timestamp}.csv"
        df_livros.to_csv(arquivo, index=False, encoding='utf-8')
        print(f"✅ Dados exportados para: {arquivo}")
        
    else:
        print(f"❌ Erro na requisição. Código: {response.status_code}")
        
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# 2. BUSCAR PERSONAGENS
print("\n👥 2. Buscando personagens...")
url_personagens = f"{url_base}/characters"

try:
    print(f"Fazendo requisição para: {url_personagens}")
    response = requests.get(url_personagens)
    
    if response.status_code == 200:
        print("✅ Requisição realizada com sucesso!")
        personagens_json = response.json()
        print(f"Encontrados {len(personagens_json)} personagens")
        
        # Converter para DataFrame
        df_personagens = pd.DataFrame(personagens_json)
        print(f"✅ Dados convertidos para DataFrame: {df_personagens.shape[0]} linhas, {df_personagens.shape[1]} colunas")
        print("\nDataFrame dos personagens:")
        print(df_personagens.head())
        
        # Análise rápida
        if 'house' in df_personagens.columns:
            print("\nDistribuição por casa:")
            print(df_personagens['house'].value_counts())
        
        # Exportar dados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo = f"harry_potter_personagens_{timestamp}.xlsx"
        df_personagens.to_excel(arquivo, index=False)
        print(f"✅ Dados exportados para: {arquivo}")
        
    else:
        print(f"❌ Erro na requisição. Código: {response.status_code}")
        
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# 3. BUSCAR FEITIÇOS
print("\n✨ 3. Buscando feitiços...")
url_feiticos = f"{url_base}/spells"

try:
    print(f"Fazendo requisição para: {url_feiticos}")
    response = requests.get(url_feiticos)
    
    if response.status_code == 200:
        print("✅ Requisição realizada com sucesso!")
        feiticos_json = response.json()
        print(f"Encontrados {len(feiticos_json)} feitiços")
        
        # Converter para DataFrame
        df_feiticos = pd.DataFrame(feiticos_json)
        print(f"✅ Dados convertidos para DataFrame: {df_feiticos.shape[0]} linhas, {df_feiticos.shape[1]} colunas")
        print("\nDataFrame dos feitiços:")
        print(df_feiticos.head())
        
        # Exportar dados
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        arquivo = f"harry_potter_feiticos_{timestamp}.json"
        df_feiticos.to_json(arquivo, orient='records', indent=2, force_ascii=False)
        print(f"✅ Dados exportados para: {arquivo}")
        
    else:
        print(f"❌ Erro na requisição. Código: {response.status_code}")
        
except Exception as e:
    print(f"❌ Erro na requisição: {e}")

# =============================================================================
# REFLEXÃO: QUANDO CRIAR FUNÇÕES
# =============================================================================

print("\n" + "="*60)
print("REFLEXÃO: QUANDO CRIAR FUNÇÕES?")
print("="*60)

print("""
O código acima funciona perfeitamente em script, mas imagine se você quisesse:

1. Buscar dados de MÚLTIPLAS APIs
2. Repetir o mesmo processo várias vezes
3. Organizar melhor o código
4. Reutilizar partes do código

Nesse caso, seria IDEAL criar funções! Por exemplo:

def buscar_dados_api(url, nome_dataset):
    dados = requests.get(url).json()
    df = pd.DataFrame(dados)
    df.to_csv(f"{nome_dataset}.csv", index=False)
    return df

# E então usar:
df_livros = buscar_dados_api(f"{url_base}/books", "livros")
df_personagens = buscar_dados_api(f"{url_base}/characters", "personagens")
""")


# Dicas finais
print("\n" + "="*60)
print("DICAS IMPORTANTES")
print("="*60)
print("✅ Sempre trate erros nas requisições")
print("✅ Use time.sleep() entre requisições para não sobrecarregar APIs")
print("✅ Salve seus dados regularmente")
print("✅ Documente seu código")
print("✅ Teste com pequenas amostras primeiro")
print("✅ Respeite os limites das APIs")