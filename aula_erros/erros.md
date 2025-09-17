# Principais Erros em Python e Como Resolvê-los

Esta aula aborda os erros mais comuns em Python, suas causas e soluções práticas para resolvê-los.

## Índice
1. [ModuleNotFoundError](#modulenotfounderror)
2. [NameError](#nameerror)
3. [ValueError](#valueerror)
4. [TypeError](#typeerror)
5. [IndexError](#indexerror)
6. [KeyError](#keyerror)
7. [FileNotFoundError](#filenotfounderror)
8. [AttributeError](#attributeerror)
9. [IndentationError](#indentationerror)
10. [SyntaxError](#syntaxerror)
11. [ImportError](#importerror)
12. [ZeroDivisionError](#zerodivisionerror)

---

## ModuleNotFoundError

### O que é?
Erro que ocorre quando o Python não consegue encontrar um módulo que você está tentando importar.

### Exemplo:
```python
import pandas  # ModuleNotFoundError: No module named 'pandas'
```

### Principais Causas:
- Módulo não está instalado
- Nome do módulo está incorreto
- Ambiente virtual não ativado
- Módulo instalado em ambiente diferente

### Como Resolver:

#### 1. Instalar o módulo:
```bash
pip install pandas
pip install numpy
pip install requests
pip install matplotlib
```

#### 2. Verificar se está no ambiente virtual correto:
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate.ps1     # Windows

# Verificar módulos instalados
pip list
```

#### 3. Instalar em ambiente específico:
```bash
python -m pip install pandas
```

#### 4. Verificar a grafia do módulo:
```python
# Incorreto
import beatifulsoup

# Correto
import beautifulsoup4
# ou
from bs4 import BeautifulSoup
```

---

## NameError

### O que é?
Erro que ocorre quando você tenta usar uma variável que não foi definida.

### Exemplo:
```python
print(nome)  # NameError: name 'nome' is not defined
```

### Principais Causas:
- Variável não foi declarada
- Erro de digitação no nome da variável
- Variável declarada em escopo diferente
- Ordem incorreta de execução

### Como Resolver:

#### 1. Definir a variável antes de usar:
```python
# Incorreto
print(nome)

# Correto
nome = "João"
print(nome)
```

#### 2. Verificar a grafia:
```python
# Incorreto
nome = "João"
print(nom)  # NameError

# Correto
nome = "João"
print(nome)
```

#### 3. Verificar escopo da variável:
```python
def funcao():
    nome_local = "João"

# Incorreto - variável está no escopo da função
print(nome_local)  # NameError

# Correto
def funcao():
    nome_local = "João"
    return nome_local

nome = funcao()
print(nome)
```

---

## ValueError

### O que é?
Erro que ocorre quando uma função recebe um argumento com tipo correto, mas valor inadequado.

### Exemplo:
```python
int("abc")  # ValueError: invalid literal for int() with base 10: 'abc'
```

### Principais Causas:
- Conversão de tipo inválida
- Valor fora do range esperado
- Formato de string incorreto

### Como Resolver:

#### 1. Validar dados antes da conversão:
```python
# Incorreto
numero = int("abc")

# Correto
texto = "abc"
if texto.isdigit():
    numero = int(texto)
else:
    print("Valor não é um número válido")
```

#### 2. Usar try/except:
```python
try:
    numero = int(input("Digite um número: "))
except ValueError:
    print("Por favor, digite apenas números!")
    numero = 0
```

#### 3. Verificar formato de datas:
```python
from datetime import datetime

# Incorreto
data = datetime.strptime("2023-13-01", "%Y-%m-%d")  # ValueError

# Correto
try:
    data = datetime.strptime("2023-12-01", "%Y-%m-%d")
except ValueError:
    print("Formato de data inválido!")
```

---

## TypeError

### O que é?
Erro que ocorre quando uma operação é aplicada a um objeto de tipo inadequado.

### Exemplo:
```python
"5" + 5  # TypeError: can only concatenate str (not "int") to str
```

### Principais Causas:
- Operações entre tipos incompatíveis
- Função chamada com argumentos de tipo incorreto
- Tentativa de usar métodos inexistentes

### Como Resolver:

#### 1. Converter tipos adequadamente:
```python
# Incorreto
resultado = "5" + 5

# Correto
resultado = int("5") + 5  # 10
# ou
resultado = "5" + str(5)  # "55"
```

#### 2. Verificar tipos antes de operações:
```python
def somar(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return a + b
    else:
        raise TypeError("Argumentos devem ser números")
```

#### 3. Tratar None adequadamente:
```python
# Incorreto
valor = None
resultado = valor + 10  # TypeError

# Correto
valor = None
if valor is not None:
    resultado = valor + 10
else:
    resultado = 10
```

---

## IndexError

### O que é?
Erro que ocorre quando você tenta acessar um índice que não existe em uma lista.

### Exemplo:
```python
lista = [1, 2, 3]
print(lista[5])  # IndexError: list index out of range
```

### Principais Causas:
- Índice maior que o tamanho da lista
- Lista vazia
- Índice negativo além do range

### Como Resolver:

#### 1. Verificar tamanho da lista:
```python
lista = [1, 2, 3]
indice = 5

if indice < len(lista):
    print(lista[indice])
else:
    print("Índice fora do range")
```

#### 2. Usar try/except:
```python
lista = [1, 2, 3]
try:
    print(lista[5])
except IndexError:
    print("Índice não existe na lista")
```

#### 3. Verificar se lista não está vazia:
```python
if lista:  # Verifica se lista não está vazia
    primeiro_item = lista[0]
else:
    print("Lista está vazia")
```

---

## KeyError

### O que é?
Erro que ocorre quando você tenta acessar uma chave que não existe em um dicionário.

### Exemplo:
```python
dicionario = {"nome": "João", "idade": 30}
print(dicionario["profissao"])  # KeyError: 'profissao'
```

### Principais Causas:
- Chave não existe no dicionário
- Erro de digitação na chave
- Estrutura de dados diferente do esperado

### Como Resolver:

#### 1. Verificar se chave existe:
```python
dicionario = {"nome": "João", "idade": 30}

if "profissao" in dicionario:
    print(dicionario["profissao"])
else:
    print("Chave 'profissao' não encontrada")
```

#### 2. Usar método get():
```python
dicionario = {"nome": "João", "idade": 30}

# Com valor padrão
profissao = dicionario.get("profissao", "Não informado")
print(profissao)  # "Não informado"
```

#### 3. Usar try/except:
```python
try:
    print(dicionario["profissao"])
except KeyError:
    print("Chave não encontrada no dicionário")
```

---

## FileNotFoundError

### O que é?
Erro que ocorre quando o Python tenta abrir um arquivo que não existe.

### Exemplo:
```python
with open("arquivo_inexistente.txt", "r") as arquivo:
    conteudo = arquivo.read()
# FileNotFoundError: [Errno 2] No such file or directory: 'arquivo_inexistente.txt'
```

### Principais Causas:
- Arquivo não existe no caminho especificado
- Caminho incorreto
- Permissões insuficientes

### Como Resolver:

#### 1. Verificar se arquivo existe:
```python
import os

caminho_arquivo = "dados.txt"
if os.path.exists(caminho_arquivo):
    with open(caminho_arquivo, "r") as arquivo:
        conteudo = arquivo.read()
else:
    print(f"Arquivo {caminho_arquivo} não encontrado")
```

#### 2. Usar try/except:
```python
try:
    with open("dados.txt", "r") as arquivo:
        conteudo = arquivo.read()
except FileNotFoundError:
    print("Arquivo não encontrado. Verifique o caminho.")
```

#### 3. Usar caminhos absolutos:
```python
import os

# Caminho relativo (pode causar erro)
# arquivo = "dados/arquivo.txt"

# Caminho absoluto (mais seguro)
diretorio_atual = os.getcwd()
caminho_arquivo = os.path.join(diretorio_atual, "dados", "arquivo.txt")
```

#### 4. Criar arquivo se não existir:
```python
try:
    with open("dados.txt", "r") as arquivo:
        conteudo = arquivo.read()
except FileNotFoundError:
    print("Arquivo não encontrado. Criando arquivo vazio.")
    with open("dados.txt", "w") as arquivo:
        arquivo.write("")
```

---

## AttributeError

### O que é?
Erro que ocorre quando você tenta acessar um atributo ou método que não existe no objeto.

### Exemplo:
```python
lista = [1, 2, 3]
lista.append(4)  # OK
lista.add(5)     # AttributeError: 'list' object has no attribute 'add'
```

### Principais Causas:
- Método não existe para o tipo de objeto
- Objeto é None
- Confusão entre tipos de dados

### Como Resolver:

#### 1. Verificar documentação do tipo:
```python
# Para listas, use append(), não add()
lista = [1, 2, 3]
lista.append(4)  # Correto

# Para sets, use add(), não append()
conjunto = {1, 2, 3}
conjunto.add(4)  # Correto
```

#### 2. Verificar se objeto não é None:
```python
def obter_dados():
    # Pode retornar None em alguns casos
    return None

dados = obter_dados()
if dados is not None:
    resultado = dados.metodo()
else:
    print("Dados não disponíveis")
```

#### 3. Usar hasattr() para verificar atributos:
```python
objeto = [1, 2, 3]
if hasattr(objeto, 'append'):
    objeto.append(4)
else:
    print("Objeto não possui método append")
```

---

## IndentationError

### O que é?
Erro que ocorre quando a indentação (espaçamento) do código está incorreta.

### Exemplo:
```python
if True:
print("Hello")  # IndentationError: expected an indented block
```

### Principais Causas:
- Falta de indentação após :
- Mistura de tabs e espaços
- Indentação inconsistente

### Como Resolver:

#### 1. Sempre indentar após dois pontos:
```python
# Incorreto
if True:
print("Hello")

# Correto
if True:
    print("Hello")
```

#### 2. Usar apenas espaços (recomendado 4 espaços):
```python
# Configurar editor para mostrar espaços/tabs
# Usar sempre 4 espaços para indentação

def minha_funcao():
    if True:
        for i in range(3):
            print(i)
```

#### 3. Verificar alinhamento de blocos:
```python
# Incorreto
if True:
    print("Primeira linha")
  print("Segunda linha")  # IndentationError

# Correto
if True:
    print("Primeira linha")
    print("Segunda linha")
```

---

## SyntaxError

### O que é?
Erro que ocorre quando o código não segue a sintaxe correta do Python.

### Exemplo:
```python
print("Hello"  # SyntaxError: unexpected EOF while parsing
```

### Principais Causas:
- Parênteses, colchetes ou chaves não fechados
- Dois pontos ausentes
- Caracteres inválidos

### Como Resolver:

#### 1. Verificar parênteses balanceados:
```python
# Incorreto
print("Hello"
lista = [1, 2, 3

# Correto
print("Hello")
lista = [1, 2, 3]
```

#### 2. Adicionar dois pontos após estruturas de controle:
```python
# Incorreto
if True
    print("Hello")

# Correto
if True:
    print("Hello")
```

#### 3. Verificar aspas balanceadas:
```python
# Incorreto
texto = "Hello World'

# Correto
texto = "Hello World"
# ou
texto = 'Hello World'
```

---

## ImportError

### O que é?
Erro relacionado à importação de módulos, similar ao ModuleNotFoundError mas mais geral.

### Exemplo:
```python
from datetime import strptime_invalid  # ImportError: cannot import name 'strptime_invalid'
```

### Principais Causas:
- Função/classe não existe no módulo
- Versão incompatível do módulo
- Dependências circulares

### Como Resolver:

#### 1. Verificar nomes corretos das funções:
```python
# Incorreto
from datetime import strptime_invalid

# Correto
from datetime import datetime
# ou
import datetime
```

#### 2. Verificar versão dos módulos:
```bash
pip show pandas
pip install pandas==1.5.0  # versão específica
```

#### 3. Evitar importações circulares:
```python
# arquivo1.py
import arquivo2  # Evitar se arquivo2 importa arquivo1

# Solução: reestruturar código ou importar dentro de funções
def minha_funcao():
    import arquivo2
    return arquivo2.alguma_funcao()
```

---

## ZeroDivisionError

### O que é?
Erro que ocorre quando você tenta dividir um número por zero.

### Exemplo:
```python
resultado = 10 / 0  # ZeroDivisionError: division by zero
```

### Principais Causas:
- Divisão direta por zero
- Variável com valor zero usado como divisor
- Cálculos que resultam em zero

### Como Resolver:

#### 1. Verificar divisor antes da operação:
```python
dividendo = 10
divisor = 0

if divisor != 0:
    resultado = dividendo / divisor
else:
    print("Erro: Divisão por zero não é permitida")
    resultado = float('inf')  # ou outro valor padrão
```

#### 2. Usar try/except:
```python
try:
    resultado = 10 / 0
except ZeroDivisionError:
    print("Erro: Tentativa de divisão por zero")
    resultado = None
```

#### 3. Validar entrada do usuário:
```python
def dividir(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return "Erro: Divisão por zero não é permitida"

# Uso
resultado = dividir(10, 0)
print(resultado)
```

---

## Dicas Gerais para Evitar Erros

### 1. Use um Bom Editor/IDE
- VS Code com extensão Python
- PyCharm
- Jupyter Notebook para experimentação

### 2. Práticas de Debugging
```python
# Usar print() para debug
def minha_funcao(x):
    print(f"Debug: x = {x}, tipo = {type(x)}")
    return x * 2

# Usar assert para verificações
def dividir(a, b):
    assert b != 0, "Divisor não pode ser zero"
    return a / b
```

### 3. Validação de Dados
```python
def processar_idade(idade):
    # Validar tipo
    if not isinstance(idade, int):
        raise TypeError("Idade deve ser um número inteiro")
    
    # Validar valor
    if idade < 0 or idade > 150:
        raise ValueError("Idade deve estar entre 0 e 150 anos")
    
    return idade
```

### 4. Uso de Ferramentas de Linting
```bash
# Instalar pylint
pip install pylint

# Verificar código
pylint meu_arquivo.py

# Instalar black (formatador)
pip install black
black meu_arquivo.py
```

### 5. Tratamento Geral de Erros
```python
def operacao_segura():
    try:
        # Código que pode gerar erro
        resultado = operacao_perigosa()
        return resultado
    except ModuleNotFoundError as e:
        print(f"Módulo não encontrado: {e}")
    except ValueError as e:
        print(f"Valor inválido: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")
    
    return None
```

---

## Resumo dos Comandos Úteis

### Instalação de Módulos:
```bash
pip install nome_do_modulo
pip install --upgrade nome_do_modulo
pip list
pip show nome_do_modulo
```

### Debugging:
```python
# Verificar tipo
print(type(variavel))

# Verificar valor
print(repr(variavel))

# Verificar atributos
print(dir(objeto))

# Verificar se atributo existe
hasattr(objeto, 'atributo')
```

### Verificações Úteis:
```python
# Verificar se arquivo existe
import os
os.path.exists('arquivo.txt')

# Verificar se é número
texto.isdigit()

# Verificar se lista não está vazia
if lista:

# Verificar se variável não é None
if variavel is not None:
```

Lembre-se: a maioria dos erros em Python são fáceis de resolver uma vez que você entende o que eles significam. Use as mensagens de erro como guia - elas geralmente indicam exatamente onde e qual é o problema!
