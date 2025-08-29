# Usa Selenium para raspar o Brasil Paralelo
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
import pandas as pd
from bs4 import BeautifulSoup

chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")  # abre a janela maximizada

# O WebDriver Manager baixa e configura o driver automaticamente
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

driver.get("https://www.brasilparalelo.com.br/search?query=woke")
time.sleep(3)

source = driver.page_source

soup = BeautifulSoup(source, "lxml")

divs = soup.find_all("div", {'class': 'search-result-item'})
noticias = []

for item in divs:
    link = item.find("a", {'class': 'link-block-12'}).get('href')
    link = 'https://www.brasilparalelo.com.br' + link
    titulo = item.find('h2').get_text(strip=True)
    intro = item.find('p').get_text(strip=True)
    noticias.append({
        'link': link,
        'titulo': titulo,
        'intro': intro
    })

df = pd.DataFrame(noticias)
df.to_csv('noticias.csv', index=False)

print(df)
time.sleep(10)

driver.quit()