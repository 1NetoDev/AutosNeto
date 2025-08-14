# automacao_hospital.py

import tkinter as tk
from tkinter import messagebox
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

# =====================================================================================
# --- CONFIGURAÇÕES (VERIFIQUE SE OS VALORES ESTÃO CORRETOS) ---
# =====================================================================================

# 1. --- LOGIN ---
SEU_USUARIO = "t432893"
SUA_SENHA = "432893@Estradas"

# Seletores da tela de login
NAME_CAMPO_USUARIO_LOGIN = "username"
NAME_CAMPO_SENHA_LOGIN = "password"
CSS_SELECTOR_BOTAO_LOGIN = "button[type='submit']"

# 2. URLs
URL_SISTEMA = "https://app.santacatarina.lecom.com.br/sso/login?redirectBackTo=https://app.santacatarina.lecom.com.br/workspace"
URL_WORKSPACE = "https://app.santacatarina.lecom.com.br/workspace"

# 3. --- SELETORES PARA CRIAR NOVO FORMULÁRIO ---
XPATH_BOTAO_ABRIR_MENU = "//li[.//span[text()='Abrir']]"
XPATH_TAB_FAVORITOS = "/html/body/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[1]/div[3]"
XPATH_LINK_PROCESSO_TI = "/html/body/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[2]/div/div[2]"

# 4. IDs e Seletores do Formulário e Pop-ups
ID_IFRAME = "iframe-form-app"
XPATH_RAMAL = "//*[@id='LT_RAMAL']"
XPATH_DROPDOWN_TIPO_SOLICITACAO = "//*[@id='LS_PROCESSO']"
XPATH_TITULO = "//*[@id='LT_TITULO_REQUISICAO']"
CSS_SELECTOR_BOTAO_FECHAR_WELCOME = "span.ant-modal-close-x"
XPATH_BOTAO_FECHAR_MENSAGENS = "//*[@id='social']/div/div/div[2]/div[1]/div[1]/div/div[2]/i[3]"

# 5. XPaths dos ícones de LUPA
XPATH_LUPA_CASA = "//*[@id='LT_CASA_lookup']"
XPATH_LUPA_CATEGORIA = "//*[@id='LT_CATEGORIA_lookup']"
XPATH_LUPA_SUBCATEGORIA = "//*[@id='LT_SUB_CAT_lookup']"
XPATH_LUPA_SERVICO = "//*[@id='LT_SERVICO_lookup']"
XPATH_LUPA_GRUPO_ATEND = "//*[@id='LT_GRUPO_ATEND_lookup']"

# 6. IDs dos campos de BUSCA dentro de cada Lupa
ID_LUPA_INPUT_CASA = "LT_CASA__lookup-modal"
ID_LUPA_INPUT_CATEGORIA = "LT_CATEGORIA__lookup-modal"
ID_LUPA_INPUT_SUBCATEGORIA = "LT_SUB_CAT__lookup-modal"
ID_LUPA_INPUT_SERVICO = "LT_SERVICO__lookup-modal"
ID_LUPA_INPUT_GRUPO_ATEND = "LT_GRUPO_ATEND__lookup-modal"

# 7. Textos Padrão para os Campos
TEXTO_CASA = "HOSPITAL SANTA CATARINA"
TEXTO_RAMAL = "8080"
TEXTO_CATEGORIA = "Software"
TEXTO_SUBCATEGORIA = "Navegadores"
TEXTO_SERVICO = "Configuração"
TEXTO_DROPDOWN_TIPO_SOLICITACAO = "INFRAESTRUTURA SOFTWARES"
TEXTO_GRUPO_ATEND = "Servicedesk"
TEXTO_TITULO = "Registro de Ligação"

# 8. --- CORREÇÃO --- XPaths específicos para cada botão "FILTRAR" e CÉLULA DE RESULTADO
XPATH_FILTRAR_CASA = "//*[@id='LT_CASA_lookup-modal']/div[2]/div/div[2]/div[1]/form/div[2]/button[2]"
XPATH_CELULA_CASA = "//*[@id='LT_CASA_lookup-modal']/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]"
XPATH_FILTRAR_CATEGORIA = "//*[@id='LT_CATEGORIA_lookup-modal']/div[2]/div/div[2]/div[1]/form/div[2]/button[2]"
XPATH_CELULA_CATEGORIA = "//*[@id='LT_CATEGORIA_lookup-modal']/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]"
XPATH_FILTRAR_SUBCATEGORIA = "//*[@id='LT_SUB_CAT_lookup-modal']/div[2]/div/div[2]/div[1]/form/div[2]/button[2]"
XPATH_CELULA_SUBCATEGORIA = "//*[@id='LT_SUB_CAT_lookup-modal']/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]"
XPATH_FILTRAR_SERVICO = "//*[@id='LT_SERVICO_lookup-modal']/div[2]/div/div[2]/div[1]/form/div[2]/button[2]"
XPATH_CELULA_SERVICO = "//*[@id='LT_SERVICO_lookup-modal']/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]"
XPATH_FILTRAR_GRUPO_ATEND = "//*[@id='LT_GRUPO_ATEND_lookup-modal']/div[2]/div/div[2]/div[1]/form/div[2]/button[2]"
XPATH_CELULA_GRUPO_ATEND = "//*[@id='LT_GRUPO_ATEND_lookup-modal']/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]"


# =====================================================================================
# --- FIM DAS CONFIGURAÇÕES ---
# =====================================================================================

driver = None

def preencher_campo_lupa(wait, status_updater, xpath_lupa_icon, id_campo_busca_lupa, texto_busca, xpath_botao_filtrar, xpath_celula_resultado):
    """Função para automatizar o preenchimento de campos com o padrão 'Lupa', com lógica de retentativa."""
    MAX_TENTATIVAS = 3
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            status_updater(f"Lupa: {texto_busca} (Tentativa {tentativa})...")
            
            wait.until(EC.element_to_be_clickable((By.XPATH, xpath_lupa_icon))).click()
            time.sleep(1.0)
            
            campo_busca = wait.until(EC.presence_of_element_located((By.ID, id_campo_busca_lupa)))
            
            actions = ActionChains(driver)
            actions.move_to_element(campo_busca).click().pause(0.5).send_keys(texto_busca).perform()
            
            botao_filtrar = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_botao_filtrar)))
            botao_filtrar.click()
            time.sleep(0.3)
            
            status_updater("Aguardando resultado...")
            primeiro_resultado = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_celula_resultado)))
            primeiro_resultado.click()
            time.sleep(0.3)
            
            status_updater(f"OK: {texto_busca} selecionado.")
            return True
        except Exception as e:
            print(f"Erro na tentativa {tentativa} da Lupa ({texto_busca}): {e}")
            if tentativa < MAX_TENTATIVAS:
                status_updater(f"Retentando Lupa: {texto_busca}...")
                try:
                    driver.find_element(By.XPATH, "//button[text()='FECHAR']").click()
                    time.sleep(0.5)
                except:
                    pass
            else:
                status_updater(f"ERRO na Lupa: {texto_busca}!")
                return False

def iniciar_navegador(status_label, botoes):
    """Abre o navegador, faz login e fecha os pop-ups."""
    global driver
    
    def run_login():
        global driver
        def atualizar_status(mensagem):
            print(mensagem)
            status_label.config(text=f"Status: {mensagem}")
        
        try:
            if driver is None:
                atualizar_status("Verificando Chrome...")
                try:
                    service = Service(ChromeDriverManager().install())
                except WebDriverException:
                    atualizar_status("ERRO: Chrome não encontrado!")
                    messagebox.showerror("Navegador não Encontrado", "O Google Chrome não foi encontrado.")
                    return

                atualizar_status("Configurando driver...")
                chrome_options = Options()
                chrome_options.add_argument("--start-maximized")
                chrome_options.add_argument("--disable-notifications")
                driver = webdriver.Chrome(service=service, options=chrome_options)
            
            atualizar_status("Acessando sistema...")
            driver.get(URL_SISTEMA)
            wait = WebDriverWait(driver, 10)
            
            atualizar_status("Preenchendo credenciais...")
            wait.until(EC.visibility_of_element_located((By.NAME, NAME_CAMPO_USUARIO_LOGIN))).send_keys(SEU_USUARIO)
            driver.find_element(By.NAME, NAME_CAMPO_SENHA_LOGIN).send_keys(SUA_SENHA)
            
            atualizar_status("Realizando login...")
            driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_BOTAO_LOGIN).click()

            atualizar_status("Login OK. Procurando pop-ups...")
            try:
                wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_BOTAO_FECHAR_WELCOME))).click()
                time.sleep(1.0)
            except TimeoutException:
                pass

            try:
                short_wait = WebDriverWait(driver, 3)
                short_wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_FECHAR_MENSAGENS))).click()
            except TimeoutException:
                pass

            atualizar_status("Navegador pronto!")
            for botao in botoes.values():
                botao.config(state=tk.NORMAL)
            messagebox.showinfo("Pronto!", "Navegador iniciado e logado.")

        except Exception as e:
            error_message = f"ERRO FATAL no login: {str(e)[:100]}..."
            atualizar_status(error_message)
            print(f"Erro detalhado: {e}")
            messagebox.showerror("Erro na Automação", f"Ocorreu um erro ao iniciar o navegador.\n\n{error_message}")

    threading.Thread(target=run_login, daemon=True).start()

def preencher_formulario(status_label):
    """Cria um novo formulário e preenche os campos."""
    global driver

    def run_fill():
        def atualizar_status(mensagem):
            print(mensagem)
            status_label.config(text=f"Status: {mensagem}")

        if driver is None:
            messagebox.showerror("Erro", "O navegador não foi iniciado primeiro.")
            return
        
        try:
            wait = WebDriverWait(driver, 15)
            
            atualizar_status("Clicando em 'Abrir'...")
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_ABRIR_MENU))).click()
            time.sleep(0.6)

            atualizar_status("Clicando na aba 'Favoritos'...")
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_TAB_FAVORITOS))).click()
            time.sleep(0.4)

            atualizar_status("Selecionando processo 'TI - Operador'...")
            wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_LINK_PROCESSO_TI))).click()
            time.sleep(1.5)
            
            atualizar_status("Procurando formulário (iframe)...")
            wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, ID_IFRAME)))
            
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_CASA, ID_LUPA_INPUT_CASA, TEXTO_CASA, XPATH_FILTRAR_CASA, XPATH_CELULA_CASA): return
            
            atualizar_status("Preenchendo Ramal...")
            driver.find_element(By.XPATH, XPATH_RAMAL).send_keys(TEXTO_RAMAL)
            
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_CATEGORIA, ID_LUPA_INPUT_CATEGORIA, TEXTO_CATEGORIA, XPATH_FILTRAR_CATEGORIA, XPATH_CELULA_CATEGORIA): return
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_SUBCATEGORIA, ID_LUPA_INPUT_SUBCATEGORIA, TEXTO_SUBCATEGORIA, XPATH_FILTRAR_SUBCATEGORIA, XPATH_CELULA_SUBCATEGORIA): return
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_SERVICO, ID_LUPA_INPUT_SERVICO, TEXTO_SERVICO, XPATH_FILTRAR_SERVICO, XPATH_CELULA_SERVICO): return
            
            atualizar_status("Selecionando Tipo de Solicitação...")
            dropdown = Select(driver.find_element(By.XPATH, XPATH_DROPDOWN_TIPO_SOLICITACAO))
            dropdown.select_by_visible_text(TEXTO_DROPDOWN_TIPO_SOLICITACAO)
            
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_GRUPO_ATEND, ID_LUPA_INPUT_GRUPO_ATEND, TEXTO_GRUPO_ATEND, XPATH_FILTRAR_GRUPO_ATEND, XPATH_CELULA_GRUPO_ATEND): return
            
            atualizar_status("Preenchendo Título...")
            driver.find_element(By.XPATH, XPATH_TITULO).send_keys(TEXTO_TITULO)
            
            atualizar_status("CONCLUÍDO! Preencha os detalhes.")
            messagebox.showinfo("Sucesso!", "Preenchimento automático concluído.")

        except Exception as e:
            error_message = f"ERRO FATAL no preenchimento: {str(e)[:100]}..."
            atualizar_status(error_message)
            print(f"Erro detalhado: {e}")
            if driver:
                driver.save_screenshot('erro_fatal.png')
            messagebox.showerror("Erro na Automação", f"Ocorreu um erro inesperado.\n\n{error_message}")

    threading.Thread(target=run_fill, daemon=True).start()

def cancelar_formulario(status_label):
    """Navega de volta para a página inicial para um novo chamado."""
    global driver
    
    def run_cancel():
        if driver is None:
            messagebox.showwarning("Aviso", "O navegador não foi iniciado.")
            return
        status_label.config(text="Status: Cancelando...")
        driver.switch_to.default_content()
        driver.get(URL_WORKSPACE)
        status_label.config(text="Status: Pronto para novo chamado.")
    
    threading.Thread(target=run_cancel, daemon=True).start()

def reiniciar_login(status_label, botoes):
    """Navega de volta para a página de login."""
    global driver

    def run_restart():
        if driver is None:
            messagebox.showwarning("Aviso", "O navegador não foi iniciado.")
            return
        status_label.config(text="Status: Reiniciando para o login...")
        driver.get(URL_SISTEMA)
        status_label.config(text="Status: Aguardando novo login...")
        botoes['preencher'].config(state=tk.DISABLED)
        botoes['cancelar'].config(state=tk.DISABLED)
        botoes['reiniciar_login'].config(state=tk.DISABLED)

    threading.Thread(target=run_restart, daemon=True).start()

def criar_interface():
    root = tk.Tk()
    root.title("Automador de Chamados")
    root.geometry("350x250")
    root.attributes('-topmost', True)
    root.resizable(False, False)

    main_frame = tk.Frame(root, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

    botoes = {}

    botoes['iniciar'] = tk.Button(main_frame, text="1. Iniciar Navegador e Login", command=lambda: iniciar_navegador(status_label, botoes), font=("Segoe UI", 10, "bold"), bg="#0078D7", fg="white", relief="flat", padx=10, pady=5)
    botoes['iniciar'].pack(pady=5, ipady=4, fill="x")

    botoes['preencher'] = tk.Button(main_frame, text="2. Preencher Formulário", command=lambda: preencher_formulario(status_label), font=("Segoe UI", 10, "bold"), bg="#2a75bb", fg="white", relief="flat", padx=10, pady=5, state=tk.DISABLED)
    botoes['preencher'].pack(pady=5, ipady=4, fill="x")
    
    control_frame = tk.Frame(main_frame)
    control_frame.pack(pady=(10,0), fill="x")

    botoes['cancelar'] = tk.Button(control_frame, text="Cancelar", command=lambda: cancelar_formulario(status_label), font=("Segoe UI", 9), bg="#d13438", fg="white", relief="flat")
    botoes['cancelar'].pack(side="left", expand=True, fill="x", padx=(0, 5))
    
    botoes['reiniciar_login'] = tk.Button(control_frame, text="Reiniciar Login", command=lambda: reiniciar_login(status_label, botoes), font=("Segoe UI", 9), bg="#005a9e", fg="white", relief="flat")
    botoes['reiniciar_login'].pack(side="right", expand=True, fill="x", padx=(5, 0))
    
    status_label = tk.Label(main_frame, text="Status: Aguardando início...", bd=1, relief="sunken", anchor="w", padx=5)
    status_label.pack(side="bottom", fill="x", pady=(10, 0))
    
    for key in ['preencher', 'cancelar', 'reiniciar_login']:
        botoes[key].config(state=tk.DISABLED)

    root.mainloop()

if __name__ == "__main__":
    criar_interface()
