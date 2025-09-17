# ===========================================
# FASTAPI - NÍVEL AVANÇADO
# ===========================================
# Este arquivo mostra conceitos avançados do FastAPI
# Incluindo Pydantic, validação de dados, autenticação, e muito mais

from fastapi import FastAPI, HTTPException, Depends, status, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import List, Optional, Dict, Any
from datetime import datetime, date
from enum import Enum
import asyncio
import json

# ===========================================
# 1. MODELOS PYDANTIC - VALIDAÇÃO DE DADOS
# ===========================================

# Enum para categorias
class CategoriaProduto(str, Enum):
    ELETRONICOS = "Eletrônicos"
    LIVROS = "Livros"
    ROUPAS = "Roupas"
    CASA = "Casa"
    ESPORTES = "Esportes"

# Modelo base para usuário
class UsuarioBase(BaseModel):
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    idade: int = Field(..., ge=0, le=120, description="Idade entre 0 e 120 anos")
    ativo: bool = Field(default=True, description="Status ativo do usuário")

# Modelo para criar usuário (herda de UsuarioBase)
class UsuarioCreate(UsuarioBase):
    senha: str = Field(..., min_length=6, description="Senha com pelo menos 6 caracteres")
    
    @field_validator('senha')
    @classmethod
    def validar_senha(cls, v):
        if len(v) < 6:
            raise ValueError('Senha deve ter pelo menos 6 caracteres')
        if not any(c.isupper() for c in v):
            raise ValueError('Senha deve ter pelo menos uma letra maiúscula')
        if not any(c.islower() for c in v):
            raise ValueError('Senha deve ter pelo menos uma letra minúscula')
        return v

# Modelo para resposta (sem senha)
class UsuarioResponse(UsuarioBase):
    id: int
    data_criacao: datetime
    
    class Config:
        # Permite usar objetos ORM (como SQLAlchemy)
        orm_mode = True

# Modelo para produto
class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, max_length=200)
    preco: float = Field(..., gt=0, description="Preço deve ser maior que zero")
    categoria: CategoriaProduto
    descricao: Optional[str] = Field(None, max_length=1000)
    estoque: int = Field(default=0, ge=0)

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int
    data_criacao: datetime
    
    class Config:
        orm_mode = True

# Modelo para pedido
class ItemPedido(BaseModel):
    produto_id: int
    quantidade: int = Field(..., gt=0)
    preco_unitario: float = Field(..., gt=0)

class PedidoCreate(BaseModel):
    itens: List[ItemPedido] = Field(..., min_items=1)
    observacoes: Optional[str] = Field(None, max_length=500)

class PedidoResponse(BaseModel):
    id: int
    itens: List[ItemPedido]
    total: float
    data_criacao: datetime
    status: str

# ===========================================
# 2. SIMULAÇÃO DE BANCO DE DADOS
# ===========================================

# Em uma aplicação real, você usaria um banco de dados real
usuarios_db: Dict[int, UsuarioResponse] = {}
produtos_db: Dict[int, ProdutoResponse] = {}
pedidos_db: Dict[int, PedidoResponse] = {}

# Contadores para IDs
usuario_counter = 0
produto_counter = 0
pedido_counter = 0

# ===========================================
# 3. CONFIGURAÇÃO DA APLICAÇÃO
# ===========================================

app = FastAPI(
    title="API Avançada",
    description="API com conceitos avançados do FastAPI",
    version="2.0.0",
    docs_url="/documentacao",  # URL customizada para docs
    redoc_url="/redoc"  # URL customizada para ReDoc
)

# Configuração de CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique domínios específicos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===========================================
# 4. SISTEMA DE AUTENTICAÇÃO SIMPLES
# ===========================================

# Simulando um sistema de autenticação básico
security = HTTPBearer()

def verificar_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Função para verificar se o token é válido
    Em uma aplicação real, você validaria contra um banco de dados
    """
    token = credentials.credentials
    
    # Simulando validação de token
    if token != "token-secreto-123":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return {"usuario": "admin", "token": token}

# ===========================================
# 5. ENDPOINTS COM VALIDAÇÃO PYDANTIC
# ===========================================

@app.post("/usuarios", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
async def criar_usuario(usuario: UsuarioCreate):
    """
    Cria um novo usuário com validação completa
    """
    global usuario_counter
    usuario_counter += 1
    
    # Simulando hash da senha (em produção, use bcrypt ou similar)
    senha_hash = f"hash_{usuario.senha}"
    
    novo_usuario = UsuarioResponse(
        id=usuario_counter,
        nome=usuario.nome,
        email=usuario.email,
        idade=usuario.idade,
        ativo=usuario.ativo,
        data_criacao=datetime.now()
    )
    
    usuarios_db[usuario_counter] = novo_usuario
    
    return novo_usuario

@app.get("/usuarios", response_model=List[UsuarioResponse])
async def listar_usuarios(skip: int = 0, limit: int = 10, ativo: Optional[bool] = None):
    """
    Lista usuários com paginação e filtros
    """
    usuarios = list(usuarios_db.values())
    
    # Aplicar filtro de status ativo
    if ativo is not None:
        usuarios = [u for u in usuarios if u.ativo == ativo]
    
    # Aplicar paginação
    return usuarios[skip:skip + limit]

@app.get("/usuarios/{usuario_id}", response_model=UsuarioResponse)
async def buscar_usuario(usuario_id: int):
    """
    Busca um usuário específico
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return usuarios_db[usuario_id]

# ===========================================
# 6. ENDPOINTS DE PRODUTOS
# ===========================================

@app.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED)
async def criar_produto(produto: ProdutoCreate, current_user: dict = Depends(verificar_token)):
    """
    Cria um novo produto (requer autenticação)
    """
    global produto_counter
    produto_counter += 1
    
    novo_produto = ProdutoResponse(
        id=produto_counter,
        nome=produto.nome,
        preco=produto.preco,
        categoria=produto.categoria,
        descricao=produto.descricao,
        estoque=produto.estoque,
        data_criacao=datetime.now()
    )
    
    produtos_db[produto_counter] = novo_produto
    
    return novo_produto

@app.get("/produtos", response_model=List[ProdutoResponse])
async def listar_produtos(
    categoria: Optional[CategoriaProduto] = None,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None,
    skip: int = 0,
    limit: int = 10
):
    """
    Lista produtos com filtros avançados
    """
    produtos = list(produtos_db.values())
    
    # Aplicar filtros
    if categoria:
        produtos = [p for p in produtos if p.categoria == categoria]
    
    if preco_min is not None:
        produtos = [p for p in produtos if p.preco >= preco_min]
    
    if preco_max is not None:
        produtos = [p for p in produtos if p.preco <= preco_max]
    
    return produtos[skip:skip + limit]

# ===========================================
# 7. SISTEMA DE PEDIDOS
# ===========================================

@app.post("/pedidos", response_model=PedidoResponse, status_code=status.HTTP_201_CREATED)
async def criar_pedido(pedido: PedidoCreate, background_tasks: BackgroundTasks):
    """
    Cria um novo pedido com processamento em background
    """
    global pedido_counter
    pedido_counter += 1
    
    # Validar se todos os produtos existem
    for item in pedido.itens:
        if item.produto_id not in produtos_db:
            raise HTTPException(
                status_code=400, 
                detail=f"Produto com ID {item.produto_id} não encontrado"
            )
    
    # Calcular total
    total = 0
    for item in pedido.itens:
        produto = produtos_db[item.produto_id]
        total += item.preco_unitario * item.quantidade
    
    # Criar pedido
    novo_pedido = PedidoResponse(
        id=pedido_counter,
        itens=pedido.itens,
        total=total,
        data_criacao=datetime.now(),
        status="Pendente"
    )
    
    pedidos_db[pedido_counter] = novo_pedido
    
    # Adicionar tarefa em background para processar o pedido
    background_tasks.add_task(processar_pedido, pedido_counter)
    
    return novo_pedido

async def processar_pedido(pedido_id: int):
    """
    Função executada em background para processar pedidos
    """
    await asyncio.sleep(5)  # Simula processamento
    
    if pedido_id in pedidos_db:
        pedidos_db[pedido_id].status = "Processado"
        print(f"Pedido {pedido_id} processado com sucesso!")

# ===========================================
# 8. ENDPOINTS DE RELATÓRIOS E ESTATÍSTICAS
# ===========================================

@app.get("/relatorios/vendas")
async def relatorio_vendas(
    data_inicio: Optional[date] = None,
    data_fim: Optional[date] = None,
    current_user: dict = Depends(verificar_token)
):
    """
    Gera relatório de vendas (requer autenticação)
    """
    pedidos = list(pedidos_db.values())
    
    # Filtrar por data se especificado
    if data_inicio:
        pedidos = [p for p in pedidos if p.data_criacao.date() >= data_inicio]
    
    if data_fim:
        pedidos = [p for p in pedidos if p.data_criacao.date() <= data_fim]
    
    # Calcular estatísticas
    total_vendas = sum(p.total for p in pedidos)
    total_pedidos = len(pedidos)
    ticket_medio = total_vendas / total_pedidos if total_pedidos > 0 else 0
    
    return {
        "periodo": {
            "inicio": data_inicio,
            "fim": data_fim
        },
        "resumo": {
            "total_vendas": total_vendas,
            "total_pedidos": total_pedidos,
            "ticket_medio": round(ticket_medio, 2)
        },
        "pedidos": pedidos
    }

# ===========================================
# 9. ENDPOINTS DE SAÚDE E MONITORAMENTO
# ===========================================

@app.get("/health")
async def health_check():
    """
    Endpoint para verificar a saúde da API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(),
        "version": "2.0.0"
    }

@app.get("/metrics")
async def metrics():
    """
    Endpoint para métricas básicas da API
    """
    return {
        "usuarios_cadastrados": len(usuarios_db),
        "produtos_cadastrados": len(produtos_db),
        "pedidos_realizados": len(pedidos_db),
        "timestamp": datetime.now()
    }

# ===========================================
# 10. MIDDLEWARE PERSONALIZADO
# ===========================================

@app.middleware("http")
async def add_process_time_header(request, call_next):
    """
    Middleware que adiciona header com tempo de processamento
    """
    start_time = datetime.now()
    response = await call_next(request)
    process_time = (datetime.now() - start_time).total_seconds()
    response.headers["X-Process-Time"] = str(process_time)
    return response

# ===========================================
# COMO EXECUTAR
# ===========================================
# uvicorn avancado:app --reload
# 
# Endpoints principais:
# - POST /usuarios - Criar usuário (com validação)
# - GET /usuarios - Listar usuários (com paginação)
# - POST /produtos - Criar produto (requer auth)
# - GET /produtos - Listar produtos (com filtros)
# - POST /pedidos - Criar pedido (com background tasks)
# - GET /relatorios/vendas - Relatório (requer auth)
# - GET /health - Status da API
# - GET /metrics - Métricas da API
#
# Documentação:
# - http://localhost:8000/documentacao (Swagger UI)
# - http://localhost:8000/redoc (ReDoc)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
