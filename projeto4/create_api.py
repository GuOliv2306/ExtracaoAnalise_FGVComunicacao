# API Framework
from fastapi import FastAPI
from pydantic import BaseModel

# Manipulação de dados (se necessário)
import pandas as pd

# Para execução da API
import uvicorn

# Utilitários (se necessário)
import json

df = pd.read_csv('https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv')

app = FastAPI(title="API de Extração e Análise - FGV Comunicações")

#IA
from agno.agent import Agent
from agno.models.groq import Groq
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.python import PythonTools
from agno.tools.pandas import PandasTools

# Modelo para input da IA
class AnaliseInput(BaseModel):
    pergunta: str
    contexto: str = "Dataset Titanic com informações sobre passageiros"

@app.get("/")
def read_root():
    return {
        'projeto': 'extraindo algo',
        'autor': 'Gustavo de Oliveira',
        'Informações': 'API para extração e análise de dados da FGV Comunicações',
        'total_registros': len(df)
    }

@app.get("/dados")
def read_dados():
    '''
    Retorna todos os dados extraídos.
    '''
    # Return data as JSON-compatible Python objects (list of records)
    return json.loads(df.to_json(orient='records'))

@app.get("/dados/{id}")
def read_dado(id: int):
    '''
    Retorna um dado específico pelo ID.
    '''
    if id < 0 or id >= len(df):
        return {"error": "ID fora do intervalo."}
    
    # Converter a Series para um dicionário JSON-serializável
    registro = df.iloc[id].to_dict()
    
    # Converter tipos numpy para tipos Python nativos
    for key, value in registro.items():
        if pd.isna(value):
            registro[key] = None
        elif hasattr(value, 'item'):  # Para tipos numpy
            registro[key] = value.item()
    
    return registro

@app.get("/categoria/{categoria}")
def read_categoria(categoria: str):
    '''
    Retorna todos os dados de uma categoria específica.
    '''
    # Verificar se a coluna 'categoria' existe no DataFrame
    if 'categoria' not in df.columns:
        return {"error": "Coluna 'categoria' não encontrada no dataset."}
    
    dados_categoria = df[df['categoria'] == categoria]
    if dados_categoria.empty:
        return {"error": "Categoria não encontrada."}
    
    # Converter DataFrame para lista de dicionários JSON-serializáveis
    return json.loads(dados_categoria.to_json(orient='records'))

@app.get("/estatisticas")
def read_estatisticas():
    '''
    Retorna estatísticas descritivas dos dados.
    '''
    estatisticas = json.loads(df.describe(include='all').to_json())
    return estatisticas
@app.get("/IA")
def analise_ia_get():
    '''
    Retorna informações sobre como usar a análise de IA.
    '''
    return {
        "message": "Use POST /analise_ia para enviar uma pergunta para análise",
        "exemplo": {
            "pergunta": "Qual a taxa de sobrevivência por classe social?",
            "contexto": "Dataset Titanic com informações sobre passageiros"
        },
        "dataset_info": {
            "total_registros": len(df),
            "colunas": df.columns.tolist(),
            "primeiros_registros": json.loads(df.head(3).to_json(orient='records'))
        }
    }

@app.post("/analise_ia")
def analise_ia_post(input_data: AnaliseInput):
    '''
    Realiza análise de dados usando IA com base no input fornecido.
    '''
    try:
        # Criar o agente de IA
        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            description=f"Você é um assistente especializado em análise de dados. {input_data.contexto}. Use as ferramentas disponíveis para responder perguntas sobre os dados.",
            tools=[PythonTools(), PandasTools()],
            show_tool_calls=True,
            markdown=False  # Retornamos em formato de texto para processar melhor
        )
        
        # Preparar o contexto com informações do dataset
        dataset_context = f"""
        Dataset disponível: Titanic
        Total de registros: {len(df)}
        Colunas: {', '.join(df.columns.tolist())}
        
        Pergunta do usuário: {input_data.pergunta}
        
        Por favor, analise os dados do Titanic e responda à pergunta de forma estruturada.
        """
        
        # Executar a análise
        resposta = agent.run(dataset_context)
        
        # Processar a resposta para retornar um dicionário estruturado
        resultado = {
            "pergunta": input_data.pergunta,
            "contexto": input_data.contexto,
            "resposta": str(resposta.content) if hasattr(resposta, 'content') else str(resposta),
            "dataset_info": {
                "total_registros": len(df),
                "colunas_analisadas": df.columns.tolist()
            },
            "status": "sucesso",
            "timestamp": pd.Timestamp.now().isoformat()
        }
        
        return resultado
        
    except Exception as e:
        return {
            "pergunta": input_data.pergunta,
            "contexto": input_data.contexto,
            "erro": str(e),
            "status": "erro",
            "timestamp": pd.Timestamp.now().isoformat(),
            "sugestao": "Verifique se a pergunta está clara e se o modelo Groq está acessível"
        }

@app.get("/analise_rapida/{pergunta}")
def analise_rapida(pergunta: str):
    '''
    Realiza uma análise rápida com base em uma pergunta simples via GET.
    '''
    try:
        # Criar o agente de IA
        agent = Agent(
            model=Groq(id="llama-3.3-70b-versatile"),
            description="Você é um assistente de análise de dados do Titanic. Responda de forma concisa e estruturada.",
            tools=[PythonTools(), PandasTools()],
            show_tool_calls=False,
            markdown=False
        )
        
        # Contexto simplificado
        contexto_rapido = f"""
        Analise o dataset Titanic ({len(df)} registros) e responda: {pergunta}
        Colunas disponíveis: {', '.join(df.columns.tolist())}
        Seja conciso e objetivo na resposta.
        """
        
        # Executar análise
        resposta = agent.run(contexto_rapido)
        
        return {
            "pergunta": pergunta,
            "resposta_rapida": str(resposta.content) if hasattr(resposta, 'content') else str(resposta),
            "dataset": "Titanic",
            "registros": len(df),
            "status": "sucesso"
        }
        
    except Exception as e:
        return {
            "pergunta": pergunta,
            "erro": str(e),
            "status": "erro",
            "alternativa": "Use POST /analise_ia para análises mais detalhadas"
        }
if __name__ == "__main__":
    try:
        import uvicorn
        uvicorn.run(app, host="localhost", port=8001)
    except RuntimeError as e:
        print(f"Erro ao iniciar a API: {e}")
        print("Verifique se a porta 8000 já está em uso e finalize o processo que está utilizando-a.")