# 🚀 Projeto 4: Desenvolvimento de API com FastAPI

## 📋 **Objetivo da Tarefa**

Desenvolver uma **API REST** usando **FastAPI** que sirva dados de uma base de dados criada ou obtida pelo aluno. A API deve ter pelo menos **2 endpoints** funcionais: um **básico** e um **médio**, seguindo os conceitos ensinados na **aula_14**.

**⚠️ IMPORTANTE: Esta tarefa vale 0,5 pontos na nota final da A1**

## 🎯 **Competências a serem Desenvolvidas**

- **Desenvolvimento de APIs**: Criação de endpoints REST com FastAPI
- **Manipulação de Dados**: Trabalhar com datasets reais ou simulados
- **Documentação Automática**: Utilizar a documentação automática do FastAPI
- **Estruturação de Projetos**: Organização de código e arquivos
- **Query Parameters e Path Parameters**: Diferentes formas de receber dados

## 🔧 **Tecnologias e Bibliotecas Obrigatórias**

### **Bibliotecas Principais:**
```python
# API Framework
from fastapi import FastAPI

# Manipulação de dados (se necessário)
import pandas as pd

# Para execução da API
import uvicorn

# Utilitários (se necessário)
import json
```

### **Instalação:**
```bash
pip install fastapi uvicorn pandas
```

## 📝 **Especificações Técnicas**

### **1. Base de Dados**

Você deve escolher **UMA** das opções abaixo:

#### **Opção A: Criar Dataset Próprio**
- Criar um dataset com pelo menos **50 registros**
- Salvar em formato CSV ou JSON
- Exemplos de temas:
  - Lista de filmes com nota, gênero, ano
  - Cardápio de restaurante com preços e categorias
  - Lista de livros com autor, páginas, gênero
  - Produtos de loja com preço, categoria, estoque
  - Lista de cidades com população, estado, região

#### **Opção B: Usar Dataset da Internet**
- Baixar dataset de sites como:
  - **Kaggle** (https://www.kaggle.com/datasets)
  - **Data.gov** (https://www.data.gov/)
  - **GitHub Awesome Public Datasets**
  - **IBGE** (dados do Brasil)
- Dataset deve ter pelo menos **50 registros**
- Citar a fonte no arquivo referido.

### **2. Endpoints Obrigatórios**

#### **2.1 Endpoint Básico (Nível 1) - OBRIGATÓRIO**
**Listar todas as entradas da tabela/dataset:**

```python
@app.get("/")
def home():
    """Endpoint básico que retorna informações sobre a API"""
    return {
        "projeto": "Minha API",
        "autor": "Seu Nome",
        "descricao": "API para servir dados de [seu dataset]",
        "total_registros": len(seus_dados)
    }

@app.get("/dados")
def listar_todos():
    """
    Endpoint BÁSICO: Retorna TODAS as entradas do dataset
    Este é o endpoint principal que lista todos os dados
    """
    return seus_dados  # Retorna todos os dados da tabela
```

#### **2.2 Endpoint Intermediário (Nível 2) - OBRIGATÓRIO**
**Busca por ID ou filtro por variável (escolha UMA das opções):**

**Opção A: Busca por ID (Path Parameter)**
```python
@app.get("/dados/{item_id}")
def buscar_por_id(item_id: int):
    """
    Endpoint INTERMEDIÁRIO: Busca um registro específico pelo ID
    Exemplo: /dados/5 - retorna o item com ID = 5
    """
    return {"item": "Info do item filtrado"}
```

**Opção B: Busca por categoria/campo (Path Parameter)**
```python
@app.get("/categoria/{categoria}")
def buscar_por_categoria(categoria: str):
    """
    Endpoint INTERMEDIÁRIO: Filtra dados por uma categoria específica
    Exemplo: /categoria/pizza - retorna todos os itens da categoria "pizza"
    """
    # Filtrar dados por categoria
    return {"item": "Info do item filtrado"}
```

**Opção C: Busca com Query Parameters**
```python
@app.get("/buscar")
def buscar_com_filtros(nome: str = None, categoria: str = None, limite: int = 10):
    """
    Endpoint INTERMEDIÁRIO: Busca com parâmetros de query
    Exemplo: /buscar?nome=pizza&limite=5
    Exemplo: /buscar?categoria=comida
    """
    
    return {
        "filtros": {"nome": nome, "categoria": categoria, "limite": limite},
        "resultados": resultados,
        "total": len(resultados)
    }
```

### **3. Estrutura do Projeto**

```
projeto4/
├── README.md                 # Este arquivo
├── main.py                   # Código da API
├── dados/                    # Pasta para os dados
│   ├── dataset.csv          # Seus dados (pode ser em outro formato além de CSV)
│   └── fonte.txt            # Fonte dos dados (se aplicável)
└── requirements.txt        # Dependências
```

### **4. Requisitos Técnicos**

#### **4.1 Código (main.py)**
- Usar **FastAPI** conforme ensinado na aula_14
- Código **comentado** e **documentado**
- Seguir estrutura do `basico.py`
- Incluir docstrings nos endpoints

#### **4.2 Dados**
- Carregar dados no início da aplicação
- Tratar erros de carregamento
- Validar formato dos dados

#### **4.3 Documentação**
- README.md completo (este arquivo)

## 📁 **Entregáveis**

**Atenção**: Todos os trabalhos devem ser entregues em um repositório chamado "Minha_Primeira_API", no Github! 

### **1. Obrigatórios**
- [ ] `main.py` - Código da API funcionando
- [ ] `README.md` - Documentação completa
- [ ] `requirements.txt` - Lista de dependências
- [ ] `dados/` - Dataset utilizado

### **2. Opcionais (pontos extras)**
- [ ] `exemplos/teste_api.py` - Script de teste (+0,05)
- [ ] Endpoint adicional criativo (+0,05)

## ✅ **Exemplos de Datasets e APIs**

### **Exemplo 1: Cardápio de Restaurante**
```python
dados_cardapio = [
    {"id": 1, "nome": "Pizza Margherita", "preco": 25.90, "categoria": "Pizza"},
    {"id": 2, "nome": "Hambúrguer Artesanal", "preco": 18.50, "categoria": "Lanches"},
    {"id": 3, "nome": "Salada Caesar", "preco": 15.00, "categoria": "Saladas"},
    # ... mais 47 registros
]

# Endpoints implementados:
# GET / - Informações da API
# GET /dados - BÁSICO: Lista TODOS os pratos do cardápio
# GET /dados/{id} - INTERMEDIÁRIO: Busca prato por ID específico
# OU
# GET /categoria/{categoria} - INTERMEDIÁRIO: Todos os pratos de uma categoria
# OU  
# GET /buscar?nome=pizza&limite=5 - INTERMEDIÁRIO: Busca com filtros
```

### **Exemplo 2: Lista de Filmes**
```python
dados_filmes = [
    {"id": 1, "nome": "Avatar", "ano": 2009, "categoria": "Ficção", "nota": 7.8},
    {"id": 2, "nome": "Titanic", "ano": 1997, "categoria": "Romance", "nota": 7.9},
    {"id": 3, "nome": "Vingadores", "ano": 2012, "categoria": "Ação", "nota": 8.0},
    # ... mais 47 registros
]

# Endpoints implementados:
# GET / - Informações da API  
# GET /dados - BÁSICO: Lista TODOS os filmes
# GET /dados/{id} - INTERMEDIÁRIO: Busca filme por ID
# OU
# GET /categoria/{categoria} - INTERMEDIÁRIO: Filmes por gênero
# OU
# GET /buscar?nome=avatar&categoria=ficção - INTERMEDIÁRIO: Busca com filtros
```

## 💡 **Dicas e Sugestões**

### **1. Começando do Zero**
```python
from fastapi import FastAPI
import pandas as pd

# Carregar dados
dados = pd.read_csv("dados/meu_dataset.csv")
dados_dict = dados.to_dict("records")

app = FastAPI(title="Minha API")

@app.get("/")
def home():
    return {"mensagem": "API funcionando!"}
```

### **2. Testando Localmente**
- Use `uvicorn main:app --reload` para desenvolvimento
- Ou... `python main.py`
- Acesse http://localhost:8000/docs para testar

### **3. Sources de Inspiração**
- **Filmes**: IMDB, TMDB
- **Música**: Spotify Charts, Last.fm
- **Comida**: Receitas, restaurantes
- **Esportes**: Times, jogadores, estatísticas
- **Geografia**: Cidades, países, clima
- **E-commerce**: Produtos, preços, categorias

## 📞 **Suporte e Dúvidas**

### **Recursos de Ajuda:**
- Revisitar `aula_14/basico.py`
- Documentação FastAPI: https://fastapi.tiangolo.com/

### **Dúvidas Comuns:**
1. **"API não executa?"** → Verifique se está na pasta correta
2. **"Endpoint não funciona?"** → Teste na documentação automática
3. **"Dados muito grandes?"** → Limite a 50-200 registros

## 🏆 **Exemplos de Projetos Criativos**

- **API de Receitas**: buscar por ingrediente, tempo de preparo
- **API de Cidades**: dados demográficos, clima, CEP
- **API de Livros**: buscar por autor, gênero, ano
- **API de Pokémon**: stats, tipos, evoluções
- **API de Times**: jogadores, estatísticas, histórico

---

## 📅 **Cronograma Sugerido**

- **Dia 1**: Escolher dataset e configurar ambiente
- **Dia 2**: Implementar endpoint básico
- **Dia 3**: Implementar endpoint médio
- **Dia 4**: Documentação e testes finais

---

**Boa sorte e bom desenvolvimento! 🚀🐍**

*Lembre-se: O importante é fazer funcionar primeiro, depois melhorar!*
