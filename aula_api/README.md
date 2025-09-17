# Aula de FastAPI: Criando APIs Modernas e Rápidas

Este diretório contém uma aula completa e prática sobre FastAPI, demonstrando como criar APIs RESTful modernas com Python.

## 🚀 O que é FastAPI?

FastAPI é um framework moderno para criar APIs em Python que oferece:
- **Performance**: Uma das APIs Python mais rápidas disponíveis
- **Desenvolvimento Rápido**: Documentação automática e validação de dados
- **Baseado em Padrões**: Baseado em OpenAPI (Swagger) e JSON Schema
- **Assíncrono**: Suporte nativo a async/await para melhor performance
- **Validação Automática**: Validação automática de tipos com Pydantic

## 📋 Pré-requisitos

- Python 3.12+
- Conhecimento básico de Python
- Familiaridade com conceitos de APIs REST

## 🛠️ Instalação das Dependências

```bash
# Instalar FastAPI e servidor ASGI
pip install fastapi uvicorn[standard]

# Dependências adicionais para validação
pip install pydantic[email]

# Ou instalar tudo de uma vez
pip install -r ../requirements.txt
```

## 📁 Estrutura da Aula

### `fastapi_completo.py`
Arquivo principal contendo uma API completa com:

- **Autenticação**: Sistema de login/logout com tokens JWT
- **CRUD de Usuários**: Gerenciamento completo de usuários
- **CRUD de Tarefas**: Sistema de tarefas com prioridades
- **Validação de Dados**: Modelos Pydantic com validações
- **Middleware**: Logging e tratamento de erros
- **Documentação**: Endpoints bem documentados
- **Estatísticas**: Métricas e relatórios

## 🚀 Como Executar

### Opção 1: Execução Direta
```bash
cd aula_api
python fastapi_completo.py
```

### Opção 2: Usando Uvicorn
```bash
cd aula_api
uvicorn fastapi_completo:app --reload --host 0.0.0.0 --port 8000
```

### Opção 3: Execução em Background
```bash
cd aula_api
uvicorn fastapi_completo:app --reload --host 0.0.0.0 --port 8000 &
```

## 🌐 Acessando a API

Após executar, a API estará disponível em:

- **API Base**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## 🔑 Credenciais de Teste

Para testar a autenticação, use:
- **Email**: admin@sistema.com
- **Senha**: 123456

## 📚 Endpoints Principais

### Autenticação
- `POST /auth/login` - Fazer login
- `POST /auth/logout` - Fazer logout

### Usuários
- `GET /usuarios` - Listar usuários
- `POST /usuarios` - Criar usuário
- `GET /usuarios/{id}` - Obter usuário específico
- `PUT /usuarios/{id}` - Atualizar usuário
- `DELETE /usuarios/{id}` - Remover usuário

### Tarefas
- `GET /tarefas` - Listar tarefas
- `POST /tarefas` - Criar tarefa
- `GET /tarefas/{id}` - Obter tarefa específica
- `PUT /tarefas/{id}` - Atualizar tarefa
- `PATCH /tarefas/{id}/concluir` - Concluir tarefa
- `DELETE /tarefas/{id}` - Remover tarefa

### Sistema
- `GET /` - Informações da API
- `GET /health` - Status da API
- `GET /estatisticas` - Estatísticas do usuário
- `POST /sistema/limpar-sessoes` - Limpeza automática

## 🧪 Testando a API

### 1. Login e Obter Token
```bash
curl -X POST "http://localhost:8000/auth/login" \
     -H "Content-Type: application/json" \
     -d '{"email": "admin@sistema.com", "senha": "123456"}'
```

### 2. Criar Usuário (sem autenticação)
```bash
curl -X POST "http://localhost:8000/usuarios" \
     -H "Content-Type: application/json" \
     -d '{"nome": "João Silva", "email": "joao@email.com", "idade": 30, "senha": "123456"}'
```

### 3. Criar Tarefa (com autenticação)
```bash
# Substitua TOKEN_AQUI pelo token obtido no login
curl -X POST "http://localhost:8000/tarefas" \
     -H "Content-Type: application/json" \
     -H "Authorization: Bearer TOKEN_AQUI" \
     -d '{"titulo": "Implementar API", "descricao": "Criar endpoints REST", "prioridade": "alta"}'
```

## 🔍 Recursos Avançados Demonstrados

### Validação de Dados
- Validação de tipos com Pydantic
- Validações customizadas
- Validação de emails
- Regex para prioridades

### Autenticação e Autorização
- Sistema de tokens
- Verificação de permissões
- Proteção de endpoints

### Middleware
- Logging de requisições
- Headers customizados
- Tratamento de erros

### Tratamento de Erros
- Handlers personalizados
- Códigos de status apropriados
- Mensagens de erro informativas

## 📖 Conceitos Aprendidos

1. **FastAPI Basics**: Criação de aplicação e configuração
2. **Modelos Pydantic**: Validação e serialização de dados
3. **Endpoints REST**: CRUD completo com diferentes métodos HTTP
4. **Autenticação**: Sistema de tokens e dependências
5. **Middleware**: Interceptação e processamento de requisições
6. **Tratamento de Erros**: Handlers personalizados e códigos de status
7. **Documentação**: Geração automática de documentação da API
8. **Validação**: Validação automática de entrada e saída
9. **Async/Await**: Programação assíncrona para melhor performance
10. **CORS**: Configuração para requisições cross-origin

## 🚀 Próximos Passos

Após dominar esta aula, você pode explorar:

- **Banco de Dados**: Integração com SQLAlchemy ou databases
- **Cache**: Redis para melhorar performance
- **Testes**: Pytest com TestClient
- **Deploy**: Docker, Heroku, AWS, etc.
- **Monitoramento**: Logs estruturados e métricas
- **Rate Limiting**: Controle de taxa de requisições
- **WebSockets**: Comunicação em tempo real

## 💡 Dicas de Desenvolvimento

- Use a documentação automática (`/docs`) para testar endpoints
- Implemente validações robustas com Pydantic
- Sempre trate erros de forma apropriada
- Use tipos de dados apropriados para cada campo
- Documente bem seus endpoints com docstrings
- Implemente logging para debugging
- Teste todos os cenários de erro

## 🐛 Solução de Problemas

### Erro de Porta em Uso
```bash
# Mudar porta
uvicorn fastapi_completo:app --reload --port 8001
```

### Erro de Dependências
```bash
# Atualizar pip
pip install --upgrade pip

# Reinstalar dependências
pip install -r ../requirements.txt
```

### Erro de CORS
- Verifique se o middleware CORS está configurado
- Confirme as origens permitidas

## 📚 Recursos Adicionais

- [Documentação Oficial FastAPI](https://fastapi.tiangolo.com/)
- [Tutorial FastAPI](https://fastapi.tiangolo.com/tutorial/)
- [Pydantic Documentation](https://pydantic-docs.helpmanual.io/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

---

**Bom estudo! 🚀**

Crie APIs modernas, rápidas e bem documentadas com FastAPI!









