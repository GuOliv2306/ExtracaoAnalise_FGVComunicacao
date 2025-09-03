# 🎵 Tarefa de Graduação: Extrator de Letras de Músicas

## 📋 **Objetivo da Tarefa**

Desenvolver um script em Python que automatize a extração de letras de músicas do site **Letras.mus.br**. O programa deve ser capaz de buscar por um artista específico, coletar uma lista de suas músicas e extrair as letras, visualizações e informações de composição de cada música.

## 🎯 **Competências a serem Desenvolvidas**

- **Web Scraping**: Automação de navegador com Selenium
- **Parsing HTML**: Extração de dados com BeautifulSoup
- **Manipulação de Dados**: Organização e estruturação com Pandas
- **Programação Orientada a Objetos**: Estruturação do código em classes/funções
- **Documentação**: Comentários e docstrings claros

## 🔧 **Tecnologias e Bibliotecas Obrigatórias**

### **Bibliotecas Principais:**
```python
# Automação web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions

# Gerenciamento automático de drivers
from webdriver_manager.chrome import ChromeDriverManager

# Parsing HTML
from bs4 import BeautifulSoup

# Manipulação de dados
import pandas as pd

# Requisições HTTP
import requests

# Barra de progresso
from tqdm import tqdm

# Utilitários
import time
```

## 📝 **Especificações Técnicas**

### **1. Funcionalidades Obrigatórias:**

#### **1.1 Navegação e Busca**
- Acessar o site https://www.letras.mus.br
- Localizar o campo de busca usando seletores (campos, como classe, atributos, etc) apropriados
- Permitir que o usuário escolha o artista a ser pesquisado
- Implementar seleção do primeiro resultado da busca

#### **1.2 Extração da Lista de Músicas**
- Extrair todas as músicas da página de resultados
- Coletar: URL, título e artista de cada música
- Armazenar em estrutura de dados apropriada (lista de dicionários)

#### **1.3 Extração de Detalhes das Músicas**
- Para cada música, acessar sua página individual
- Extrair:
  - **Letra completa** da música
  - **Número de visualizações**
  - **Informações de composição** (autores, compositores)

#### **1.4 Salvamento dos Dados**
- Salvar todos os dados em arquivo CSV
- Incluir metadados: data de extração (+0,1)
- Implementar encoding UTF-8 para caracteres especiais

### **2. Estrutura do Código:**

#### **2.1 Organização Recomendada:**
```python
# 1. Imports e configurações
# 2. Configuração do navegador
# 3. Função de busca de artista
# 4. Função de extração de lista de músicas
# 5. Função de extração de detalhes
# 6. Função de salvamento
# 7. Função principal (main)
# 8. Execução do script
```

> **Nota**: Você pode escolher qualquer artista, desde que tenha um catálogo significativo no Letras.mus.br, o que significa ter pelo menos 70 músicas.

### **⚡ Otimizações Recomendadas:**
```python
# 1. Reutilizar sessão HTTP
session = requests.Session()

# 2. Implementar delays apropriados
time.sleep(2)  # Entre requisições

# 3. Usar barra de progresso
for song in tqdm(songs_list, desc="Extraindo letras"):
    # processamento
```

### **🛡️ Tratamento de Erros:**
```python
try:
    # operação crítica
    lyrics = soup.find('div', {'class': 'lyric-original'}).get_text()
except AttributeError:
    lyrics = "Letra não encontrada"
except Exception as e:
    print(f"Erro inesperado: {e}")
    lyrics = "Erro na extração"
```

## 📁 **Entregáveis**

### **1. Código Fonte**
- Arquivo Python principal: `extrator_letras_[seu_nome].py`
- Código comentado e documentado
- README.md com instruções de uso

### **2. Dados Extraídos**
- Arquivo CSV com as músicas extraídas


## 🚀 **Exemplo de Saída Esperada**

```csv
url,title,artist,lyrics,views,composition,extracted_at
https://www.letras.mus.br/joao-gomes/...,"Eu Tenho a Senha","João Gomes","Eu tenho a senha do seu coração...","2.5M","João Gomes","2025-09-03 11:10:00"
```

## 📞 **Suporte e Dúvidas**

Para dúvidas sobre implementação, consulte:
- Documentação oficial do Selenium
- Tutoriais de BeautifulSoup
- Exemplos de web scraping em Python
- Fóruns de programação (Stack Overflow)

---

## 📚 **Recursos Adicionais**

### **Checklist de implementação**
- [ ] Configuração do ambiente (instalação de dependências)
- [ ] Configuração do navegador
- [ ] Implementação da busca
- [ ] Extração da lista de músicas
- [ ] Extração de detalhes individuais
- [ ] Tratamento de erros
- [ ] Salvamento em CSV
- [ ] Testes e validação
- [ ] Documentação

### **Dicas de Debugging:**
```python
# 1. Use prints para acompanhar o progresso
print(f"Processando música: {song_title}")


# 2. Teste com poucas músicas primeiro
songs_list = songs_list[:3]  # Apenas 3 músicas para teste
```

**Boa sorte e bom desenvolvimento! 🎵🐍**
