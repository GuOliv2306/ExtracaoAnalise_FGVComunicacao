# 🚀 FastAPI - Guia Completo

## 📚 Índice
1. [Introdução ao FastAPI](#introdução-ao-fastapi)
2. [Conceitos Básicos](#conceitos-básicos)
3. [Níveis de Aprendizado](#níveis-de-aprendizado)
4. [Pydantic - Validação de Dados](#pydantic---validação-de-dados)
5. [Conceitos Avançados](#conceitos-avançados)
6. [Boas Práticas](#boas-práticas)
7. [Executando os Exemplos](#executando-os-exemplos)

---

## 🎯 Introdução ao FastAPI

**FastAPI** é um framework moderno e rápido para construir APIs web com Python. Ele é baseado em:

- **Python 3.6+** com type hints
- **Pydantic** para validação de dados
- **Starlette** para performance
- **OpenAPI** para documentação automática

### Por que usar FastAPI?

✅ **Performance**: Uma das APIs mais rápidas disponíveis  
✅ **Fácil de usar**: Sintaxe intuitiva e clara  
✅ **Documentação automática**: Swagger UI e ReDoc integrados  
✅ **Validação automática**: Baseada em type hints  
✅ **Async/await**: Suporte nativo para programação assíncrona  
✅ **Padrões modernos**: Baseado em padrões abertos (OpenAPI, JSON Schema)  

---

## 🔧 Conceitos Básicos

### 1. O que é um Decorador `@app`?

```python
@app.get("/")
def hello_world():
    return {"mensagem": "Hello World!"}
```

O `@app.get()` é um **decorador** que:
- Define que a função responde a requisições **GET**
- Mapeia a URL `/` para a função `hello_world()`
- Automaticamente converte o retorno para JSON
- Gera documentação automática

### 2. Métodos HTTP

| Método | Uso | Exemplo |
|--------|-----|---------|
| `GET` | Buscar dados | `@app.get("/usuarios")` |
| `POST` | Criar dados | `@app.post("/usuarios")` |
| `PUT` | Atualizar dados | `@app.put("/usuarios/{id}")` |
| `DELETE` | Remover dados | `@app.delete("/usuarios/{id}")` |

### 3. Tipos de Parâmetros

#### Path Parameters (na URL)
```python
@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int):
    return {"id": usuario_id}
```

#### Query Parameters (após o ?)
```python
@app.get("/usuarios")
def listar_usuarios(skip: int = 0, limit: int = 10):
    return {"skip": skip, "limit": limit}
```

#### Request Body (dados enviados)
```python
@app.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate):
    return {"usuario": usuario}
```

---

## 📈 Níveis de Aprendizado

### 🟢 Nível Básico (`basico.py`)

**Conceitos abordados:**
- Criação de endpoints simples
- Parâmetros de URL e query
- Retorno de dados JSON
- Execução básica com uvicorn

**Exemplo:**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello_world():
    return {"mensagem": "Hello World!"}
```

### 🟡 Nível Intermediário (`medio.py`)

**Conceitos abordados:**
- Diferentes métodos HTTP (GET, POST, PUT, DELETE)
- Trabalhando com dicionários como banco de dados
- Tratamento de erros com HTTPException
- Funções assíncronas (async/await)
- Query parameters e filtros
- Middleware personalizado
- Responses customizadas

**Exemplo:**
```python
@app.post("/usuarios")
def criar_usuario(nome: str, email: str, idade: int):
    novo_usuario = {
        "id": len(usuarios_db) + 1,
        "nome": nome,
        "email": email,
        "idade": idade
    }
    usuarios_db[novo_usuario["id"]] = novo_usuario
    return {"mensagem": "Usuário criado", "usuario": novo_usuario}
```

### 🔴 Nível Avançado (`avancado.py`)

**Conceitos abordados:**
- Modelos Pydantic para validação
- Sistema de autenticação
- Background tasks
- CORS middleware
- Relatórios e métricas
- Validação avançada de dados
- Paginação e filtros complexos

---

## 🛡️ Pydantic - Validação de Dados

### O que é Pydantic?

**Pydantic** é uma biblioteca que usa type hints do Python para validação de dados. Ela garante que os dados recebidos estejam no formato correto.

### Exemplo Básico

```python
from pydantic import BaseModel, EmailStr, Field

class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    idade: int = Field(..., ge=0, le=120)
    ativo: bool = Field(default=True)
```

### Validação Automática

```python
class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6)
    
    @validator('senha')
    def validar_senha(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve ter maiúscula')
        return v
```

### Vantagens do Pydantic

✅ **Validação automática** de tipos  
✅ **Mensagens de erro claras**  
✅ **Documentação automática**  
✅ **Serialização/deserialização** JSON  
✅ **Validação customizada** com validators  

---

## ⚡ Conceitos Avançados

### 1. Async/Await

```python
@app.get("/async-exemplo")
async def exemplo_async():
    await asyncio.sleep(1)  # Operação não-bloqueante
    return {"mensagem": "Processado assincronamente"}
```

**Por que usar async?**
- Melhor performance para operações I/O
- Suporte a muitas conexões simultâneas
- Não bloqueia o servidor durante operações lentas

### 2. Background Tasks

```python
@app.post("/pedidos")
async def criar_pedido(pedido: PedidoCreate, background_tasks: BackgroundTasks):
    # Processa imediatamente
    novo_pedido = criar_pedido_db(pedido)
    
    # Adiciona tarefa em background
    background_tasks.add_task(processar_pedido, novo_pedido.id)
    
    return novo_pedido
```

### 3. Autenticação

```python
from fastapi.security import HTTPBearer

security = HTTPBearer()

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != "token-secreto":
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"usuario": "admin"}

@app.get("/protegido")
def endpoint_protegido(current_user: dict = Depends(verificar_token)):
    return {"mensagem": "Acesso autorizado"}
```

### 4. Middleware

```python
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Tempo: {process_time:.4f}s")
    return response
```

---

## 🎯 Boas Práticas

### 1. Estrutura de Projeto

```
projeto/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   └── usuario.py
│   ├── routers/
│   │   ├── __init__.py
│   │   └── usuarios.py
│   └── database.py
├── requirements.txt
└── README.md
```

### 2. Separação de Responsabilidades

```python
# models/usuario.py
class Usuario(BaseModel):
    id: int
    nome: str
    email: str

# routers/usuarios.py
from fastapi import APIRouter
router = APIRouter(prefix="/usuarios", tags=["usuarios"])

@router.get("/")
def listar_usuarios():
    return {"usuarios": []}

# main.py
from routers.usuarios import router as usuarios_router
app.include_router(usuarios_router)
```

### 3. Tratamento de Erros

```python
from fastapi import HTTPException

@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int):
    if usuario_id not in usuarios_db:
        raise HTTPException(
            status_code=404,
            detail="Usuário não encontrado"
        )
    return usuarios_db[usuario_id]
```

### 4. Validação de Dados

```python
class UsuarioCreate(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    idade: int = Field(..., ge=0, le=120)
    
    @validator('nome')
    def nome_deve_ter_espaco(cls, v):
        if ' ' not in v:
            raise ValueError('Nome deve ter pelo menos um espaço')
        return v.title()
```

---

## 🚀 Executando os Exemplos

### 1. Instalação

```bash
pip install fastapi uvicorn
pip install email-validator  # Para EmailStr
```

### 2. Executando os Arquivos

```bash
# Básico
uvicorn basico:app --reload

# Intermediário
uvicorn medio:app --reload

# Avançado
uvicorn avancado:app --reload
```

### 3. Acessando a API

- **API**: http://localhost:8000
- **Documentação Swagger**: http://localhost:8000/docs
- **Documentação ReDoc**: http://localhost:8000/redoc

### 4. Testando com curl

```bash
# GET simples
curl http://localhost:8000/

# POST com dados
curl -X POST "http://localhost:8000/usuarios" \
     -H "Content-Type: application/json" \
     -d '{"nome": "João", "email": "joao@email.com", "idade": 30}'

# Com autenticação
curl -X GET "http://localhost:8000/produtos" \
     -H "Authorization: Bearer token-secreto-123"
```

---

## 📚 Recursos Adicionais

### Documentação Oficial
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Pydantic Docs](https://pydantic-docs.helpmanual.io/)

### Tutoriais Recomendados
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

### Extensões Úteis
- **SQLAlchemy**: ORM para banco de dados
- **Alembic**: Migrações de banco
- **Redis**: Cache e sessões
- **Celery**: Background tasks
- **JWT**: Autenticação com tokens

---

## 🎉 Conclusão

FastAPI é uma ferramenta poderosa que combina:
- **Simplicidade** para começar
- **Poder** para aplicações complexas
- **Performance** para produção
- **Documentação** automática
- **Validação** robusta de dados

Comece com o `basico.py`, evolua para `medio.py` e domine o `avancado.py`. Em pouco tempo, você estará criando APIs profissionais e robustas!

**Lembre-se**: A prática leva à perfeição. Experimente, modifique os códigos e crie seus próprios endpoints! 🚀

