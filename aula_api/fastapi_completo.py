"""
AULA COMPLETA: FastAPI 

Autor: Matheus C. Pestana
Data: 2025
"""

# =============================================================================
# IMPORTS NECESSÁRIOS
# =============================================================================
from fastapi import FastAPI, HTTPException, Depends, Header, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, EmailStr, validator
from typing import List, Optional, Dict, Any
from uuid import uuid4, UUID
import uvicorn
import json
from datetime import datetime, timedelta
import asyncio

# =============================================================================
# CONFIGURAÇÃO INICIAL DO FASTAPI
# =============================================================================

# Criando a instância principal da aplicação
app = FastAPI(
    title="API de Exemplo - FastAPI Completo",
    description="Uma API completa demonstrando recursos avançados do FastAPI",
    version="1.0.0",
    docs_url="/docs",  # Documentação Swagger UI
    redoc_url="/redoc"  # Documentação ReDoc
)

# Configurando CORS para permitir requisições de diferentes origens
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique apenas as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# MODELOS DE DADOS (Pydantic)
# =============================================================================

class UsuarioBase(BaseModel):
    """Modelo base para usuários com validações"""
    nome: str = Field(..., min_length=2, max_length=100, description="Nome completo do usuário")
    email: EmailStr = Field(..., description="Email válido do usuário")
    idade: Optional[int] = Field(None, ge=0, le=120, description="Idade do usuário (opcional)")
    
    @validator('nome')
    def nome_deve_ter_espaco(cls, v):
        """Valida se o nome contém pelo menos um espaço"""
        if ' ' not in v:
            raise ValueError('Nome deve conter nome e sobrenome')
        return v.title()

class UsuarioCriar(UsuarioBase):
    """Modelo para criação de usuários"""
    senha: str = Field(..., min_length=6, description="Senha com pelo menos 6 caracteres")

class Usuario(UsuarioBase):
    """Modelo completo de usuário com ID e data de criação"""
    id: UUID
    data_criacao: datetime
    ativo: bool = True
    
    class Config:
        """Configurações do modelo"""
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "nome": "João Silva",
                "email": "joao.silva@email.com",
                "idade": 30,
                "data_criacao": "2025-01-15T10:00:00",
                "ativo": True
            }
        }

class TarefaBase(BaseModel):
    """Modelo base para tarefas"""
    titulo: str = Field(..., min_length=1, max_length=200, description="Título da tarefa")
    descricao: Optional[str] = Field(None, max_length=1000, description="Descrição detalhada")
    prioridade: str = Field("média", regex="^(baixa|média|alta)$", description="Prioridade da tarefa")
    
class TarefaCriar(TarefaBase):
    """Modelo para criação de tarefas"""
    pass

class Tarefa(TarefaBase):
    """Modelo completo de tarefa"""
    id: UUID
    usuario_id: UUID
    criada_em: datetime
    concluida: bool = False
    concluida_em: Optional[datetime] = None
    
    class Config:
        schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "titulo": "Implementar API",
                "descricao": "Criar endpoints para CRUD de usuários",
                "prioridade": "alta",
                "usuario_id": "123e4567-e89b-12d3-a456-426614174000",
                "criada_em": "2025-01-15T10:00:00",
                "concluida": False,
                "concluida_em": None
            }
        }

class LoginRequest(BaseModel):
    """Modelo para requisição de login"""
    email: EmailStr
    senha: str

class TokenResponse(BaseModel):
    """Modelo para resposta de autenticação"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# =============================================================================
# BANCO DE DADOS SIMULADO (EM MEMÓRIA)
# =============================================================================

# Dicionários para simular um banco de dados
USUARIOS: Dict[UUID, Usuario] = {}
TAREFAS: Dict[UUID, Tarefa] = {}
SESSOES: Dict[str, Dict[str, Any]] = {}

# Usuário padrão para testes
USUARIO_PADRAO = Usuario(
    id=uuid4(),
    nome="Admin Sistema",
    email="admin@sistema.com",
    idade=25,
    data_criacao=datetime.now(),
    ativo=True
)
USUARIOS[USUARIO_PADRAO.id] = USUARIO_PADRAO

# =============================================================================
# FUNÇÕES AUXILIARES E DEPENDÊNCIAS
# =============================================================================

def get_usuario_por_id(usuario_id: UUID) -> Usuario:
    """Busca um usuário pelo ID ou retorna erro 404"""
    if usuario_id not in USUARIOS:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return USUARIOS[usuario_id]

def get_tarefa_por_id(tarefa_id: UUID) -> Tarefa:
    """Busca uma tarefa pelo ID ou retorna erro 404"""
    if tarefa_id not in TAREFAS:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return TAREFAS[tarefa_id]

async def verificar_token(authorization: str = Header(...)) -> Usuario:
    """Verifica se o token de autorização é válido"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Token inválido")
    
    token = authorization.replace("Bearer ", "")
    
    if token not in SESSOES:
        raise HTTPException(status_code=401, detail="Token expirado ou inválido")
    
    sessao = SESSOES[token]
    if datetime.now() > sessao["expira_em"]:
        del SESSOES[token]
        raise HTTPException(status_code=401, detail="Token expirado")
    
    return get_usuario_por_id(sessao["usuario_id"])

def gerar_token(usuario_id: UUID) -> str:
    """Gera um token de acesso para o usuário"""
    token = str(uuid4())
    SESSOES[token] = {
        "usuario_id": usuario_id,
        "expira_em": datetime.now() + timedelta(hours=24)
    }
    return token

# =============================================================================
# ENDPOINTS DE AUTENTICAÇÃO
# =============================================================================

@app.post("/auth/login", response_model=TokenResponse, tags=["Autenticação"])
async def login(credenciais: LoginRequest):
    """
    Endpoint para autenticação de usuários
    
    - **email**: Email do usuário
    - **senha**: Senha do usuário
    
    Retorna um token de acesso válido por 24 horas
    """
    # Em um sistema real, você verificaria a senha no banco de dados
    # Aqui estamos simulando com o usuário padrão
    if (credenciais.email == "admin@sistema.com" and 
        credenciais.senha == "123456"):
        token = gerar_token(USUARIO_PADRAO.id)
        return TokenResponse(
            access_token=token,
            expires_in=86400  # 24 horas em segundos
        )
    
    raise HTTPException(status_code=401, detail="Credenciais inválidas")

@app.post("/auth/logout", tags=["Autenticação"])
async def logout(usuario_atual: Usuario = Depends(verificar_token)):
    """
    Endpoint para logout (invalida o token atual)
    """
    # Em um sistema real, você invalidaria o token
    # Aqui estamos apenas retornando sucesso
    return {"mensagem": "Logout realizado com sucesso"}

# =============================================================================
# ENDPOINTS DE USUÁRIOS
# =============================================================================

@app.get("/usuarios", response_model=List[Usuario], tags=["Usuários"])
async def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    ativo: Optional[bool] = None
):
    """
    Lista todos os usuários com paginação e filtros
    
    - **skip**: Número de registros para pular (paginação)
    - **limit**: Número máximo de registros a retornar
    - **ativo**: Filtrar por status ativo/inativo
    """
    usuarios = list(USUARIOS.values())
    
    # Aplicar filtro de status se especificado
    if ativo is not None:
        usuarios = [u for u in usuarios if u.ativo == ativo]
    
    # Aplicar paginação
    return usuarios[skip:skip + limit]

@app.get("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuários"])
async def obter_usuario(usuario_id: UUID):
    """
    Obtém um usuário específico pelo ID
    """
    return get_usuario_por_id(usuario_id)

@app.post("/usuarios", response_model=Usuario, status_code=201, tags=["Usuários"])
async def criar_usuario(usuario: UsuarioCriar):
    """
    Cria um novo usuário
    
    - **usuario**: Dados do usuário a ser criado
    
    Retorna o usuário criado com ID e data de criação
    """
    # Verificar se o email já existe
    for u in USUARIOS.values():
        if u.email == usuario.email:
            raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    # Criar novo usuário
    novo_usuario = Usuario(
        id=uuid4(),
        nome=usuario.nome,
        email=usuario.email,
        idade=usuario.idade,
        data_criacao=datetime.now(),
        ativo=True
    )
    
    USUARIOS[novo_usuario.id] = novo_usuario
    return novo_usuario

@app.put("/usuarios/{usuario_id}", response_model=Usuario, tags=["Usuários"])
async def atualizar_usuario(
    usuario_id: UUID,
    usuario_atualizado: UsuarioBase,
    usuario_atual: Usuario = Depends(verificar_token)
):
    """
    Atualiza um usuário existente
    
    - **usuario_id**: ID do usuário a ser atualizado
    - **usuario_atualizado**: Novos dados do usuário
    
    Apenas usuários autenticados podem atualizar
    """
    # Verificar se o usuário está tentando atualizar a si mesmo
    if usuario_atual.id != usuario_id:
        raise HTTPException(status_code=403, detail="Não autorizado a atualizar outros usuários")
    
    usuario = get_usuario_por_id(usuario_id)
    
    # Atualizar campos
    usuario.nome = usuario_atualizado.nome
    usuario.email = usuario_atualizado.email
    usuario.idade = usuario_atualizado.idade
    
    return usuario

@app.delete("/usuarios/{usuario_id}", status_code=204, tags=["Usuários"])
async def deletar_usuario(
    usuario_id: UUID,
    usuario_atual: Usuario = Depends(verificar_token)
):
    """
    Remove um usuário (soft delete - marca como inativo)
    
    - **usuario_id**: ID do usuário a ser removido
    
    Apenas usuários autenticados podem remover
    """
    if usuario_atual.id != usuario_id:
        raise HTTPException(status_code=403, detail="Não autorizado a remover outros usuários")
    
    usuario = get_usuario_por_id(usuario_id)
    usuario.ativo = False

# =============================================================================
# ENDPOINTS DE TAREFAS
# =============================================================================

@app.get("/tarefas", response_model=List[Tarefa], tags=["Tarefas"])
async def listar_tarefas(
    skip: int = 0,
    limit: int = 100,
    usuario_id: Optional[UUID] = None,
    concluida: Optional[bool] = None,
    prioridade: Optional[str] = None
):
    """
    Lista todas as tarefas com filtros e paginação
    
    - **skip**: Número de registros para pular
    - **limit**: Número máximo de registros
    - **usuario_id**: Filtrar por usuário específico
    - **concluida**: Filtrar por status de conclusão
    - **prioridade**: Filtrar por prioridade
    """
    tarefas = list(TAREFAS.values())
    
    # Aplicar filtros
    if usuario_id is not None:
        tarefas = [t for t in tarefas if t.usuario_id == usuario_id]
    
    if concluida is not None:
        tarefas = [t for t in tarefas if t.concluida == concluida]
    
    if prioridade is not None:
        tarefas = [t for t in tarefas if t.prioridade == prioridade]
    
    # Aplicar paginação
    return tarefas[skip:skip + limit]

@app.get("/tarefas/{tarefa_id}", response_model=Tarefa, tags=["Tarefas"])
async def obter_tarefa(tarefa_id: UUID):
    """
    Obtém uma tarefa específica pelo ID
    """
    return get_tarefa_por_id(tarefa_id)

@app.post("/tarefas", response_model=Tarefa, status_code=201, tags=["Tarefas"])
async def criar_tarefa(
    tarefa: TarefaCriar,
    usuario_atual: Usuario = Depends(verificar_token)
):
    """
    Cria uma nova tarefa
    
    - **tarefa**: Dados da tarefa a ser criada
    
    A tarefa será associada ao usuário autenticado
    """
    nova_tarefa = Tarefa(
        id=uuid4(),
        titulo=tarefa.titulo,
        descricao=tarefa.descricao,
        prioridade=tarefa.prioridade,
        usuario_id=usuario_atual.id,
        criada_em=datetime.now(),
        concluida=False
    )
    
    TAREFAS[nova_tarefa.id] = nova_tarefa
    return nova_tarefa

@app.put("/tarefas/{tarefa_id}", response_model=Tarefa, tags=["Tarefas"])
async def atualizar_tarefa(
    tarefa_id: UUID,
    tarefa_atualizada: TarefaBase,
    usuario_atual: Usuario = Depends(verificar_token)
):
    """
    Atualiza uma tarefa existente
    
    - **tarefa_id**: ID da tarefa a ser atualizada
    - **tarefa_atualizada**: Novos dados da tarefa
    
    Apenas o proprietário da tarefa pode atualizá-la
    """
    tarefa = get_tarefa_por_id(tarefa_id)
    
    if tarefa.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Não autorizado a atualizar esta tarefa")
    
    # Atualizar campos
    tarefa.titulo = tarefa_atualizada.titulo
    tarefa.descricao = tarefa_atualizada.descricao
    tarefa.prioridade = tarefa_atualizada.prioridade
    
    return tarefa

@app.patch("/tarefas/{tarefa_id}/concluir", response_model=Tarefa, tags=["Tarefas"])
async def concluir_tarefa(
    tarefa_id: UUID,
    usuario_atual: Usuario = Depends(verificar_token)
):
    """
    Marca uma tarefa como concluída
    
    - **tarefa_id**: ID da tarefa a ser concluída
    """
    tarefa = get_tarefa_por_id(tarefa_id)
    
    if tarefa.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Não autorizado a concluir esta tarefa")
    
    if tarefa.concluida:
        raise HTTPException(status_code=400, detail="Tarefa já está concluída")
    
    tarefa.concluida = True
    tarefa.concluida_em = datetime.now()
    
    return tarefa

@app.delete("/tarefas/{tarefa_id}", status_code=204, tags=["Tarefas"])
async def deletar_tarefa(
    tarefa_id: UUID,
    usuario_atual: Usuario = Depends(verificar_token)
):
    """
    Remove uma tarefa permanentemente
    
    - **tarefa_id**: ID da tarefa a ser removida
    
    Apenas o proprietário da tarefa pode removê-la
    """
    tarefa = get_tarefa_por_id(tarefa_id)
    
    if tarefa.usuario_id != usuario_atual.id:
        raise HTTPException(status_code=403, detail="Não autorizado a remover esta tarefa")
    
    del TAREFAS[tarefa_id]

# =============================================================================
# ENDPOINTS DE ESTATÍSTICAS
# =============================================================================

@app.get("/estatisticas", tags=["Estatísticas"])
async def obter_estatisticas(usuario_atual: Usuario = Depends(verificar_token)):
    """
    Retorna estatísticas das tarefas do usuário autenticado
    """
    tarefas_usuario = [t for t in TAREFAS.values() if t.usuario_id == usuario_atual.id]
    
    total_tarefas = len(tarefas_usuario)
    tarefas_concluidas = len([t for t in tarefas_usuario if t.concluida])
    tarefas_pendentes = total_tarefas - tarefas_concluidas
    
    # Estatísticas por prioridade
    prioridades = {}
    for tarefa in tarefas_usuario:
        prioridades[tarefa.prioridade] = prioridades.get(tarefa.prioridade, 0) + 1
    
    return {
        "total_tarefas": total_tarefas,
        "tarefas_concluidas": tarefas_concluidas,
        "tarefas_pendentes": tarefas_pendentes,
        "taxa_conclusao": (tarefas_concluidas / total_tarefas * 100) if total_tarefas > 0 else 0,
        "por_prioridade": prioridades
    }

# =============================================================================
# MIDDLEWARE E ENDPOINTS DE SISTEMA
# =============================================================================

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware para logar todas as requisições
    """
    start_time = datetime.now()
    
    # Processar a requisição
    response = await call_next(request)
    
    # Calcular tempo de resposta
    process_time = (datetime.now() - start_time).total_seconds()
    
    # Adicionar headers informativos
    response.headers["X-Process-Time"] = str(process_time)
    response.headers["X-Request-ID"] = str(uuid4())
    
    # Log da requisição (em produção, use um sistema de logging apropriado)
    print(f"{request.method} {request.url.path} - {response.status_code} - {process_time:.3f}s")
    
    return response

@app.get("/", tags=["Sistema"])
async def root():
    """
    Endpoint raiz da API
    """
    return {
        "mensagem": "Bem-vindo à API de Exemplo - FastAPI Completo!",
        "versao": "1.0.0",
        "documentacao": "/docs",
        "endpoints_disponiveis": [
            "/auth/login",
            "/usuarios",
            "/tarefas",
            "/estatisticas"
        ]
    }

@app.get("/health", tags=["Sistema"])
async def health_check():
    """
    Endpoint para verificar a saúde da API
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "usuarios_cadastrados": len(USUARIOS),
        "tarefas_cadastradas": len(TAREFAS),
        "sessoes_ativas": len(SESSOES)
    }

# =============================================================================
# TAREFAS EM SEGUNDO PLANO
# =============================================================================

def limpar_sessoes_expiradas():
    """
    Função para limpar sessões expiradas
    """
    tokens_para_remover = []
    for token, sessao in SESSOES.items():
        if datetime.now() > sessao["expira_em"]:
            tokens_para_remover.append(token)
    
    for token in tokens_para_remover:
        del SESSOES[token]
    
    print(f"Limpeza automática: {len(tokens_para_remover)} sessões expiradas removidas")

@app.post("/sistema/limpar-sessoes", tags=["Sistema"])
async def limpar_sessoes(background_tasks: BackgroundTasks):
    """
    Agenda uma limpeza automática das sessões expiradas
    """
    background_tasks.add_task(limpar_sessoes_expiradas)
    return {"mensagem": "Limpeza de sessões agendada"}

# =============================================================================
# TRATAMENTO DE ERROS PERSONALIZADO
# =============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """
    Handler personalizado para exceções HTTP
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "erro": True,
            "codigo": exc.status_code,
            "mensagem": exc.detail,
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handler para exceções gerais não tratadas
    """
    return JSONResponse(
        status_code=500,
        content={
            "erro": True,
            "codigo": 500,
            "mensagem": "Erro interno do servidor",
            "timestamp": datetime.now().isoformat(),
            "path": request.url.path
        }
    )

# =============================================================================
# FUNÇÃO PRINCIPAL PARA EXECUÇÃO
# =============================================================================

if __name__ == "__main__":
    """
    Executa o servidor FastAPI diretamente
    
    Para executar:
    python fastapi_completo.py
    
    Ou usando uvicorn:
    uvicorn fastapi_completo:app --reload --host 0.0.0.0 --port 8000
    """
    print("🚀 Iniciando servidor FastAPI...")
    print("📚 Documentação disponível em: http://localhost:8000/docs")
    print("🔍 ReDoc disponível em: http://localhost:8000/redoc")
    print("💡 Use Ctrl+C para parar o servidor")
    
    uvicorn.run(
        "fastapi_completo:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )









