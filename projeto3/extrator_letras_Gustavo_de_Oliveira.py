# Automação web
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOption
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Gerenciamento automático de drivers

# Parsing HTML
from bs4 import BeautifulSoup

# Manipulação de dados
import pandas as pd

# Requisições HTTP
import requests

# Crud
import customtkinter as ctk
import tkinter as tk

# Barra de progresso

# Utilitários
import time
from urllib.parse import urljoin, urlparse
import re, os
from threading import Thread

# A automação inicia apenas quando o usuário clicar em "Pesquisar" no painel.

# --- Utilidades anti-popups/abas ---
def _normaliza_janela_letras(driver):
    """Garante que estamos na aba do letras.mus.br e fecha abas externas comuns de propaganda."""
    try:
        handles = list(driver.window_handles)
    except Exception:
        return
    alvo = None
    for h in handles:
        try:
            driver.switch_to.window(h)
            url = driver.current_url
        except Exception:
            continue
        if "letras.mus.br" in (url or ""):
            alvo = h
            break
    # Se houver mais de uma janela e achamos a do letras, fechamos externas
    if alvo and len(handles) > 1:
        for h in list(driver.window_handles):
            if h == alvo:
                continue
            try:
                driver.switch_to.window(h)
                url = driver.current_url
                if "letras.mus.br" not in (url or ""):
                    try:
                        driver.close()
                    except Exception:
                        pass
            except Exception:
                pass
        try:
            driver.switch_to.window(alvo)
        except Exception:
            pass

def _tenta_fechar_popups(driver):
    """Fecha popups/modais genéricos e consentimentos simples (resiliente, silencioso)."""
    try:
        seletores = [
            "button[aria-label='Fechar']",
            "button[aria-label='Close']",
            "button[title='Fechar']",
            "button[class*='close']",
            "div[role='dialog'] button",
            "[class*='modal'] button",
            "[class*='popup'] button",
        ]
        for sel in seletores:
            try:
                for el in driver.find_elements(By.CSS_SELECTOR, sel):
                    try:
                        if el.is_displayed() and el.is_enabled():
                            el.click(); time.sleep(0.15)
                    except Exception:
                        pass
            except Exception:
                pass

        textos = {"fechar", "aceitar", "aceito", "continuar", "ok", "concordo", "prosseguir"}
        for b in driver.find_elements(By.TAG_NAME, "button"):
            try:
                t = (b.text or "").strip().lower()
                if t in textos and b.is_displayed() and b.is_enabled():
                    b.click(); time.sleep(0.15)
            except Exception:
                pass
    except Exception:
        pass

def _remove_overlays_com_js(driver):
    """Remove overlays/modais/iframes de domínios externos via JavaScript sem quebrar a página."""
    js = """
    (function(){
      const sels = ['[role=dialog]','[id*=modal]','[class*=modal]','[class*=popup]','[class*=overlay]'];
      for (const sel of sels) {
        try { document.querySelectorAll(sel).forEach(e => e.remove()); } catch(e){}
      }
      try {
        document.querySelectorAll('iframe').forEach(ifr => {
          const src = (ifr.getAttribute('src')||'').toLowerCase();
          if (src && src.indexOf('letras.mus.br') === -1) {
            ifr.parentNode && ifr.parentNode.removeChild(ifr);
          }
        });
      } catch(e){}
    })();
    """
    try:
        driver.execute_script(js)
    except Exception:
        pass

def _aceita_cookies_conhecidos(driver):
    """Clica em botões de consentimento (cookies) mais comuns (OneTrust, Didomi, Quantcast)."""
    try:
        sels = [
            "#onetrust-accept-btn-handler",
            "button#onetrust-accept-btn-handler",
            "button[aria-label='Aceitar']",
            "button[aria-label='Aceitar todos']",
            "button[aria-label='Accept All']",
            "button[mode='accept']",
            ".qc-cmp2-summary-buttons button[mode='accept']",
            "button.didomi-accept-button",
            "button.didomi-approve-button",
            "button[title='Aceitar']",
            "button[title='Aceitar todos']",
        ]
        for sel in sels:
            try:
                for el in driver.find_elements(By.CSS_SELECTOR, sel):
                    try:
                        if el.is_displayed() and el.is_enabled():
                            el.click(); time.sleep(0.15)
                    except Exception:
                        pass
            except Exception:
                pass

        palavras = ["aceitar", "aceitar todos", "accept all", "consentir", "ok", "prosseguir"]
        for b in driver.find_elements(By.TAG_NAME, "button"):
            try:
                tx = (b.text or "").strip().lower()
                if any(p in tx for p in palavras) and b.is_displayed() and b.is_enabled():
                    b.click(); time.sleep(0.15)
            except Exception:
                pass
    except Exception:
        pass

def _garante_contexto_pos_click(driver, timeout=12, tentativas=2):
    """Após o clique no artista, garante que estamos na lista de músicas do letras, com retries."""
    for _ in range(tentativas):
        _normaliza_janela_letras(driver)
        _tenta_fechar_popups(driver)
        _aceita_cookies_conhecidos(driver)
        _remove_overlays_com_js(driver)
        # Se caiu em domínio externo na mesma aba, tenta voltar
        try:
            host = urlparse(driver.current_url).netloc
            if 'letras.mus.br' not in host:
                driver.back()
                time.sleep(0.7)
        except Exception:
            pass
        # Espera a lista de músicas aparecer
        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.songList-table-songName"))
            )
            return True
        except Exception:
            # Tenta um pequeno scroll para disparar lazy load
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3)")
                time.sleep(0.3)
                driver.execute_script("window.scrollTo(0, 0)")
            except Exception:
                pass
    return False


def scrape_letras(artista_nome: str, hooks=None):
    """
    Executa a automação e o scraping para o artista informado.
    hooks: dict opcional com callbacks:
        - on_total(total)
        - on_musica(titulo, idx, total)
        - on_done(csv_path)
        - on_error(msg)
        - on_status(msg)
    """
    driver = None
    try:
        # Cria o driver apenas quando a coleta é iniciada pela UI
        edge_options = EdgeOption()
        edge_options.add_argument("--start-maximized")
        # Reduz algumas interrupções comuns
        edge_options.add_argument("--disable-notifications")
        edge_options.add_argument("--disable-popup-blocking")
        edge_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        edge_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.cookies": 1,
            "profile.default_content_setting_values.popups": 0,
            "profile.default_content_setting_values.notifications": 2,
        })
        service = EdgeService()
        driver = webdriver.Edge(service=service, options=edge_options)
        # Início da automação (mantendo a base do seu código)
        driver.get("https://www.letras.mus.br")
        time.sleep(2)

        caixa_pesquisa = driver.find_element(By.ID, "headerInput")
        time.sleep(2)  # espera 2 segundos para a página carregar

        caixa_pesquisa.clear()
        caixa_pesquisa.send_keys(artista_nome)
        time.sleep(1)
        artista = driver.find_element(By.CLASS_NAME, "suggest-artist")
        artista.click()
        # Anti-ads: se anúncio atrapalhar, reescreve o artista e tenta novamente
        ok = _garante_contexto_pos_click(driver, timeout=12, tentativas=3)
        if not ok:
            # Loop simples: fechar anúncio, limpar campo, digitar e clicar na sugestão novamente
            for _ in range(5):
                try:
                    _normaliza_janela_letras(driver)
                    _tenta_fechar_popups(driver)
                    _aceita_cookies_conhecidos(driver)
                    _remove_overlays_com_js(driver)

                    campo = WebDriverWait(driver, 8).until(
                        EC.presence_of_element_located((By.ID, "headerInput"))
                    )
                    try:
                        campo.click()
                    except Exception:
                        pass
                    campo.clear()
                    # atualiza a página e tenta novamente
                    try:
                        driver.refresh()
                        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, "headerInput")))
                        campo = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.ID, "headerInput")))
                        try:
                            campo.click()
                        except Exception:
                            pass
                        campo.clear()
                        campo.send_keys(artista_nome)
                    except Exception:
                        pass
                    time.sleep(1)

                    sugerido = WebDriverWait(driver, 6).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "suggest-artist"))
                    )
                    sugerido.click()

                    if _garante_contexto_pos_click(driver, timeout=12, tentativas=3):
                        break
                except Exception:
                    # tenta próxima iteração do loop
                    pass

        soup = BeautifulSoup(driver.page_source, 'html.parser')
        musicas = soup.find_all("a", class_="songList-table-songName")
        # Se ainda não carregou nada (possível anúncio), repete o mesmo fluxo de pesquisa
        if not musicas:
            for _ in range(5):
                try:
                    _normaliza_janela_letras(driver)
                    _tenta_fechar_popups(driver)
                    _aceita_cookies_conhecidos(driver)
                    _remove_overlays_com_js(driver)

                    campo = WebDriverWait(driver, 8).until(
                        EC.element_to_be_clickable((By.ID, "headerInput"))
                    )
                    try:
                        campo.click()
                    except Exception:
                        pass
                    campo.clear()
                    # atualiza a página e tenta novamente
                    try:
                        driver.refresh()
                        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.ID, "headerInput")))
                        campo = WebDriverWait(driver, 8).until(EC.element_to_be_clickable((By.ID, "headerInput")))
                        try:
                            campo.click()
                        except Exception:
                            pass
                        campo.clear()
                        campo.send_keys(artista_nome)
                    except Exception:
                        pass
                    time.sleep(1)

                    sugerido = WebDriverWait(driver, 6).until(
                        EC.element_to_be_clickable((By.CLASS_NAME, "suggest-artist"))
                    )
                    sugerido.click()

                    if _garante_contexto_pos_click(driver, timeout=12, tentativas=3):
                        soup = BeautifulSoup(driver.page_source, 'html.parser')
                        musicas = soup.find_all("a", class_="songList-table-songName")
                        if musicas:
                            break
                except Exception:
                    pass

        lista_musicas = []
        for musica in musicas:
            base = driver.current_url
            titulo = musica.get_text().strip()
            href = musica.get('href')
            if href:
                href = urljoin(base, href)
            lista_musicas.append({'titulo': titulo, 'href': href})

        # informa total para a UI
        total = len(lista_musicas)
        if hooks and 'on_total' in hooks and callable(hooks['on_total']):
            hooks['on_total'](total)

        # coletar detalhes em uma lista separada
        resultados = []
        for idx, item in enumerate(lista_musicas, start=1):
            if hooks and 'on_musica' in hooks and callable(hooks['on_musica']):
                hooks['on_musica'](item['titulo'], idx, total)
            if not item.get('href'):
                continue
            html = requests.get(item['href']).text
            soup = BeautifulSoup(html, 'html.parser')

            letra_el = soup.select_one("div.lyric-original")
            views_el = soup.select_one("b.font.--base.--strong.--size16.u-block")
            comp_el = soup.select_one("div.lyric-info-composition")

            # Extrai apenas o texto entre ':' e o primeiro '.'
            comp_text = comp_el.get_text(" ", strip=True) if comp_el else None
            composicao = None
            if comp_text:
                m = re.search(r':\s*(.*?)\.', comp_text, flags=re.IGNORECASE)
                if m:
                    composicao = m.group(1).strip()
                else:
                    # fallback: remove prefixo e sufixo comum
                    cleaned = re.sub(r'^[^:]*:\s*', '', comp_text)
                    cleaned = cleaned.split('Essa informação', 1)[0].strip()
                    composicao = cleaned or None

            resultados.append({
                'titulo': item['titulo'],
                'url': item['href'],
                'letra': letra_el.get_text(strip=True) if letra_el else None,
                'views': views_el.get_text(strip=True) if views_el else None,
                'composicao': composicao if composicao != "Sabe de quem é a composição? Envie pra gente." else None,
                'extracted_at': time.strftime("%Y-%m-%d %H:%M:%S")
            })

        # Salva CSV com nome baseado no artista
        nome_base = (artista_nome.strip().lower().replace(' ', '_')) or "artista"
        csv_name = f"{nome_base}_letras.csv"
        df = pd.DataFrame(resultados)
        df.to_csv(csv_name, index=False, sep=';', encoding='utf-8')

        print(f"Coleta concluída. Dados salvos em '{csv_name}'.")
        if hooks and 'on_done' in hooks and callable(hooks['on_done']):
            hooks['on_done'](os.path.abspath(csv_name))

    except Exception as e:
        err = f"Erro: {e}"
        print(err)
        if hooks and 'on_error' in hooks and callable(hooks['on_error']):
            hooks['on_error'](err)
    finally:
        if driver is not None:
            try:
                driver.quit()
            except Exception:
                pass


# -------------------------
# Painel CustomTkinter
# -------------------------
class PainelExtracao(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("dark-blue")

        self.title("FGV Comunicação - Extrator de Letras")
        self.geometry("720x520")
        self.minsize(680, 480)

        # Estado
        self.total = 0
        self.progress_val = tk.DoubleVar(value=0.0)
        self.artista_var = tk.StringVar()  # sugestão inicial

        # Layout
        self.columnconfigure(0, weight=1)
        self.rowconfigure(3, weight=1)

        header = ctk.CTkLabel(self, text="Extrator de letras (letras.mus.br)", font=ctk.CTkFont(size=18, weight="bold"))
        header.grid(row=0, column=0, padx=16, pady=(16, 8), sticky="w")

        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=16, pady=8, sticky="ew")
        form_frame.columnconfigure(1, weight=1)

        lbl = ctk.CTkLabel(form_frame, text="Artista:")
        lbl.grid(row=0, column=0, padx=(12, 8), pady=12, sticky="w")

        self.entry = ctk.CTkEntry(form_frame, textvariable=self.artista_var, placeholder_text="Digite o nome do artista")
        self.entry.grid(row=0, column=1, padx=(0, 8), pady=12, sticky="ew")

        self.btn_buscar = ctk.CTkButton(form_frame, text="Pesquisar", command=self.iniciar_busca)
        self.btn_buscar.grid(row=0, column=2, padx=(0, 12), pady=12)

        progress_frame = ctk.CTkFrame(self)
        progress_frame.grid(row=2, column=0, padx=16, pady=(8, 0), sticky="ew")
        progress_frame.columnconfigure(0, weight=1)

        self.status_label = ctk.CTkLabel(progress_frame, text="Aguardando...", anchor="w")
        self.status_label.grid(row=0, column=0, padx=12, pady=(10, 4), sticky="ew")

        self.progress = ctk.CTkProgressBar(progress_frame)
        self.progress.grid(row=1, column=0, padx=12, pady=(0, 10), sticky="ew")
        self.progress.set(0.0)

        self.percent_label = ctk.CTkLabel(progress_frame, text="")
        self.percent_label.grid(row=1, column=1, padx=12, pady=(0, 10), sticky="e")

        log_frame = ctk.CTkFrame(self)
        log_frame.grid(row=3, column=0, padx=16, pady=8, sticky="nsew")
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log = ctk.CTkTextbox(log_frame, wrap="word")
        self.log.grid(row=0, column=0, sticky="nsew", padx=8, pady=8)
        self.log.configure(state="disabled")

        footer = ctk.CTkFrame(self)
        footer.grid(row=4, column=0, padx=16, pady=(0, 12), sticky="ew")
        footer.columnconfigure(0, weight=1)

        self.done_label = ctk.CTkLabel(footer, text="", font=ctk.CTkFont(size=14, weight="bold"))
        self.done_label.grid(row=0, column=0, padx=12, pady=6, sticky="w")

        self.btn_abrir = ctk.CTkButton(footer, text="Abrir CSV", command=self.abrir_csv)
        self.btn_abrir.grid(row=0, column=1, padx=12, pady=6, sticky="e")
        self.btn_abrir.configure(state="disabled")

        self.csv_path = None

    # Utilidades UI
    def _safe(self, fn, *args, **kwargs):
        self.after(0, lambda: fn(*args, **kwargs))

    def append_log(self, msg: str):
        self.log.configure(state="normal")
        self.log.insert("end", msg + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def reset_ui(self):
        self.total = 0
        self.csv_path = None
        self.progress.set(0.0)
        self.percent_label.configure(text="")
        self.status_label.configure(text="Iniciando...")
        self.done_label.configure(text="")
        self.btn_abrir.configure(state="disabled")
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")

    def set_total(self, total: int):
        self.total = total
        self._safe(self.status_label.configure, text=f"Encontradas {total} músicas.")
        self._safe(self.append_log, f"Total de músicas encontradas: {total}")

    def set_musica(self, titulo: str, idx: int, total: int):
        prog = (idx / total) if total else 0.0
        self._safe(self.status_label.configure, text=f"Processando música ({idx}/{total}): {titulo}")
        self._safe(self.progress.set, prog)
        self._safe(self.percent_label.configure, text=f"{int(prog*100)}%")
        self._safe(self.append_log, f"- {idx}/{total}: {titulo}")

    def concluir(self, csv_path: str):
        self.csv_path = csv_path
        self._safe(self.status_label.configure, text="✅ Coleta concluída.")
        self._safe(self.done_label.configure, text=f"✅ Concluído: {os.path.basename(csv_path)}")
        self._safe(self.btn_abrir.configure, state="normal")
        self._safe(self.btn_buscar.configure, state="normal")
        self._safe(self.entry.configure, state="normal")

    def falhou(self, msg: str):
        self._safe(self.status_label.configure, text="Falha na coleta.")
        self._safe(self.append_log, f"[ERRO] {msg}")
        self._safe(self.btn_buscar.configure, state="normal")
        self._safe(self.entry.configure, state="normal")

    def abrir_csv(self):
        if self.csv_path and os.path.exists(self.csv_path):
            try:
                os.startfile(self.csv_path)  # Windows
            except Exception as e:
                self.append_log(f"Não foi possível abrir o arquivo: {e}")

    # Fluxo
    def iniciar_busca(self):
        artista = self.artista_var.get().strip()
        if not artista:
            self.status_label.configure(text="Informe o nome do artista.")
            return

        self.btn_buscar.configure(state="disabled")
        self.entry.configure(state="disabled")
        self.reset_ui()

        def worker():
            hooks = {
                'on_total': lambda total: self._safe(self.set_total, total),
                'on_musica': lambda titulo, idx, total: self.set_musica(titulo, idx, total),
                'on_done': lambda csv_path: self.concluir(csv_path),
                'on_error': lambda msg: self.falhou(msg),
            }
            scrape_letras(artista, hooks)

        Thread(target=worker, daemon=True).start()


if __name__ == "__main__":
    app = PainelExtracao()
    app.mainloop()