"""
EXEMPLO SIMPLES: FastAPI - Primeiros Passos

Este arquivo demonstra os conceitos básicos do FastAPI de forma simples e didática.
Ideal para quem está começando com o framework.

Autor: Matheus C. Pestana
Data: 2025
"""

from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

# =============================================================================
# CONFIGURAÇÃO BÁSICA
# =============================================================================

# Criando a aplicação FastAPI
app = FastAPI(
    title="API Simples - FastAPI",
    description="Uma API simples para aprender FastAPI",
    version="1.0.0"
)

# =============================================================================
# MODELOS SIMPLES (Pydantic)
# =============================================================================

class Produto(BaseModel):
    """Modelo para produtos"""
    nome: str = Field(..., min_length=1, max_length=100, description="Nome do produto")
    preco: float = Field(..., gt=0, description="Preço do produto (deve ser maior que 0)")
    categoria: str = Field(..., description="Categoria do produto")
    em_estoque: bool = Field(default=True, description="Se o produto está em estoque")
    
    class Config:
        """Configurações do modelo"""
        schema_extra = {
            "example": {
                "nome": "Notebook Dell",
                "preco": 2999.99,
                "categoria": "Eletrônicos",
                "em_estoque": True
            }
        }

class Mensagem(BaseModel):
    """Modelo para mensagens de resposta"""
    mensagem: str
    sucesso: bool = True

# =============================================================================
# BANCO DE DADOS SIMULADO
# =============================================================================

# Lista para armazenar produtos (simula um banco de dados)
produtos = [
    {
        "id": 1,
        "nome": "Notebook Dell Inspiron",
        "preco": 2999.99,
        "categoria": "Eletrônicos",
        "em_estoque": True
    },
    {
        "id": 2,
        "nome": "Mouse Wireless",
        "preco": 89.90,
        "categoria": "Acessórios",
        "em_estoque": True
    },
    {
        "id": 3,
        "nome": "Teclado Mecânico",
        "preco": 299.90,
        "categoria": "Acessórios",
        "em_estoque": False
    }
]

# Contador para IDs únicos
proximo_id = 4

# =============================================================================
# ENDPOINTS BÁSICOS
# =============================================================================

@app.get("/", tags=["Sistema"])
async def root():
    """
    Endpoint raiz - Bem-vindo à API
    """
    return {
        "mensagem": "Bem-vindo à API Simples de FastAPI!",
        "endpoints": [
            "/produtos",
            "/produtos/{id}",
            "/buscar",
            "/categorias"
        ],
        "documentacao": "/docs"
    }

@app.get("/produtos", response_model=List[dict], tags=["Produtos"])
async def listar_produtos(
    categoria: Optional[str] = Query(None, description="Filtrar por categoria"),
    em_estoque: Optional[bool] = Query(None, description="Filtrar por disponibilidade")
):
    """
    Lista todos os produtos com filtros opcionais
    
    - **categoria**: Filtrar produtos por categoria específica
    - **em_estoque**: Filtrar apenas produtos em estoque
    """
    resultado = produtos.copy()
    
    # Aplicar filtros se fornecidos
    if categoria:
        resultado = [p for p in resultado if p["categoria"].lower() == categoria.lower()]
    
    if em_estoque is not None:
        resultado = [p for p in resultado if p["em_estoque"] == em_estoque]
    
    return resultado

@app.get("/produtos/{produto_id}", response_model=dict, tags=["Produtos"])
async def obter_produto(produto_id: int = Path(..., ge=1, description="ID do produto")):
    """
    Obtém um produto específico pelo ID
    
    - **produto_id**: ID numérico do produto (deve ser >= 1)
    """
    # Buscar produto pelo ID
    for produto in produtos:
        if produto["id"] == produto_id:
            return produto
    
    # Se não encontrar, retornar erro 404
    raise HTTPException(status_code=404, detail=f"Produto com ID {produto_id} não encontrado")

@app.post("/produtos", response_model=dict, status_code=201, tags=["Produtos"])
async def criar_produto(produto: Produto):
    """
    Cria um novo produto
    
    - **produto**: Dados do produto a ser criado
    
    Retorna o produto criado com ID único
    """
    global proximo_id
    
    # Criar novo produto
    novo_produto = {
        "id": proximo_id,
        "nome": produto.nome,
        "preco": produto.preco,
        "categoria": produto.categoria,
        "em_estoque": produto.em_estoque
    }
    
    # Adicionar à lista
    produtos.append(novo_produto)
    proximo_id += 1
    
    return novo_produto

@app.put("/produtos/{produto_id}", response_model=dict, tags=["Produtos"])
async def atualizar_produto(
    produto_id: int = Path(..., ge=1, description="ID do produto"),
    produto: Produto = None
):
    """
    Atualiza um produto existente
    
    - **produto_id**: ID do produto a ser atualizado
    - **produto**: Novos dados do produto
    """
    # Buscar produto existente
    for i, p in enumerate(produtos):
        if p["id"] == produto_id:
            # Atualizar produto
            produtos[i] = {
                "id": produto_id,
                "nome": produto.nome,
                "preco": produto.preco,
                "categoria": produto.categoria,
                "em_estoque": produto.em_estoque
            }
            return produtos[i]
    
    # Se não encontrar, retornar erro 404
    raise HTTPException(status_code=404, detail=f"Produto com ID {produto_id} não encontrado")

@app.delete("/produtos/{produto_id}", response_model=Mensagem, tags=["Produtos"])
async def deletar_produto(produto_id: int = Path(..., ge=1, description="ID do produto")):
    """
    Remove um produto
    
    - **produto_id**: ID do produto a ser removido
    
    Retorna mensagem de confirmação
    """
    global produtos
    
    # Buscar e remover produto
    for i, produto in enumerate(produtos):
        if produto["id"] == produto_id:
            produtos.pop(i)
            return Mensagem(mensagem=f"Produto {produto_id} removido com sucesso")
    
    # Se não encontrar, retornar erro 404
    raise HTTPException(status_code=404, detail=f"Produto com ID {produto_id} não encontrado")

# =============================================================================
# ENDPOINTS COM PARÂMETROS DE QUERY
# =============================================================================

@app.get("/buscar", response_model=List[dict], tags=["Busca"])
async def buscar_produtos(
    q: str = Query(..., min_length=2, description="Termo de busca"),
    preco_min: Optional[float] = Query(None, ge=0, description="Preço mínimo"),
    preco_max: Optional[float] = Query(None, ge=0, description="Preço máximo")
):
    """
    Busca produtos por termo e filtros de preço
    
    - **q**: Termo de busca (mínimo 2 caracteres)
    - **preco_min**: Preço mínimo para filtrar
    - **preco_max**: Preço máximo para filtrar
    """
    resultado = []
    
    for produto in produtos:
        # Verificar se o termo de busca está no nome ou categoria
        if (q.lower() in produto["nome"].lower() or 
            q.lower() in produto["categoria"].lower()):
            
            # Aplicar filtros de preço
            if preco_min is not None and produto["preco"] < preco_min:
                continue
            if preco_max is not None and produto["preco"] > preco_max:
                continue
            
            resultado.append(produto)
    
    return resultado

@app.get("/categorias", response_model=List[str], tags=["Categorias"])
async def listar_categorias():
    """
    Lista todas as categorias únicas disponíveis
    """
    categorias = set()
    for produto in produtos:
        categorias.add(produto["categoria"])
    
    return sorted(list(categorias))

@app.get("/categorias/{categoria}", response_model=List[dict], tags=["Categorias"])
async def produtos_por_categoria(
    categoria: str = Path(..., description="Nome da categoria")
):
    """
    Lista produtos de uma categoria específica
    
    - **categoria**: Nome da categoria
    """
    resultado = []
    
    for produto in produtos:
        if produto["categoria"].lower() == categoria.lower():
            resultado.append(produto)
    
    if not resultado:
        raise HTTPException(
            status_code=404, 
            detail=f"Nenhum produto encontrado na categoria '{categoria}'"
        )
    
    return resultado

# =============================================================================
# ENDPOINTS DE ESTATÍSTICAS
# =============================================================================

@app.get("/estatisticas", tags=["Estatísticas"])
async def estatisticas():
    """
    Retorna estatísticas gerais dos produtos
    """
    total_produtos = len(produtos)
    produtos_em_estoque = len([p for p in produtos if p["em_estoque"]])
    produtos_sem_estoque = total_produtos - produtos_em_estoque
    
    # Calcular preço médio
    if total_produtos > 0:
        preco_medio = sum(p["preco"] for p in produtos) / total_produtos
    else:
        preco_medio = 0
    
    # Produto mais caro
    if produtos:
        produto_mais_caro = max(produtos, key=lambda x: x["preco"])
    else:
        produto_mais_caro = None
    
    return {
        "total_produtos": total_produtos,
        "em_estoque": produtos_em_estoque,
        "sem_estoque": produtos_sem_estoque,
        "preco_medio": round(preco_medio, 2),
        "produto_mais_caro": produto_mais_caro,
        "categorias_disponiveis": len(set(p["categoria"] for p in produtos))
    }

# =============================================================================
# FUNÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    """
    Executa o servidor FastAPI
    
    Para executar:
    python exemplo_simples.py
    
    Ou usando uvicorn:
    uvicorn exemplo_simples:app --reload --port 8000
    """
    print("🚀 Iniciando API Simples FastAPI...")
    print("📚 Documentação disponível em: http://localhost:8000/docs")
    print("💡 Use Ctrl+C para parar o servidor")
    
    uvicorn.run(
        "exemplo_simples:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
