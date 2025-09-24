from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOption


from webdriver_manager.microsoft import EdgeChromiumDriverManager


from bs4 import BeautifulSoup


import pandas as pd


import requests


from tqdm import tqdm


import time
from urllib.parse import urljoin, urlparse

edge_options = EdgeOption()
edge_options.add_argument("--start-maximized")  


service = EdgeService()
options = EdgeOption()
driver = webdriver.Edge(service=service, options=options)
artista= 'lana del rey'
driver.get("https://www.letras.mus.br")
time.sleep(2) 
caixa_pesquisa = driver.find_element(By.ID, "headerInput")
time.sleep(2)

caixa_pesquisa.send_keys(artista)
time.sleep(2)
artista= driver.find_element(By.CLASS_NAME, "suggest-artist")
time.sleep(2)
artista.click()

soup=BeautifulSoup(driver.page_source, 'html.parser')
musicas=soup.find_all("a", class_="songList-table-songName")

lista_musicas=[]
for musica in musicas:
    base= driver.current_url
    titulo=musica.get_text(strip=True)
    href=musica.get('href')
    if href:
        href=urljoin(base, href)
    lista_musicas.append({'titulo':titulo, 'link': href})

resultado=[] #dnjnsdisji
for musica in tqdm(lista_musicas):
    html_musica=requests.get(musica['link']).text
    soup=BeautifulSoup(html_musica, 'html.parser')

    letra_el=soup.select_one("div.lyric-original")
    views_el=soup.select_one("b.font.--base.--strong.--size16.u-block")
    comp_el=soup.select_one("div.lyric-info-composition")

    resultado.append({
        'titulo': musica['titulo'],
        'link': musica['link'],
        'letra': letra_el.get_text(separator="\n").strip() if letra_el else None,
        'views': views_el.get_text().strip() if views_el else None,
        'composição': comp_el.get_text(separator="\n").strip() if comp_el else None
        'extracted_at': time.strftime("%Y-%m-%d %H:%M:%S")
    })

df=pd.DataFrame(resultado)
csv_name= 'lana_del_rey_letras.csv'
df.to_csv(csv_name, index=False, encoding='utf-8')
print(f"Arquivo salvo como {csv_name}")

