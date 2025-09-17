# ===========================================
# FASTAPI - NÍVEL BÁSICO
# ===========================================
# Este arquivo mostra o básico do básico do FastAPI
# Vamos começar com um simples "Hello World"

# 1. IMPORTANDO O FASTAPI
# O FastAPI é uma biblioteca para criar APIs web modernas e rápidas
from fastapi import FastAPI

# 2. CRIANDO UMA INSTÂNCIA DO FASTAPI
# Aqui criamos nossa aplicação FastAPI
# O parâmetro 'title' aparece na documentação automática
app = FastAPI(title="Minha Primeira API")

# 3. CRIANDO NOSSO PRIMEIRO ENDPOINT
# O decorador @app.get() define que esta função responde a requisições GET
# "/" significa que será acessível na URL raiz (ex: http://localhost:8000/)
@app.get("/")
def hello_world():
    """
    Esta função retorna uma mensagem simples
    O FastAPI automaticamente converte o retorno para JSON
    """
    return {"mensagem": "Hello World!"}

# 4. CRIANDO UM ENDPOINT COM PARÂMETRO
# Agora vamos criar um endpoint que aceita um parâmetro na URL
@app.get("/ola/{nome}")
def ola_pessoa(nome: str):
    """
    Este endpoint aceita um parâmetro 'nome' na URL
    Exemplo: http://localhost:8000/ola/João
    """
    return {"mensagem": f"Olá, {nome}!"}

# 5. ENDPOINT COM QUERY PARAMETERS
# Query parameters são parâmetros que vêm após o ? na URL
@app.get("/soma")
def somar_numeros(a: int, b: int):
    """
    Este endpoint aceita dois parâmetros como query parameters
    Exemplo: http://localhost:8000/soma?a=5&b=3
    """
    resultado = a + b
    return {"a": a, "b": b, "soma": resultado}

# 6. COMO EXECUTAR ESTA API
# Para executar, use no terminal, ESTANDO DENTRO DA PASTA AULA_14!!!!!!!
# uvicorn basico:app --reload
# 
# O --reload faz com que a API reinicie automaticamente quando você modificar o código
# Acesse http://localhost:8000 para ver o resultado
# Acesse http://localhost:8000/docs para ver a documentação automática!

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
