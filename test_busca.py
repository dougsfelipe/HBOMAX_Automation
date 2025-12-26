import pytest
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APP_PACKAGE = "com.wbd.stream"


# --- CONFIGURAÇÃO (SETUP) ---
@pytest.fixture(scope="session")
def driver_session():
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": APP_PACKAGE,
        "appium:appWaitActivity": "*",
        "appium:noReset": True,
        "appium:newCommandTimeout": 300,
        "appium:adbExecTimeout": 60000,
        "appium:ensureWebviewsHavePages": True
    })

    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)
    # Garante app aberto
    drv.activate_app(APP_PACKAGE)
    time.sleep(5)
    yield drv
    drv.quit()


@pytest.fixture(autouse=True)
def reset_app(driver_session):
    """
    Reinicia o app ANTES e DEPOIS de cada teste para garantir a Home limpa.
    """
    driver = driver_session
    # Garante que está na frente
    driver.activate_app(APP_PACKAGE)

    yield

    # Teardown: Fecha e reabre para limpar a busca anterior
    print("\n[Teardown] Reiniciando app para limpar busca...")
    driver.terminate_app(APP_PACKAGE)
    time.sleep(2)
    driver.activate_app(APP_PACKAGE)
    time.sleep(5)  # Espera Home carregar


@pytest.fixture
def driver(driver_session):
    return driver_session


# --- FUNÇÕES AUXILIARES ---

def wait_and_click(driver, by, value, timeout=20):
    wait = WebDriverWait(driver, timeout)
    el = wait.until(EC.element_to_be_clickable((by, value)))
    el.click()
    return el


def realizar_busca(driver, termo):
    """
    Passo a passo comum para clicar na lupa e digitar
    """
    print(f"Iniciando busca por: '{termo}'")

    # 1. Clicar na lupa (Menu Inferior)
    try:
        wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Buscar")
    except:
        # Fallback se o ID mudar ou estiver em inglês
        xpath_lupa = "//*[contains(@content-desc, 'Busca') or contains(@content-desc, 'Search')]"
        wait_and_click(driver, AppiumBy.XPATH, xpath_lupa)

    # 2. Clicar no campo e Digitar
    campo_busca = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
    )
    campo_busca.click()
    campo_busca.send_keys(termo)

    # 3. Confirmar (Enter do teclado Android)
    print("Enviando ENTER...")
    driver.press_keycode(66)
    time.sleep(3)  # Espera resultados carregarem


# --- CASOS DE TESTE ---

def test_ct05_busca_titulo_existente(driver):
    """
    CT-05: Busque por um Título Existente
    """
    titulo_alvo = "SMILING FRIENDS"

    # Ação
    realizar_busca(driver, titulo_alvo)

    # Validação
    print("Validando se o título apareceu nos resultados...")

    # Usamos contains para evitar erro com caracteres ocultos (⁨Smiling Friends⁩)
    xpath_resultado = f"//android.widget.TextView[contains(@text, '{titulo_alvo}')]"

    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath_resultado))
        )
        print(f"SUCESSO: Título '{titulo_alvo}' encontrado na tela.")
    except:
        driver.save_screenshot(f"erro_busca_{titulo_alvo}.png")
        assert False, f"O título '{titulo_alvo}' não foi exibido nos resultados da busca."


def test_ct06_busca_titulo_inexistente(driver):
    """
    CT-06: Busque por um Título Inexistente
    """
    termo_inexistente = "boucha"

    # Ação
    realizar_busca(driver, termo_inexistente)

    # Validação
    print("Validando mensagem de erro...")

    # Texto esperado (parcial é mais seguro para evitar erros de quebra de linha)
    # Frase completa: "Parece que não temos esse conteúdo. Confira estes outros títulos ou tente uma pesquisa diferente"
    trecho_chave = "Parece que não temos esse conteúdo"

    xpath_erro = f"//*[contains(@text, '{trecho_chave}')]"

    try:
        el = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.XPATH, xpath_erro))
        )
        print("SUCESSO: Mensagem de 'conteúdo não encontrado' exibida corretamente.")
        print(f"Texto encontrado: {el.text}")

    except:
        # Debug: Imprime a tela para ver se apareceu outra coisa
        print("FALHA: Mensagem de erro não encontrada. XML da tela:")
        # print(driver.page_source) # Descomente se precisar debugar
        driver.save_screenshot("erro_busca_negativa.png")

        # Verifica se por acaso ele achou algum resultado (Falso Positivo)
        resultados = driver.find_elements(AppiumBy.XPATH, f"//*[contains(@text, '{termo_inexistente}')]")
        if resultados:
            assert False, f"ERRO: A busca deveria falhar, mas encontrou resultados para '{termo_inexistente}'."

        assert False, f"A mensagem contendo '{trecho_chave}' não apareceu."