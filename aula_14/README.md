# 🚀 Aula 14 - FastAPI

Esta pasta contém uma aula completa e didática sobre FastAPI, dividida em três níveis de complexidade.

## 📁 Arquivos

- **`basico.py`** - Conceitos básicos do FastAPI
- **`medio.py`** - Conceitos intermediários com dicionários e async
- **`avancado.py`** - Conceitos avançados com Pydantic e autenticação
- **`API.md`** - Documentação completa sobre FastAPI
- **`requirements.txt`** - Dependências necessárias

## 🚀 Como Começar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar os Exemplos

```bash
# Nível Básico
uvicorn basico:app --reload

# Nível Intermediário
uvicorn medio:app --reload

# Nível Avançado
uvicorn avancado:app --reload
```

### 3. Acessar a Documentação

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 Ordem de Estudo

1. **Comece com `basico.py`** - Aprenda os conceitos fundamentais
2. **Evolua para `medio.py`** - Entenda dicionários e async
3. **Domine `avancado.py`** - Aprenda Pydantic e autenticação
4. **Leia `API.md`** - Consolide todo o conhecimento

## 💡 Dicas

- Execute cada arquivo separadamente
- Experimente modificar os códigos
- Use a documentação automática (Swagger)
- Leia os comentários no código
