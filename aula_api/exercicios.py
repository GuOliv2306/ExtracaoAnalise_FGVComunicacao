#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EXERCÍCIOS PRÁTICOS: FastAPI - Aplicando o Conhecimento

Este arquivo contém exercícios práticos para consolidar o aprendizado do FastAPI.
Complete cada exercício para dominar os conceitos apresentados.

Autor: LabExtracaoAnalise2025
Data: 2025
"""

"""
EXERCÍCIO 1: API de Livros
=======================

Crie uma API para gerenciar uma biblioteca de livros com os seguintes endpoints:

1. GET /livros - Listar todos os livros
2. GET /livros/{id} - Obter livro específico
3. POST /livros - Adicionar novo livro
4. PUT /livros/{id} - Atualizar livro
5. DELETE /livros/{id} - Remover livro
6. GET /livros/buscar?q={termo} - Buscar livros por termo
7. GET /livros/autor/{autor} - Listar livros por autor
8. GET /livros/estatisticas - Estatísticas da biblioteca

Modelo de Livro:
- id: int (automático)
- titulo: str (obrigatório, 1-200 chars)
- autor: str (obrigatório, 1-100 chars)
- ano: int (opcional, 1800-2025)
- genero: str (obrigatório, escolha: romance, ficcao, nao-ficcao, biografia)
- paginas: int (opcional, >0)
- disponivel: bool (padrao: True)

Validações:
- Ano deve estar entre 1800 e 2025
- Páginas deve ser maior que 0
- Gênero deve ser um dos valores permitidos
- Título e autor são obrigatórios

Funcionalidades:
- Busca por termo no título ou autor
- Filtros por gênero e disponibilidade
- Estatísticas (total, por gênero, disponíveis)
- Paginação na listagem principal
"""

"""
EXERCÍCIO 2: Sistema de Avaliações
===============================

Crie uma API para um sistema de avaliações de produtos com:

1. GET /produtos - Listar produtos
2. POST /produtos - Adicionar produto
3. GET /produtos/{id} - Obter produto
4. POST /produtos/{id}/avaliacoes - Adicionar avaliação
5. GET /produtos/{id}/avaliacoes - Listar avaliações
6. GET /produtos/{id}/estatisticas - Estatísticas do produto

Modelos:
Produto:
- id: int
- nome: str
- descricao: str
- preco: float
- categoria: str

Avaliacao:
- id: int
- produto_id: int
- usuario: str
- nota: int (1-5)
- comentario: str (opcional)
- data: datetime

Validações:
- Nota deve estar entre 1 e 5
- Usuário é obrigatório
- Produto deve existir

Funcionalidades:
- Calcular nota média por produto
- Contar total de avaliações
- Filtrar por nota mínima
- Ordenar por data ou nota
"""

"""
EXERCÍCIO 3: API de Eventos
========================

Crie uma API para gerenciar eventos com:

1. GET /eventos - Listar eventos
2. POST /eventos - Criar evento
3. GET /eventos/{id} - Obter evento
4. PUT /eventos/{id} - Atualizar evento
5. DELETE /eventos/{id} - Remover evento
6. POST /eventos/{id}/inscricoes - Inscrever participante
7. GET /eventos/{id}/participantes - Listar participantes
8. GET /eventos/proximos - Eventos futuros
9. GET /eventos/estatisticas - Estatísticas gerais

Modelos:
Evento:
- id: int
- titulo: str
- descricao: str
- data_inicio: datetime
- data_fim: datetime
- local: str
- capacidade: int
- preco: float
- categoria: str

Inscricao:
- id: int
- evento_id: int
- nome: str
- email: str
- telefone: str (opcional)
- data_inscricao: datetime

Validações:
- Data fim deve ser depois da data início
- Capacidade deve ser > 0
- Preço deve ser >= 0
- Email deve ser válido
- Não permitir inscrições duplicadas por email

Funcionalidades:
- Filtrar eventos por data
- Verificar disponibilidade
- Calcular ocupação
- Estatísticas por categoria
"""

"""
EXERCÍCIO 4: Sistema de Autenticação
================================

Implemente um sistema de autenticação completo:

1. POST /auth/registrar - Registrar usuário
2. POST /auth/login - Fazer login
3. POST /auth/logout - Fazer logout
4. GET /auth/perfil - Obter perfil do usuário
5. PUT /auth/perfil - Atualizar perfil
6. POST /auth/alterar-senha - Alterar senha

Modelos:
Usuario:
- id: int
- nome: str
- email: str (único)
- senha_hash: str
- data_criacao: datetime
- ativo: bool

LoginRequest:
- email: str
- senha: str

RegistroRequest:
- nome: str
- email: str
- senha: str
- confirmar_senha: str

Validações:
- Email deve ser único
- Senha deve ter pelo menos 8 caracteres
- Senhas devem coincidir no registro
- Email deve ser válido

Funcionalidades:
- Hash de senha com bcrypt
- Tokens JWT para sessão
- Middleware de autenticação
- Proteção de rotas
- Validação de token
"""

"""
EXERCÍCIO 5: API com Middleware e Tratamento de Erros
===============================================

Crie uma API que demonstre:

1. Middleware personalizado para logging
2. Tratamento de erros customizado
3. Validação de rate limiting
4. Headers de segurança
5. Compressão de resposta
6. Cache simples

Funcionalidades:
- Log de todas as requisições com timestamp
- Contador de requisições por IP
- Rate limiting (máximo 100 req/min por IP)
- Headers de segurança (X-Content-Type-Options, X-Frame-Options)
- Compressão gzip para respostas grandes
- Cache em memória para respostas frequentes
- Tratamento personalizado de erros 404, 500
- Health check com métricas

Endpoints:
- GET / - Informações da API
- GET /teste - Endpoint de teste
- GET /cache-test - Teste de cache
- GET /health - Status e métricas
- GET /stats - Estatísticas de uso
"""

"""
EXERCÍCIO 6: API com Upload de Arquivos
===================================

Crie uma API para upload e gerenciamento de arquivos:

1. POST /upload - Upload de arquivo
2. GET /arquivos - Listar arquivos
3. GET /arquivos/{id} - Download de arquivo
4. DELETE /arquivos/{id} - Remover arquivo
5. GET /arquivos/{id}/info - Informações do arquivo
6. POST /arquivos/{id}/compartilhar - Compartilhar arquivo

Modelos:
Arquivo:
- id: int
- nome_original: str
- nome_arquivo: str
- tamanho: int
- tipo_mime: str
- data_upload: datetime
- usuario_id: int
- publico: bool

Validações:
- Tamanho máximo: 10MB
- Tipos permitidos: pdf, doc, docx, txt, jpg, png
- Nome do arquivo não pode estar vazio

Funcionalidades:
- Armazenamento local de arquivos
- Geração de nomes únicos
- Verificação de tipo MIME
- Compressão de imagens
- Geração de thumbnails
- Controle de acesso
- Estatísticas de uso
"""

"""
DICAS PARA OS EXERCÍCIOS:
========================

1. Comece sempre pelos modelos Pydantic
2. Implemente validações robustas
3. Use tipos apropriados para cada campo
4. Documente bem todos os endpoints
5. Implemente tratamento de erros
6. Teste todos os cenários
7. Use a documentação automática (/docs)
8. Implemente filtros e paginação
9. Adicione estatísticas úteis
10. Mantenha o código organizado e limpo

BONUS:
======
- Adicione testes unitários
- Implemente validação de dados mais avançada
- Adicione cache Redis
- Implemente busca full-text
- Adicione autenticação OAuth2
- Implemente WebSockets para tempo real
- Adicione monitoramento com Prometheus
- Implemente backup automático
- Adicione sistema de notificações
- Implemente API versioning
"""

if __name__ == "__main__":
    print("📚 EXERCÍCIOS PRÁTICOS - FASTAPI")
    print("=" * 50)
    print("Complete cada exercício para dominar o FastAPI!")
    print("\nExercícios disponíveis:")
    print("1. API de Livros")
    print("2. Sistema de Avaliações")
    print("3. API de Eventos")
    print("4. Sistema de Autenticação")
    print("5. API com Middleware e Tratamento de Erros")
    print("6. API com Upload de Arquivos")
    print("\n💡 Dica: Comece pelo exercício 1 e avance gradualmente!")
    print("🚀 Use a documentação automática para testar suas APIs!")









