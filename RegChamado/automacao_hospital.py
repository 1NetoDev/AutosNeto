# automacao_hospital.py

import tkinter as tk
from tkinter import messagebox
import threading
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import WebDriverException
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

# 3. --- SELETORES PARA CRIAR NOVO FORMULÁRIO ---
XPATH_BOTAO_ABRIR_MENU = "//li[.//span[text()='Abrir']]"
XPATH_TAB_FAVORITOS = "/html/body/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[1]/div[3]"
XPATH_LINK_PROCESSO_TI = "/html/body/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[2]/div/div[2]"

# 4. IDs e Seletores do Formulário e Pop-ups
ID_IFRAME = "iframe-form-app"
ID_RAMAL = "LT_RAMAL"
ID_DROPDOWN_TIPO_SOLICITACAO = "LS_PROCESSO"
ID_TITULO = "LT_TITULO_REQUISICAO"
CSS_SELECTOR_BOTAO_FECHAR_WELCOME = "span.ant-modal-close-x"
XPATH_BOTAO_FECHAR_MENSAGENS = "//*[@id='social']/div/div/div[2]/div[1]/div[1]/div/div[2]/i[3]"

# 5. XPaths dos ícones de LUPA
XPATH_LUPA_CASA = "//*[@id='LT_CASA_lookup']"
XPATH_LUPA_CATEGORIA = "//*[@id='LT_CATEGORIA_lookup']"
XPATH_LUPA_SUBCATEGORIA = "//*[@id='LT_SUB_CAT_lookup']"
XPATH_LUPA_SERVICO = "//*[@id='LT_SERVICO_lookup']"
XPATH_LUPA_GRUPO_ATEND = "//*[@id='LT_GRUPO_ATEND_lookup']"

# 6. IDs dos campos de BUSCA dentro de cada Lupa (CORRIGIDOS)
ID_LUPA_INPUT_CASA = "LT_CASA_lookup-modal"
ID_LUPA_INPUT_CATEGORIA = "LT_CATEGORIA_lookup-modal"
ID_LUPA_INPUT_SUBCATEGORIA = "LT_SUB_CAT_lookup-modal"
ID_LUPA_INPUT_SERVICO = "LT_SERVICO_lookup-modal"
ID_LUPA_INPUT_GRUPO_ATEND = "LT_GRUPO_ATEND_lookup-modal"

# 7. Textos Padrão para os Campos
TEXTO_CASA = "HOSPITAL SANTA CATARINA"
TEXTO_RAMAL = "0000"
TEXTO_CATEGORIA = "Software"
TEXTO_SUBCATEGORIA = "Navegadores"
TEXTO_SERVICO = "Configuração"
TEXTO_DROPDOWN_TIPO_SOLICITACAO = "INFRAESTRUTURA SOFTWARES"
TEXTO_GRUPO_ATEND = "Servicedesk"
TEXTO_TITULO = "Registro de Ligação"

# 8. Seletor para o botão "FILTRAR" e CÉLULA DE RESULTADO dentro da Lupa
XPATH_BOTAO_FILTRAR = "//*[@id='LT_CASA_lookup-modal']/div[2]/div/div[2]/div[1]/form/div[2]/button[2]"
XPATH_CELULA_RESULTADO = "//*[@id='LT_CASA_lookup-modal']/div[2]/div/div[2]/div[2]/div/div/table/tbody/tr/td[2]"


# =====================================================================================
# --- FIM DAS CONFIGURAÇÕES ---
# =====================================================================================

driver = None

def preencher_campo_lupa(wait, status_updater, xpath_lupa_icon, id_campo_busca_lupa, texto_busca):
    """Função para automatizar o preenchimento de campos com o padrão 'Lupa', com lógica de retentativa."""
    MAX_TENTATIVAS = 3
    for tentativa in range(1, MAX_TENTATIVAS + 1):
        try:
            status_updater(f"Lupa: {texto_busca} (Tentativa {tentativa})...")
            
            lupa_icon = wait.until(EC.element_to_be_clickable((By.XPATH, xpath_lupa_icon)))
            lupa_icon.click()
            
            time.sleep(1.0)
            
            campo_busca = wait.until(EC.presence_of_element_located((By.ID, id_campo_busca_lupa)))
            
            actions = ActionChains(driver)
            actions.move_to_element(campo_busca).click().pause(0.5).send_keys(texto_busca).perform()
            
            botao_filtrar = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_FILTRAR)))
            botao_filtrar.click()
            
            # --- LÓGICA ATUALIZADA ---
            time.sleep(0.3) # Pausa solicitada
            
            status_updater("Aguardando resultado...")
            primeiro_resultado = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_CELULA_RESULTADO)))
            primeiro_resultado.click()
            
            time.sleep(0.3) # Pausa solicitada
            
            status_updater(f"OK: {texto_busca} selecionado.")
            return True
        except Exception as e:
            print(f"Erro na tentativa {tentativa} da Lupa ({texto_busca}): {e}")
            if tentativa == MAX_TENTATIVAS:
                status_updater(f"ERRO na Lupa: {texto_busca}!")
                return False
            status_updater(f"Retentando Lupa: {texto_busca}...")
            try:
                driver.find_element(By.XPATH, "//button[text()='FECHAR']").click()
            except:
                pass

def iniciar_navegador(status_label, botao_preencher):
    """Abre o navegador, faz login e fecha os pop-ups."""
    
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
                    messagebox.showerror("Navegador não Encontrado", "O Google Chrome não foi encontrado neste computador.\n\nPor favor, instale o Google Chrome para usar esta automação.")
                    return

                atualizar_status("Configurando driver...")
                chrome_options = Options()
                chrome_options.add_argument("--window-size=1366,768")
                chrome_options.add_argument("--disable-notifications")
                driver = webdriver.Chrome(service=service, options=chrome_options)
            
            atualizar_status("Acessando sistema...")
            driver.get(URL_SISTEMA)
            wait = WebDriverWait(driver, 30)
            
            atualizar_status("Preenchendo credenciais...")
            wait.until(EC.visibility_of_element_located((By.NAME, NAME_CAMPO_USUARIO_LOGIN))).send_keys(SEU_USUARIO)
            driver.find_element(By.NAME, NAME_CAMPO_SENHA_LOGIN).send_keys(SUA_SENHA)
            
            atualizar_status("Realizando login...")
            driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR_BOTAO_LOGIN).click()

            atualizar_status("Login OK. Procurando pop-up de boas-vindas...")
            try:
                botao_fechar_welcome = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, CSS_SELECTOR_BOTAO_FECHAR_WELCOME)))
                botao_fechar_welcome.click()
                atualizar_status("Pop-up de boas-vindas fechado.")
            except Exception:
                atualizar_status("Pop-up de boas-vindas não encontrado.")

            atualizar_status("Procurando janela de mensagens...")
            try:
                time.sleep(2)
                botao_fechar_mensagens = wait.until(EC.element_to_be_clickable((By.XPATH, XPATH_BOTAO_FECHAR_MENSAGENS)))
                botao_fechar_mensagens.click()
                atualizar_status("Janela de mensagens fechada.")
            except Exception:
                atualizar_status("Janela de mensagens não encontrada.")

            atualizar_status("Navegador pronto!")
            botao_preencher.config(state=tk.NORMAL)
            messagebox.showinfo("Pronto!", "Navegador iniciado e logado.\n\nClique em 'Preencher Formulário' para começar.")

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
            messagebox.showerror("Erro", "O navegador não foi iniciado. Por favor, clique em 'Iniciar Navegador' primeiro.")
            return
        
        try:
            wait = WebDriverWait(driver, 30)
            
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
            
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_CASA, ID_LUPA_INPUT_CASA, TEXTO_CASA): return
            
            atualizar_status("Preenchendo Ramal...")
            driver.find_element(By.ID, ID_RAMAL).send_keys(TEXTO_RAMAL)
            
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_CATEGORIA, ID_LUPA_INPUT_CATEGORIA, TEXTO_CATEGORIA): return
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_SUBCATEGORIA, ID_LUPA_INPUT_SUBCATEGORIA, TEXTO_SUBCATEGORIA): return
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_SERVICO, ID_LUPA_INPUT_SERVICO, TEXTO_SERVICO): return
            
            atualizar_status("Selecionando Tipo de Solicitação...")
            dropdown = Select(driver.find_element(By.ID, ID_DROPDOWN_TIPO_SOLICITACAO))
            dropdown.select_by_visible_text(TEXTO_DROPDOWN_TIPO_SOLICITACAO)
            
            if not preencher_campo_lupa(wait, atualizar_status, XPATH_LUPA_GRUPO_ATEND, ID_LUPA_INPUT_GRUPO_ATEND, TEXTO_GRUPO_ATEND): return
            
            atualizar_status("Preenchendo Título...")
            driver.find_element(By.ID, ID_TITULO).send_keys(TEXTO_TITULO)
            
            atualizar_status("CONCLUÍDO! Preencha os detalhes.")
            messagebox.showinfo("Sucesso!", "Preenchimento automático concluído.\n\nPor favor, preencha o campo 'Detalhe da sua requisição' e envie o chamado.")

        except Exception as e:
            error_message = f"ERRO FATAL no preenchimento: {str(e)[:100]}..."
            atualizar_status(error_message)
            print(f"Erro detalhado: {e}")
            if driver:
                driver.save_screenshot('erro_fatal.png')
            messagebox.showerror("Erro na Automação", f"Ocorreu um erro inesperado.\n\n{error_message}\n\nUm screenshot foi salvo como 'erro_fatal.png'.")

    threading.Thread(target=run_fill, daemon=True).start()

def criar_interface():
    root = tk.Tk()
    root.title("Automador de Chamados")
    root.geometry("350x180")
    root.attributes('-topmost', True)
    root.resizable(False, False)

    main_frame = tk.Frame(root, padx=15, pady=15)
    main_frame.pack(fill="both", expand=True)

    botao_iniciar = tk.Button(main_frame, text="1. Iniciar Navegador e Login", command=lambda: iniciar_navegador(status_label, botao_preencher), font=("Segoe UI", 10, "bold"), bg="#0078D7", fg="white", relief="flat", padx=10, pady=5)
    botao_iniciar.pack(pady=5, ipady=4, fill="x")

    botao_preencher = tk.Button(main_frame, text="2. Preencher Formulário", command=lambda: preencher_formulario(status_label), font=("Segoe UI", 10, "bold"), bg="#2a75bb", fg="white", relief="flat", padx=10, pady=5, state=tk.DISABLED)
    botao_preencher.pack(pady=5, ipady=4, fill="x")
    
    status_label = tk.Label(main_frame, text="Status: Aguardando início...", bd=1, relief="sunken", anchor="w", padx=5)
    status_label.pack(side="bottom", fill="x", pady=(10, 0))
    
    root.mainloop()

if __name__ == "__main__":
    criar_interface()
