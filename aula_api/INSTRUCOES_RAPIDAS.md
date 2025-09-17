# 🚀 INSTRUÇÕES RÁPIDAS - FastAPI

## ⚡ Início Rápido

### 1. Instalar Dependências
```bash
cd aula_api
pip install -r requirements.txt
```

### 2. Executar API Simples (Recomendado para iniciantes)
```bash
python exemplo_simples.py
```
- Acesse: http://localhost:8000
- Documentação: http://localhost:8000/docs

### 3. Executar API Completa (Avançado)
```bash
python fastapi_completo.py
```
- Acesse: http://localhost:8000
- Documentação: http://localhost:8000/docs

## 🔧 Comandos Alternativos

### Usando Uvicorn
```bash
# API Simples
uvicorn exemplo_simples:app --reload --port 8000

# API Completa
uvicorn fastapi_completo:app --reload --port 8000
```

### Mudar Porta
```bash
uvicorn exemplo_simples:app --reload --port 8001
```

## 🧪 Testar APIs

### Teste Automático
```bash
python teste_rapido.py
```

### Teste Manual
```bash
# Testar endpoint raiz
curl http://localhost:8000/

# Listar produtos
curl http://localhost:8000/produtos

# Criar produto
curl -X POST "http://localhost:8000/produtos" \
     -H "Content-Type: application/json" \
     -d '{"nome": "Teste", "preco": 99.99, "categoria": "Teste"}'
```

## 📚 Ordem de Estudo

1. **Comece com**: `exemplo_simples.py`
2. **Avançado**: `fastapi_completo.py`
3. **Pratique**: `exercicios.py`
4. **Teste**: `teste_rapido.py`

## 🌐 URLs Importantes

- **API Base**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔑 Credenciais de Teste (API Completa)

- **Email**: admin@sistema.com
- **Senha**: 123456

## 🛠️ Solução de Problemas

### Porta em Uso
```bash
# Mudar porta
uvicorn exemplo_simples:app --reload --port 8001
```

### Dependências
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Servidor Não Inicia
- Verifique se Python 3.12+ está instalado
- Verifique se as dependências foram instaladas
- Verifique se a porta 8000 está livre

## 📖 Próximos Passos

1. Estude o código dos exemplos
2. Complete os exercícios práticos
3. Experimente modificando os endpoints
4. Adicione novas funcionalidades
5. Implemente um banco de dados real
6. Adicione testes automatizados

---

**💡 Dica**: Use sempre a documentação automática (`/docs`) para testar os endpoints!









