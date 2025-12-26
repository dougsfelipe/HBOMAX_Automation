import pytest
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


# --- FIXTURES (Iguais às anteriores) ---
@pytest.fixture(scope="session")
def driver_session():
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": "com.wbd.stream",
        # Aceita qualquer tela inicial, mas não garante o launch
        "appium:appWaitActivity": "*",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True,
        "appium:noReset": True,
        "appium:adbExecTimeout": 60000,
    })

    # 1. Conecta no Appium
    print("Conectando ao Appium...")
    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)

    # 2. O PULO DO GATO: Força o app a abrir explicitamente
    # Se o app estiver fechado, ele abre. Se estiver em background, ele traz pra frente.
    print("Forçando a abertura do App...")
    drv.activate_app("com.wbd.stream")

    # Opcional: Espera 5 segundos para garantir que carregou a Home
    time.sleep(5)

    yield drv

    # 3. Fecha tudo no final
    drv.quit()

@pytest.fixture(autouse=True)
def reset_app_para_home(driver_session):
    driver = driver_session
    yield
    print("\n[Teardown] Reiniciando app...")
    try:
        driver.terminate_app("com.wbd.stream")
        driver.activate_app("com.wbd.stream")
    except:
        pass


@pytest.fixture
def driver(driver_session):
    return driver_session


# --- FUNÇÕES AUXILIARES ---

def wait_and_click(driver, by, value, timeout=20):
    wait = WebDriverWait(driver, timeout)
    element = wait.until(EC.element_to_be_clickable((by, value)))
    element.click()
    return element


def wait_for_element(driver, by, value, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.presence_of_element_located((by, value)))


def buscar_conteudo(driver, nome_conteudo):
    print(f"Buscando por: {nome_conteudo}")
    try:
        wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, 'Buscar')
    except:
        xpath_busca = "//*[contains(@content-desc, 'Busca') or contains(@content-desc, 'Search')]"
        wait_and_click(driver, AppiumBy.XPATH, xpath_busca)

    search_input = wait_for_element(driver, AppiumBy.CLASS_NAME, "android.widget.EditText")
    search_input.click()
    search_input.send_keys(nome_conteudo)
    driver.press_keycode(66)  # Enter

    xpath_resultado = f"//*[contains(@text, '{nome_conteudo}')]"
    wait_and_click(driver, AppiumBy.XPATH, xpath_resultado)
    print("Entrou na tela de detalhes.")


# --- O TESTE AJUSTADO ---

def test_adicionar_minha_lista(driver):
    nome_filme = "The Last of Us"

    # 1. Busca e entra nos detalhes
    buscar_conteudo(driver, nome_filme)

    # 2. Clicar no Menu de 3 Pontinhos
    print(f"Procurando menu de opções...")
    # XPath robusto para o menu de kebab
    xpath_menu = f"//*[contains(@content-desc, 'Menu de') or starts-with(@content-desc, 'Menu de')]"
    wait_and_click(driver, AppiumBy.XPATH, xpath_menu)

    print("Menu clicado. Aguardando popup...")
    time.sleep(2)

    # 3. Interagir com o Popup
    # Procura texto "lista" (serve para 'Adicione à lista' ou 'Remover da lista')
    selector_popup = 'new UiSelector().textContains("lista")'

    try:
        botao_popup = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector_popup)
        texto_botao = botao_popup.text
        print(f"Opção encontrada: '{texto_botao}'")
    except:
        assert False, "Opção de lista não apareceu no popup."

    # Lógica de Toggle (Se já tem, remove e adiciona de novo)
    if "Remover" in texto_botao or "Remove" in texto_botao:
        print("Item já na lista. Removendo...")
        botao_popup.click()
        time.sleep(2)

        # Abre menu de novo e adiciona
        wait_and_click(driver, AppiumBy.XPATH, xpath_menu)
        time.sleep(1)
        driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Adicione")').click()
    else:
        print("Clicando em Adicionar...")
        botao_popup.click()

    # 4. VALIDAÇÃO (Navegação corrigida com seus IDs)
    print("Navegando para validar...")
    time.sleep(2)

    # Passo de segurança: Voltar 1 vez garante que saímos do detalhes/popup
    # e a barra inferior (Home/Minhas Coisas) fica visível.
    driver.back()

    print("Clicando em Início...")
    try:
        # Tenta clicar no Início primeiro para garantir o estado
        wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Início")
    except:
        # Se falhar (talvez precise voltar mais uma vez), tenta voltar e clica de novo
        print("Botão Início não visível, voltando mais uma vez...")
        driver.back()
        wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Início")

    print("Clicando em Minhas Coisas...")
    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Minhas Coisas")

    # 5. Validar se o filme está lá
    print(f"Verificando a lista...")

    # Procura pelo texto do filme na tela de Minhas Coisas
    xpath_filme = f"//*[contains(@text, '{nome_filme}')]"

    try:
        wait_for_element(driver, AppiumBy.XPATH, xpath_filme, timeout=10)
        print("SUCESSO: O filme apareceu na lista 'Minhas Coisas'!")
    except:
        # Debug: Se falhar, imprime o XML para vermos o que tem na tela "Minhas Coisas"
        print("FALHA: Filme não encontrado. XML da tela atual:")
        print(driver.page_source)
        assert False, "Filme não encontrado na aba Minhas Coisas."


def test_remover_da_lista(driver):
    """
    Cenário:
    1. Buscar e entrar nos detalhes.
    2. GARANTIR que o item está na lista (se não estiver, adiciona).
    3. Clicar no Menu > Remover.
    4. Ir em Minhas Coisas e validar que o item SUMIU.
    """
    nome_filme = "The Last of Us"

    # 1. Busca e entra nos detalhes
    buscar_conteudo(driver, nome_filme)

    # 2. Localizar Menu de 3 Pontinhos
    print("Abrindo menu de opções...")
    xpath_menu = f"//*[contains(@content-desc, 'Menu de') or starts-with(@content-desc, 'Menu de')]"
    wait_and_click(driver, AppiumBy.XPATH, xpath_menu)
    time.sleep(2)

    # 3. Verificar estado atual (Adicionar ou Remover?)
    selector_popup = 'new UiSelector().textContains("lista")'
    try:
        botao_popup = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector_popup)
        texto_botao = botao_popup.text
        print(f"Estado inicial: '{texto_botao}'")
    except:
        assert False, "Popup de opções não apareceu."

    # --- PRÉ-CONDIÇÃO: O item TEM que estar na lista para podermos remover ---
    if "Adicione" in texto_botao or "Add" in texto_botao:
        print("Item não estava na lista. Adicionando primeiro (Preparação)...")
        botao_popup.click()
        time.sleep(3)  # Espera salvar
        # Reabre o menu para agora sim fazer o teste de remover
        wait_and_click(driver, AppiumBy.XPATH, xpath_menu)
        time.sleep(2)
        # Atualiza a referência do botão
        botao_popup = driver.find_element(AppiumBy.ANDROID_UIAUTOMATOR, selector_popup)

    # --- AÇÃO DO TESTE: REMOVER ---
    print("Clicando em REMOVER...")
    # Aqui garantimos que estamos clicando em "Remover"
    if "Remover" in botao_popup.text or "Remove" in botao_popup.text:
        botao_popup.click()
        time.sleep(2)  # Espera o backend processar
    else:
        assert False, "Falha na lógica de estado. Deveria estar pronto para remover."

    # 4. VALIDAÇÃO (Item NÃO deve existir em Minhas Coisas)
    print("Navegando para validar a ausência...")

    driver.back()  # Fecha detalhes/teclado
    try:
        wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Início")
    except:
        driver.back()  # Tenta voltar mais uma vez se necessário
        wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Início")

    wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Minhas Coisas")

    print(f"Verificando se '{nome_filme}' sumiu da lista...")
    xpath_filme = f"//*[contains(@text, '{nome_filme}')]"

    # --- ASSERTIVA NEGATIVA ---
    # Usamos WebDriverWait com timeout curto.
    # SUCESSO = O elemento NÃO ser encontrado (TimeoutException)
    # FALHA = O elemento ser encontrado (significa que não removeu)
    try:
        WebDriverWait(driver, 5).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath_filme)))

        # Se chegou aqui, é porque encontrou o filme -> ERRO!
        print("FALHA: O filme ainda está na lista!")
        assert False, f"O título '{nome_filme}' deveria ter sido removido, mas ainda está visível."

    except TimeoutException:
        # Se deu timeout, é porque não achou o filme -> SUCESSO!
        print("SUCESSO: O filme não foi encontrado na lista (Timeout esperado).")