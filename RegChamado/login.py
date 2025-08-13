# login.py

import time
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Importa as configurações do arquivo xpaths.py
import xpaths

# --- SUAS CREDENCIAIS ---
SEU_USUARIO = "t432893"
SUA_SENHA = "432893@Estradas"

driver = None

def executar_login(status_updater):
    """Abre o navegador, faz login e fecha os pop-ups."""
    global driver
    
    try:
        if driver is None:
            status_updater("Verificando Chrome...")
            try:
                service = Service(ChromeDriverManager().install())
            except WebDriverException:
                status_updater("ERRO: Chrome não encontrado!")
                messagebox.showerror("Navegador não Encontrado", "O Google Chrome não foi encontrado.")
                return None

            status_updater("Configurando driver...")
            chrome_options = Options()
            chrome_options.add_argument("--start-maximized")
            chrome_options.add_argument("--disable-notifications")
            driver = webdriver.Chrome(service=service, options=chrome_options)
        
        status_updater("Acessando sistema...")
        driver.get(xpaths.URL_SISTEMA)
        wait = WebDriverWait(driver, 10)
        
        status_updater("Preenchendo credenciais...")
        wait.until(EC.visibility_of_element_located((By.NAME, xpaths.NAME_CAMPO_USUARIO_LOGIN))).send_keys(SEU_USUARIO)
        driver.find_element(By.NAME, xpaths.NAME_CAMPO_SENHA_LOGIN).send_keys(SUA_SENHA)
        
        status_updater("Realizando login...")
        driver.find_element(By.CSS_SELECTOR, xpaths.CSS_SELECTOR_BOTAO_LOGIN).click()

        status_updater("Login OK. Procurando pop-ups...")
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, xpaths.CSS_SELECTOR_BOTAO_FECHAR_WELCOME))).click()
            status_updater("Pop-up de boas-vindas fechado.")
        except TimeoutException:
            status_updater("Pop-up de boas-vindas não encontrado.")

        try:
            short_wait = WebDriverWait(driver, 3)
            short_wait.until(EC.element_to_be_clickable((By.XPATH, xpaths.XPATH_BOTAO_FECHAR_MENSAGENS))).click()
            status_updater("Janela de mensagens fechada.")
        except TimeoutException:
            status_updater("Janela de mensagens não encontrada.")

        status_updater("Navegador pronto!")
        messagebox.showinfo("Pronto!", "Navegador iniciado e logado.")
        return driver

    except Exception as e:
        error_message = f"ERRO FATAL no login: {str(e)[:100]}..."
        status_updater(error_message)
        print(f"Erro detalhado: {e}")
        messagebox.showerror("Erro na Automação", f"Ocorreu um erro ao iniciar o navegador.\n\n{error_message}")
        return None
