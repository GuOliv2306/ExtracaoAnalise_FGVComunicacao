# ===========================================
# FASTAPI - NÍVEL INTERMEDIÁRIO
# ===========================================
# Este arquivo mostra conceitos intermediários do FastAPI
# Incluindo dicionários, diferentes métodos HTTP, e conceitos de async

from fastapi import FastAPI, HTTPException
from typing import List, Optional
import asyncio

# Criando nossa aplicação
app = FastAPI(title="API Intermediária", version="1.0.0")

# ===========================================
# 1. TRABALHANDO COM DICIONÁRIOS E DADOS
# ===========================================

# Simulando um banco de dados simples com dicionários
usuarios_db = {
    1: {"id": 1, "nome": "Matheus Pestana", "email": "matheus.pestana@fgv.br", "idade": 32},
    2: {"id": 2, "nome": "Getulio Vargas", "email": "getulio@vargas.br", "idade": 72},
    3: {"id": 3, "nome": "Helen Folasade Adu", "email": "sa@de.uk", "idade": 66}
}

produtos_db = {
    1: {"id": 1, "nome": "Notebook Gamer", "preco": 2500.00, "categoria": "Eletrônicos"},
    2: {"id": 2, "nome": "Livro Aprenda Python!", "preco": 89.90, "categoria": "Livros"},
    3: {"id": 3, "nome": "Perfume do Cebolinha", "preco": 45.50, "categoria": "Perfumes"},
    4: {"id": 4, "nome": "SSD 1TB", "preco": 500.99, "categoria": "Eletrônicos"}
}

# ===========================================
# 2. MÉTODOS HTTP DIFERENTES
# ===========================================

# GET - Buscar dados
@app.get("/usuarios")
def listar_usuarios():
    """
    Retorna todos os usuários
    GET /usuarios
    """
    return {"usuarios": list(usuarios_db.values())}

@app.get("/usuarios/{usuario_id}")
def buscar_usuario(usuario_id: int):
    """
    Busca um usuário específico pelo ID
    GET /usuarios/1
    """
    if usuario_id not in usuarios_db:
        # HTTPException é usada para retornar erros HTTP apropriados
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    return {"usuario": usuarios_db[usuario_id]}

# POST - Criar novos dados
@app.post("/usuarios")
def criar_usuario(nome: str, email: str, idade: int):
    """
    Cria um novo usuário
    POST /usuarios?nome=Polyana&email=polyana.barboza@fgv.br&idade=30
    """
    # Gerando um novo ID (simulando auto-incremento)
    novo_id = max(usuarios_db.keys()) + 1 if usuarios_db else 1
    
    novo_usuario = {
        "id": novo_id,
        "nome": nome,
        "email": email,
        "idade": idade
    }
    
    usuarios_db[novo_id] = novo_usuario
    
    return {"mensagem": "Usuário criado com sucesso", "usuario": novo_usuario}

# PUT - Atualizar dados existentes
@app.put("/usuarios/{usuario_id}")
def atualizar_usuario(usuario_id: int, nome: str, email: str, idade: int):
    """
    Atualiza um usuário existente
    PUT /usuarios/1?nome=Matheus Atualizado&email=matheus.pestana@prof.fgv.edu.br&idade=32
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuarios_db[usuario_id] = {
        "id": usuario_id,
        "nome": nome,
        "email": email,
        "idade": idade
    }
    
    return {"mensagem": "Usuário atualizado com sucesso", "usuario": usuarios_db[usuario_id]}

# DELETE - Remover dados
@app.delete("/usuarios/{usuario_id}")
def deletar_usuario(usuario_id: int):
    """
    Remove um usuário
    DELETE /usuarios/1
    """
    if usuario_id not in usuarios_db:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    usuario_removido = usuarios_db.pop(usuario_id)
    
    return {"mensagem": "Usuário removido com sucesso", "usuario_removido": usuario_removido}

# ===========================================
# 3. CONCEITOS DE ASYNC/AWAIT
# ===========================================

# Função assíncrona simples
@app.get("/async-exemplo")
async def exemplo_async():
    """
    Exemplo de função assíncrona
    O 'async' permite que a função seja executada de forma não-bloqueante
    """
    # Simulando uma operação que demora (como consulta ao banco)
    await asyncio.sleep(1)  # Aguarda 1 segundo
    
    return {"mensagem": "Esta resposta demorou 1 segundo para ser processada"}

# Função assíncrona com processamento
@app.get("/estatisticas")
async def estatisticas_usuarios():
    """
    Calcula estatísticas dos usuários de forma assíncrona
    """
    # Simulando processamento pesado
    await asyncio.sleep(3.5)
    
    usuarios = list(usuarios_db.values())
    idades = [usuario["idade"] for usuario in usuarios]
    
    estatisticas = {
        "total_usuarios": len(usuarios),
        "idade_media": sum(idades) / len(idades) if idades else 0,
        "idade_minima": min(idades) if idades else 0,
        "idade_maxima": max(idades) if idades else 0
    }
    
    return {"estatisticas": estatisticas}

# ===========================================
# 4. QUERY PARAMETERS E FILTROS
# ===========================================

@app.get("/produtos")
def listar_produtos(categoria: Optional[str] = None, preco_maximo: Optional[float] = None):
    """
    Lista produtos com filtros opcionais
    GET /produtos
    GET /produtos?categoria=Eletrônicos
    GET /produtos?preco_maximo=100.0
    GET /produtos?categoria=Eletrônicos&preco_maximo=100.0
    """
    produtos = list(produtos_db.values())
    
    # Aplicando filtros
    if categoria:
        produtos = [p for p in produtos if p["categoria"] == categoria]
    
    if preco_maximo is not None:
        produtos = [p for p in produtos if p["preco"] <= preco_maximo]
    
    return {"produtos": produtos, "total": len(produtos)}

# ===========================================
# 5. RESPONSES PERSONALIZADAS
# ===========================================

from fastapi.responses import JSONResponse

@app.get("/resposta-personalizada")
def resposta_personalizada():
    """
    Exemplo de resposta personalizada com status code customizado
    """
    return JSONResponse(
        status_code=201,  # Status 201 = Created
        content={
            "mensagem": "Resposta personalizada",
            "status": "sucesso",
            "dados": {"exemplo": "valor"}
        }
    )

# ===========================================
# COMO EXECUTAR
# ===========================================
# uvicorn medio:app --reload
# 
# Endpoints disponíveis:
# - GET /usuarios - Lista todos os usuários
# - GET /usuarios/{id} - Busca usuário específico
# - POST /usuarios - Cria novo usuário
# - PUT /usuarios/{id} - Atualiza usuário
# - DELETE /usuarios/{id} - Remove usuário
# - GET /async-exemplo - Exemplo de async
# - GET /usuarios/estatisticas - Estatísticas dos usuários
# - GET /produtos - Lista produtos com filtros
# - GET /resposta-personalizada - Resposta customizada

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
