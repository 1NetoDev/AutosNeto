# xpaths.py
# Este arquivo centraliza todos os seletores e textos para fácil manutenção.

# --- URLs ---
URL_SISTEMA = "https://app.santacatarina.lecom.com.br/sso/login?redirectBackTo=https://app.santacatarina.lecom.com.br/workspace"
URL_WORKSPACE = "https://app.santacatarina.lecom.com.br/workspace"

# --- LOGIN ---
NAME_CAMPO_USUARIO_LOGIN = "username"
NAME_CAMPO_SENHA_LOGIN = "password"
CSS_SELECTOR_BOTAO_LOGIN = "button[type='submit']"

# --- CRIAÇÃO DE NOVO FORMULÁRIO ---
XPATH_BOTAO_ABRIR_MENU = "//li[.//span[text()='Abrir']]"
XPATH_TAB_FAVORITOS = "/html/body/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div[1]/div/div/div/div/div[1]/div[3]"
XPATH_LINK_PROCESSO_TI = "/html/body/div[3]/div/div[2]/div/div/div/div/div[1]/div[2]/div[3]/div[3]/div[2]/div/div[2]"

# --- FORMULÁRIO E POP-UPS ---
ID_IFRAME = "iframe-form-app"
XPATH_RAMAL = "//*[@id='LT_RAMAL']"
XPATH_DROPDOWN_TIPO_SOLICITACAO = "//*[@id='LS_PROCESSO']"
XPATH_TITULO = "//*[@id='LT_TITULO_REQUISICAO']"
CSS_SELECTOR_BOTAO_FECHAR_WELCOME = "span.ant-modal-close-x"
XPATH_BOTAO_FECHAR_MENSAGENS = "//*[@id='social']/div/div/div[2]/div[1]/div[1]/div/div[2]/i[3]/svg"

# --- ÍCONES DE LUPA ---
XPATH_LUPA_CASA = "//*[@id='LT_CASA_lookup']"
XPATH_LUPA_CATEGORIA = "//*[@id='LT_CATEGORIA_lookup']"
XPATH_LUPA_SUBCATEGORIA = "//*[@id='LT_SUB_CAT_lookup']"
XPATH_LUPA_SERVICO = "//*[@id='LT_SERVICO_lookup']"
XPATH_LUPA_GRUPO_ATEND = "//*[@id='LT_GRUPO_ATEND_lookup']"

# --- CAMPOS DE BUSCA (DENTRO DAS LUPAS) ---
ID_LUPA_INPUT_CASA = "LT_CASA_lookup-modal"
ID_LUPA_INPUT_CATEGORIA = "LT_CATEGORIA_lookup-modal"
ID_LUPA_INPUT_SUBCATEGIA = "LT_SUB_CAT_lookup-modal"
ID_LUPA_INPUT_SERVICO = "LT_SERVICO_lookup-modal"
ID_LUPA_INPUT_GRUPO_ATEND = "LT_GRUPO_ATEND_lookup-modal"

# --- LUPA: BOTÃO FILTRAR E CÉLULA DE RESULTADO (SERÃO FORMATADOS DINAMICAMENTE) ---
XPATH_BOTAO_FILTRAR_BASE = "//*[@id='{id_campo_busca}']/following-sibling::div//button[contains(., 'Filtrar')]"
XPATH_CELULA_RESULTADO_BASE = "//*[@id='{id_campo_busca}']/following-sibling::div//table/tbody/tr/td[2]"

# --- TEXTOS PADRÃO ---
TEXTO_CASA = "HOSPITAL SANTA CATARINA"
TEXTO_RAMAL = "8080"
TEXTO_CATEGORIA = "Software"
TEXTO_SUBCATEGORIA = "Navegadores"
TEXTO_SERVICO = "Configuração"
TEXTO_DROPDOWN_TIPO_SOLICITACAO = "INFRAESTRUTURA SOFTWARES"
TEXTO_GRUPO_ATEND = "Servicedesk"
TEXTO_TITULO = "Registro de Ligação"
