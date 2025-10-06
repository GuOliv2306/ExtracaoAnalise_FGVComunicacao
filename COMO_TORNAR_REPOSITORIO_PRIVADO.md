# 🔒 Como Tornar este Repositório Privado

## Instruções Passo a Passo

### Método 1: Alterar Visibilidade no GitHub (Recomendado)

1. **Acesse seu repositório no GitHub:**
   - Vá para: https://github.com/GuOliv2306/ExtracaoAnalise_FGVComunicacao

2. **Acesse as Configurações:**
   - Clique na aba **"Settings"** (Configurações)
   - Role até o final da página

3. **Altere a Visibilidade:**
   - Na seção **"Danger Zone"** (Zona de Perigo)
   - Clique em **"Change repository visibility"**
   - Selecione **"Make private"**
   - Digite o nome do repositório para confirmar: `GuOliv2306/ExtracaoAnalise_FGVComunicacao`
   - Clique em **"I understand, change repository visibility"**

### ⚠️ Importante Saber

**Limitações de Repositórios Privados:**
- Contas gratuitas do GitHub têm limite de colaboradores em repositórios privados
- Algumas funcionalidades podem ter restrições

**O que acontece quando você torna o repositório privado:**
- ✅ Apenas você e colaboradores autorizados podem ver o código
- ✅ O repositório não aparece em buscas públicas
- ✅ Links públicos param de funcionar para usuários não autorizados
- ❌ O professor não conseguirá mais ver suas anotações (a menos que você o adicione como colaborador)

## Alternativas para Trabalho Privado

### Método 2: Criar Repositório Totalmente Privado (Recomendado para Anotações)

Se você quer manter suas anotações privadas mas ainda receber atualizações do professor:

1. **Crie um novo repositório privado:**
   - No GitHub, clique em "+" → "New repository"
   - Nome: `MinhasAnotacoes_ExtracaoAnalise`
   - ✅ Marque "Private"
   - ✅ Adicione README

2. **Clone seus dois repositórios:**
```bash
# Clone o repositório do curso (público)
git clone https://github.com/mateuspestana/ExtracaoAnalise_FGVComunicacao curso_original

# Clone seu repositório privado
git clone https://github.com/GuOliv2306/MinhasAnotacoes_ExtracaoAnalise minhas_anotacoes
```

3. **Copie os arquivos quando necessário:**
```bash
# Copiar nova aula do curso original
cp -r curso_original/aula_XX/ minhas_anotacoes/

# Fazer suas modificações em minhas_anotacoes/
cd minhas_anotacoes
# ... fazer alterações ...

git add .
git commit -m "Minhas anotações da aula XX"
git push
```

### Método 3: Usar Branches Privadas

Mantenha o repositório público mas crie branches privadas:

```bash
# Criar branch para suas anotações
git checkout -b minhas-anotacoes

# Fazer suas modificações
# ... editar arquivos ...

git add .
git commit -m "Minhas anotações privadas"
git push origin minhas-anotacoes
```

## Recomendação Final

**Para máxima flexibilidade, recomendo:**

1. **Manter este fork público** para receber atualizações do professor
2. **Criar um repositório separado e privado** para suas anotações pessoais
3. **Copiar arquivos quando necessário** entre os dois repositórios

Isso permite:
- ✅ Receber atualizações do curso
- ✅ Manter anotações privadas
- ✅ Compartilhar código específico quando necessário
- ✅ Não perder acesso ao material original

## Precisa de Ajuda?

Se encontrar dificuldades, verifique:
- Você tem permissões de admin no repositório?
- Sua conta GitHub permite repositórios privados?
- Você realmente quer tornar TODO o conteúdo privado?

**Lembre-se:** Uma vez privado, outras pessoas (incluindo o professor) não conseguirão ver seu trabalho a menos que você os adicione como colaboradores.