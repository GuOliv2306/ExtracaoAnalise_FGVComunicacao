from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOption

# Gerenciamento automático de drivers
from webdriver_manager.microsoft import EdgeChromiumDriverManager

# Parsing HTML
from bs4 import BeautifulSoup

# Manipulação de dados
import pandas as pd

# Requisições HTTP
import requests

# Barra de progresso
from tqdm import tqdm

# Utilitários
import time
from urllib.parse import urljoin, urlparse

edge_options = EdgeOption()
edge_options.add_argument("--start-maximized")  # abre a janela maximizada

# O WebDriver Manager baixa e configura o driver automaticamente
service = EdgeService()
options = EdgeOption()
driver = webdriver.Edge(service=service, options=options)

driver.get("https://www.letras.mus.br")
time.sleep(2) 

caixa_pesquisa = driver.find_element(By.ID, "headerInput")
time.sleep(2)    # espera 2 segundos para a página carregar

caixa_pesquisa.send_keys('Coldplay')
time.sleep(1)
artista= driver.find_element(By.CLASS_NAME, "suggest-artist")
artista.click()

soup=BeautifulSoup(driver.page_source, 'html.parser')
musicas=soup.find_all("a", class_="songList-table-songName")

lista_musicas=[]
for musica in musicas:
    base= driver.current_url
    titulo=musica.get_text().strip()
    href=musica.get('href')
    if href:
        href=urljoin(base, href)
    lista_musicas.append({'titulo': titulo, 'link': href})

resultado=[]
for musica in tqdm(lista_musicas):
    html_musica=requests.get(musica['link']).text
    soup=BeautifulSoup(html_musica, 'html.parser')

    letra_el=soup.select_one("div.lyric-original")
    views_el=soup.select_one("b.font.--base.--strong.--size16.u-block")
    comp_el=soup.select_one("div.lyric-info-composition")

    resultado.append({
        'titulo': musica['titulo'],
        'url': musica['link'],
        'letra': letra_el.get_text(separator="\n").strip() if letra_el else None,
        'views': views_el.get_text().strip() if views_el else None,
        'composicao': comp_el.get_text().strip() if comp_el else None,
        'extracted_at': time.strftime("%Y-%m-%d %H:%M:%S")
    })

csv_filename = "coldplay_letras.csv"
df = pd.DataFrame(resultado)
df.to_csv(csv_filename, index=False, encoding='utf-8')