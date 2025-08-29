# ---------------------------
# IMPORTS BÁSICOS
# ---------------------------
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# WebDriver Manager para Edge
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions

# ---------------------------
# CONFIGURAÇÃO DO DRIVER
# ---------------------------
chrome_options = ChromeOptions()
chrome_options.add_argument("--start-maximized")  # abre a janela maximizada

# O WebDriver Manager baixa e configura o driver automaticamente
service = ChromeService(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# Se quiser usar o Edge, basta substituir o Chrome pelo Edge
# edge_options = EdgeOptions()
# edge_options.add_argument("--start-maximized")  # abre a janela maximizada
# service = EdgeService(EdgeChromiumDriverManager().install())
# driver = webdriver.Edge(service=service, options=edge_options)

# ---------------------------
# ACESSANDO O SITE
# ---------------------------
driver.get("https://www.google.com")
time.sleep(5)

# ---------------------------
# ACESSANDO A AMAZON
# ---------------------------
driver.get("https://www.amazon.com.br")
time.sleep(5)

# ---------------------------
# LOCALIZANDO ELEMENTOS 
# ---------------------------
caixa_pesquisa = driver.find_element(By.ID, "twotabsearchtextbox")
time.sleep(1)

# ---------------------------
# INSERINDO O TEXTO NA CAIXA DE PESQUISA
# ---------------------------
caixa_pesquisa.send_keys("iphone 15")
time.sleep(1)

# ---------------------------
# CLICANDO NO BOTÃO DE BUSCA
# ---------------------------
botao_pesquisa = driver.find_element(By.ID, "nav-search-submit-button")
botao_pesquisa.click()
time.sleep(5)

# ---------------------------
# USANDO BEAUTIFULSOUP PARA PEGAR TODOS OS CELULARES DA PAGINA
# ---------------------------
from bs4 import BeautifulSoup

soup = BeautifulSoup(driver.page_source, "lxml")

celulares = soup.find_all("div", {'class': 'desktop-grid-content-view'})

print(celulares)
time.sleep(10)

# ---------------------------
# FECHANDO O DRIVER
# ---------------------------
driver.quit()