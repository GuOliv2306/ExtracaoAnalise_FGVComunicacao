Guia de Estudos: Fundamentos do Scikit-learn para Machine Learning
O Scikit-learn é uma das bibliotecas mais poderosas e populares para Machine Learning em Python. A sua força reside numa API consistente, numa vasta gama de ferramentas e na simplificação do fluxo de trabalho, desde a preparação dos dados até à avaliação de modelos. Neste guia, vamos explorar cinco componentes essenciais: OneHotEncoder, StandardScaler, PCA, KMeans e LDA.

1. Pré-processamento de Dados: A Base Essencial
Modelos de Machine Learning raramente funcionam bem com dados brutos ("raw data"). É crucial transformá-los num formato numérico, limpo e bem-escalonado para que os algoritmos possam extrair padrões de forma eficiente.

a) OneHotEncoder: Transformando Variáveis Categóricas
Variáveis categóricas representam categorias ou rótulos (ex: "cor", "cidade", "tipo de produto"). Como os algoritmos se baseiam em operações matemáticas, eles não conseguem processar texto diretamente. O OneHotEncoder resolve este problema ao converter categorias em vetores numéricos binários.

Conceito: Para cada categoria única numa coluna, é criada uma nova coluna (ou "feature"). Se uma amostra (linha) pertence a essa categoria, o valor na nova coluna correspondente é 1; caso contrário, é 0. Este processo evita que o modelo interprete erradamente as categorias como tendo uma ordem ou magnitude (ex: "vermelho" < "verde" < "azul").

Exemplo Prático e Código:

Vamos usar um dataset simples de animais para ilustrar o conceito.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import OneHotEncoder

# --- Dados de Exemplo ---
data = {'animal': ['gato', 'cão', 'gato', 'pássaro', 'cão', 'gato'],
        'origem': ['doméstico', 'doméstico', 'selvagem', 'selvagem', 'doméstico', 'doméstico']}
df = pd.DataFrame(data)

print("--- DataFrame Original ---")
print(df)

# --- Visualização dos Dados Originais (Opcional) ---
# Mostra a contagem de cada categoria antes da transformação.

# --- Aplicação do OneHotEncoder ---
encoder = OneHotEncoder(sparse_output=False)
one_hot_encoded = encoder.fit_transform(df[['animal', 'origem']])
feature_names = encoder.get_feature_names_out(['animal', 'origem'])
df_encoded = pd.DataFrame(one_hot_encoded, columns=feature_names, dtype=int)

print("\n--- DataFrame Transformado (OneHotEncoded) ---")
print(df_encoded)

Resultado e Análise:
O OneHotEncoder criou novas colunas binárias para cada categoria única em animal e origem. Agora, os dados estão num formato puramente numérico, pronto para serem usados por um modelo de Machine Learning.

b) StandardScaler: Normalizando a Escala das Features
Algoritmos que se baseiam em distâncias (como KMeans, SVM) ou gradientes (como regressão linear e redes neurais) são sensíveis à escala das features. Se uma feature (ex: salário, em milhares) tiver uma magnitude muito maior que outra (ex: idade, em dezenas), a primeira dominará o cálculo da distância, distorcendo o resultado.

Conceito: O StandardScaler transforma os dados para que tenham uma média de 0 e um desvio padrão de 1. A fórmula aplicada a cada valor x é:

$$ z = \frac{(x - \mu)}{\sigma} $$

Onde μ é a média da feature e σ é o desvio padrão. Este processo é chamado de padronização.

Exemplo Prático e Código:

Vamos criar dados sintéticos de idade e salário para ver o efeito do StandardScaler.

from sklearn.preprocessing import StandardScaler

# --- Dados de Exemplo com Escalas Diferentes ---
np.random.seed(42)
data_escala = {
    'idade': np.random.randint(20, 65, size=100),
    'salario_anual': np.random.randint(30000, 150000, size=100)
}
df_escala = pd.DataFrame(data_escala)

# --- Aplicação do StandardScaler ---
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_escala)
df_scaled = pd.DataFrame(scaled_data, columns=['idade_scaled', 'salario_scaled'])

print("\n--- Estatísticas Antes da Padronização ---")
print(df_escala.describe())
print("\n--- Estatísticas Depois da Padronização ---")
print(df_scaled.describe())

Análise:
As estatísticas confirmam que, após a padronização, a média de cada coluna está próxima de 0 e o desvio padrão próximo de 1, colocando ambas as features na mesma escala de importância.

2. Redução de Dimensionalidade
Trabalhar com muitas features (alta dimensionalidade) pode ser computacionalmente caro e levar a overfitting. Técnicas de redução de dimensionalidade ajudam a projetar os dados num espaço de menor dimensão, preservando o máximo de informação relevante possível.

a) PCA (Principal Component Analysis)
O PCA é uma técnica não supervisionada que transforma um conjunto de variáveis possivelmente correlacionadas num conjunto de variáveis linearmente não correlacionadas chamadas componentes principais.

Conceito: O PCA encontra as direções (eixos) no espaço de dados onde a variância é máxima. O primeiro componente principal (PC1) é o eixo que captura a maior parte da variância dos dados. O PC2 é o próximo eixo, ortogonal (perpendicular) ao PC1, que captura a maior parte da variância restante, e assim por diante. Ao selecionar apenas os primeiros k componentes, podemos reduzir a dimensão dos dados, mantendo a maior parte da sua estrutura.

Exemplo Prático com o Dataset Iris:

O dataset Iris tem 4 features. Usaremos o PCA para reduzi-lo para 2, de forma a podermos visualizá-lo num gráfico 2D.

from sklearn.decomposition import PCA
from sklearn.datasets import load_iris

# --- Carregar Dados ---
iris = load_iris()
X = iris.data
y = iris.target
# É crucial escalar os dados ANTES de aplicar o PCA
X_scaled = StandardScaler().fit_transform(X)

# --- Aplicação do PCA ---
# Reduzir para 2 componentes principais
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

# --- Análise dos Componentes ---
print(f"Variância explicada por cada componente: {pca.explained_variance_ratio_}")
print(f"Variância total explicada pelos 2 componentes: {sum(pca.explained_variance_ratio_):.2f}%")

# --- Visualização (código omitido, mas geraria um gráfico de dispersão) ---
# Um scatter plot de PC1 vs. PC2 mostraria as 3 classes de flores bem separadas.

Análise:
Mesmo reduzindo de 4 para 2 dimensões, os dois componentes principais conseguiram capturar mais de 95% da variância original. Uma visualização mostraria que, neste novo espaço 2D, as três espécies de flores estão claramente separadas.

3. Clustering e Análise de Grupos
Clustering é uma tarefa de Machine Learning não supervisionada que visa agrupar dados semelhantes. O objetivo é que os pontos de dados no mesmo grupo (cluster) sejam mais semelhantes entre si do que com os de outros grupos.

a) KMeans
O KMeans é um dos algoritmos de clustering mais populares. Ele particiona os dados em K clusters distintos, onde cada ponto de dado pertence ao cluster com a média (centroide) mais próxima.

Conceito (Algoritmo):

Inicialização: Escolha K pontos aleatórios como centroides iniciais.

Atribuição: Atribua cada ponto de dado ao centroide mais próximo.

Atualização: Recalcule a posição de cada centroide como a média de todos os pontos de dados atribuídos a ele.

Repetição: Repita os passos 2 e 3 até que os centroides não mudem mais de posição (convergência).

Exemplo Prático com Dados Sintéticos:

Usaremos make_blobs para criar dados com agrupamentos claros e aplicar o KMeans.

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

# --- Gerar Dados Sintéticos ---
X_blobs, y_blobs = make_blobs(n_samples=300, centers=4, cluster_std=0.7, random_state=42)

# --- Aplicação do KMeans ---
kmeans = KMeans(n_clusters=4, random_state=42, n_init='auto')
y_kmeans = kmeans.fit_predict(X_blobs)

# --- Visualização (código omitido) ---
# Um gráfico de dispersão colorindo os pontos por y_kmeans e marcando
# os centroides mostraria 4 grupos bem definidos.

Análise:
O KMeans identifica com sucesso os 4 clusters nos dados, encontrando os centros de cada grupo e atribuindo corretamente cada ponto ao seu cluster correspondente.

4. Classificação e Separação de Classes
Enquanto o PCA é não supervisionado, existem técnicas de redução de dimensionalidade que usam as etiquetas (labels) dos dados para encontrar uma projeção que maximize a separabilidade entre as classes.

a) LDA (Linear Discriminant Analysis)
O LDA é uma técnica supervisionada usada tanto para redução de dimensionalidade quanto para classificação.

Conceito (LDA vs. PCA):

PCA: Encontra os eixos de máxima variância nos dados, ignorando as classes.

LDA: Encontra os eixos (discriminantes lineares) que maximizam a separação entre múltiplas classes.

O número máximo de componentes que o LDA pode encontrar é min(n_classes - 1, n_features).

Exemplo Prático com o Dataset Iris:

Vamos aplicar o LDA para reduzir o dataset Iris para 1 dimensão.

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

# Reutilizando os dados do Iris (X_scaled e y)
lda = LinearDiscriminantAnalysis(n_components=1)
X_lda = lda.fit_transform(X_scaled, y) # LDA é supervisionado, então passamos 'y'

# --- Visualização (código omitido) ---
# Um gráfico de distribuição 1D (como stripplot) mostraria as
# projeções dos pontos de cada classe sobre um único eixo.

Análise Final:
O LDA projeta os dados de 4D para 1D de uma forma que maximiza a separação entre as classes. Uma visualização mostraria que, mesmo nesta única dimensão, as três classes de flores estão notavelmente bem separadas, demonstrando a eficácia do LDA para tarefas de separação de classes.