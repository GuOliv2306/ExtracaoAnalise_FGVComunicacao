## Lab de Extração e Análise de Dados — FGV Comunicação Rio

Repositório oficial de materiais e códigos da disciplina de Extração e Análise de Dados (FGV Comunicação Rio). Aqui você encontrará o conteúdo organizado por aula e as bases de dados utilizadas durante o curso.

- Repositório original: `https://github.com/mateuspestana/ExtracaoAnalise_FGVComunicacao`

> 🔒 **Quer tornar este repositório privado?** Consulte o guia completo: [COMO_TORNAR_REPOSITORIO_PRIVADO.md](./COMO_TORNAR_REPOSITORIO_PRIVADO.md)

### Estrutura do repositório

- `aula_XX/`: pasta de cada aula, com códigos, notebooks e materiais de suporte
  - Exemplo: `aula_04/` corresponde à quarta aula
- `bases/`: bases de dados usadas nas aulas (arquivos como `.csv`, `.json`, `.ndjson`, etc.)
- Outros arquivos auxiliares podem aparecer na raiz (ex.: `requirements.py`, scripts utilitários, etc.)

### Guia de Terminal (VS Code)

Se você está começando no terminal, consulte os guias passo a passo (com foco em Windows PowerShell e alternativas para macOS/Linux):

- [01 — Conceitos básicos do terminal](./aula_terminal/01_conceitos_basicos_terminal.md)
- [02 — Navegação e manipulação de arquivos](./aula_terminal/02_navegacao_arquivos.md)
- [03 — Python: venv, pip e execução de scripts (no VS Code)](./aula_terminal/03_python_venv_execucao.md)
- [04 — Git essencial para o curso (no VS Code)](./aula_terminal/04_git_essencial.md)
- [05 — Resolução de problemas comuns (no VS Code)](./aula_terminal/05_resolucao_problemas.md)

### Como clonar este repositório (somente leitura)

Caso você tenha apenas permissão de leitura no repositório:

```bash
git clone https://github.com/mateuspestana/ExtracaoAnalise_FGVComunicacao
cd ExtracaoAnalise_FGVComunicacao
```

Repositório original: `https://github.com/mateuspestana/ExtracaoAnalise_FGVComunicacao`

Observação: os comandos `git` são os mesmos em macOS, Linux e Windows. No Windows, você pode usar o PowerShell ou o Git Bash (instalado com o Git for Windows).

### Como obter atualizações do professor

- **Se você clonou diretamente o repositório original (somente leitura):**

```bash
git pull
```

### Fluxo recomendado: trabalhar com fork (recomendado)

O fork permite que você tenha um repositório próprio no seu GitHub para anotações e modificações, sem afetar o repositório original do professor.

1) No GitHub, clique em "Fork" para criar uma cópia na sua conta.

2) Clone o seu fork localmente:

```bash
git clone <URL_DO_SEU_FORK>
cd ExtracaoAnalise_FGVComunicacao
```

Exemplo de URL do seu fork:

```text
https://github.com/SEU_USUARIO/ExtracaoAnalise_FGVComunicacao
```

3) Configure o remoto `upstream` para acompanhar o repositório do professor:

```bash
git remote add upstream https://github.com/mateuspestana/ExtracaoAnalise_FGVComunicacao
git remote -v
```

4) Para trazer novidades do professor e mantê-las no seu fork:

```bash
git fetch upstream
git checkout main
git pull --rebase upstream main
git push origin main
```

5) Para trabalhar nas suas anotações/códigos, crie branches no seu fork:

```bash
git checkout -b minhas-anotacoes-aula04
# edite arquivos...
git add .
git commit -m "Minhas anotações da aula 04"
git push -u origin minhas-anotacoes-aula04
```

Observação: você não precisa abrir Pull Request para o repositório do professor. O fork funciona como seu caderno de estudos.

#### Conceitos rápidos: Fork e Upstream

- **Fork**: é uma cópia do repositório do professor na sua conta do GitHub. Você tem controle total sobre esse repositório (o seu), pode criar branches, commits e enviar para o seu remoto (`origin`). O fork não altera o repositório original.
- **Upstream**: é um apelido (remoto Git) que aponta para o repositório original do professor. Usamos `upstream` para buscar as novidades do professor e trazê-las para o seu repositório local/fork. Em resumo: `origin` = seu fork; `upstream` = repositório do professor.

### Como criar seu repositório de anotações (sem alterar o original)

Opção alternativa (mais simples): para evitar qualquer alteração neste repositório, mantenha suas anotações em um repositório próprio de uso pessoal. Fluxo sugerido:

1) Atualize este repositório sempre que houver novidades:

```bash
cd /caminho/para/LabExtracaoAnalise2025
git pull
```

2) Crie um diretório separado para o seu repositório de anotações e inicialize o Git:

```bash
mkdir -p /caminho/para/MinhasAnotacoesDados
cd /caminho/para/MinhasAnotacoesDados
git init
git branch -M main
```

3) Copie os arquivos do repositório da disciplina para o seu repositório de anotações, sem mover nem apagar nada no original.

macOS/Linux:

```bash
rsync -av --exclude='.git' --exclude='.venv' /caminho/para/LabExtracaoAnalise2025/ .
```

Windows (PowerShell):

```powershell
robocopy "C:\caminho\LabExtracaoAnalise2025" "." /E /XD .git .venv
```

4) Faça seu primeiro commit no repositório de anotações:

```bash
git add .
git commit -m "Anotações iniciais copiadas do repositório da disciplina"
```

5) Sempre que houver novidades no repositório da disciplina, repita os passos 1 e 3 para copiar novamente (apenas adicionando/atualizando arquivos). Em seguida, faça novos commits no seu repositório de anotações.

Observação: se preferir, você pode baixar o ZIP do repositório da disciplina e extrair o conteúdo dentro do seu repositório de anotações. Certifique-se de não copiar a pasta oculta `.git` do repositório da disciplina.

### Ambiente e dependências (sempre instalar requirements)

Use um ambiente virtual dedicado e instale as dependências listadas. Recomendamos `.venv`.

#### O que é um ambiente virtual (venv)?

- **`venv`** é um ambiente isolado de Python para um projeto específico. Dentro dele ficam as bibliotecas que você instala com `pip`.
- **Por que usar:**
  - Evita conflitos de versão entre projetos diferentes no seu computador
  - Melhora a reprodutibilidade: todos usam as mesmas versões definidas em `requirements.py`
  - Dispensa permissões de administrador (instala tudo localmente)
  - Mantém seu sistema organizado, sem “poluir” o Python global
- **Onde fica:** normalmente em uma pasta chamada `.venv` dentro do projeto. Não é necessário versionar essa pasta.

#### Como criar e ativar o `venv`

macOS/Linux:

```bash
# Dentro do seu repositório (disciplina ou anotações)
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.py
```

Windows (PowerShell):

```powershell
# Dentro do seu repositório (disciplina ou anotações)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.py
```

Windows (Git Bash):

```bash
# Dentro do seu repositório (disciplina ou anotações)
python -m venv .venv
source .venv/Scripts/activate
pip install --upgrade pip
pip install -r requirements.py
```

Se o PowerShell bloquear a ativação do ambiente, execute uma vez:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned -Force
```

- Sempre que você atualizar os arquivos do curso (ex.: depois de um `git pull`), rode novamente:

```bash
pip install -r requirements.py
```

Para desativar o ambiente virtual em qualquer sistema, use:

```bash
deactivate
```

### Como atualizar em casa e na faculdade

Se você usa fork (recomendado):

Em cada computador (casa e faculdade), após clonar o seu fork, faça regularmente:

```bash
cd <pasta-do-seu-clone-do-fork>
git checkout main
git pull origin main          # traz o que já está no seu fork
git fetch upstream            # busca novidades do professor
git pull --rebase upstream main
git push origin main          # sincroniza seu fork remoto

# Reative o ambiente e reinstale dependências
# macOS/Linux
source .venv/bin/activate
pip install -r requirements.py

# Windows (PowerShell)
.\.venv\Scripts\Activate.ps1
pip install -r requirements.py
```

Se você usa o repositório de anotações (cópia):

- Mantenha dois diretórios: `LabExtracaoAnalise2025` (somente leitura) e `MinhasAnotacoesDados` (seu repositório de anotações).
- Para atualizar:
  1) No diretório da disciplina, rode `git pull`.
  2) Copie novamente para o seu repositório de anotações.

macOS/Linux:

```bash
rsync -av --exclude='.git' --exclude='.venv' /caminho/para/LabExtracaoAnalise2025/ /caminho/para/MinhasAnotacoesDados/
```

Windows (PowerShell):

```powershell
robocopy "C:\caminho\LabExtracaoAnalise2025" "C:\caminho\MinhasAnotacoesDados" /E /XD .git .venv
```

Depois da cópia, faça `git add`, `git commit` no seu repositório de anotações e reinstale os requirements no `.venv` daquele repositório.

### Observações

- Mantenha as bases de dados na pasta `bases/` para facilitar a organização e o versionamento.
- Cada aula terá sua própria pasta (`aula_01/`, `aula_02/`, …, `aula_04/`, etc.).
- Se o professor disponibilizar dependências de Python, elas serão indicadas na raiz do projeto (por exemplo, em `requirements.py`/`requirements.txt`). Utilize um ambiente virtual (`.venv`) ao instalar pacotes para isolar as dependências do curso do seu sistema.


