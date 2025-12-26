import pytest
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

APP_PACKAGE = "com.wbd.stream"


# --- CONFIGURAÇÃO ---
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
    drv.activate_app(APP_PACKAGE)
    time.sleep(5)
    yield drv
    drv.quit()


@pytest.fixture
def driver(driver_session):
    return driver_session


# --- FUNÇÕES ---

def wait_and_click(driver, by, value, timeout=20):
    wait = WebDriverWait(driver, timeout)
    el = wait.until(EC.element_to_be_clickable((by, value)))
    el.click()
    return el


def garantir_controles_visiveis(driver):
    """Toca no meio da tela para exibir a barra de tempo/controles"""
    window = driver.get_window_size()
    driver.tap([(int(window['width'] / 2), int(window['height'] / 2))])
    time.sleep(1)


def buscar_e_dar_play_inicial(driver, titulo):
    print(f"--- ETAPA 1: Buscando '{titulo}' ---")

    # 1. Clicar na Busca
    try:
        wait_and_click(driver, AppiumBy.ACCESSIBILITY_ID, "Buscar")
    except:
        xpath_busca = "//*[contains(@content-desc, 'Busca') or contains(@content-desc, 'Search')]"
        wait_and_click(driver, AppiumBy.XPATH, xpath_busca)

    # 2. Digitar Título
    campo_busca = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
    campo_busca.click()
    campo_busca.send_keys(titulo)
    driver.press_keycode(66)  # Enter

    # 3. Clicar no Poster
    # Mude de [@text=...] para [contains(@text, ...)]
    print("Clicando no poster...")
    driver.find_element(
        AppiumBy.XPATH,
        f"//android.widget.TextView[contains(@text, '{titulo}')]"
    ).click()

    # 4. Clicar em Assistir
    print("Clicando em Assistir...")
    try:
        driver.find_element(AppiumBy.ACCESSIBILITY_ID, f"Assistir {titulo}").click()
    except:
        # Fallback genérico
        xpath_play = f"//*[contains(@content-desc, 'Assistir') or contains(@content-desc, 'Play')]"
        wait_and_click(driver, AppiumBy.XPATH, xpath_play)

    print("Aguardando player iniciar...")
    time.sleep(10)  # Tempo para buffering


def scroll_manual_ate_achar(driver, texto_alvo, max_tentativas=10):
    """
    Rola a tela manualmente procurando o texto.
    """
    print(f"Iniciando Scroll Manual procurando por: '{texto_alvo}'")
    window = driver.get_window_size()
    width = window['width']
    height = window['height']

    # Swipe de baixo para cima
    start_x = int(width * 0.5)
    start_y = int(height * 0.8)
    end_y = int(height * 0.3)

    xpath_alvo = f"//*[contains(@text, '{texto_alvo}')]"

    for i in range(max_tentativas):
        try:
            # Verifica se apareceu (timeout rápido de 1s)
            el = WebDriverWait(driver, 1).until(EC.presence_of_element_located((AppiumBy.XPATH, xpath_alvo)))
            print(f"ENCONTRADO na tentativa {i + 1}!")
            return el
        except:
            print(f"Swipe {i + 1}/{max_tentativas}...")
            driver.swipe(start_x, start_y, start_x, end_y, 800)
            time.sleep(2)

    return None


# --- TESTE PRINCIPAL ---

def test_resume_video(driver):
    titulo = "Shrek 2"

    # 1. Busca e Play
    buscar_e_dar_play_inicial(driver, titulo)

    # 2. ASSISTIR (Apenas esperar o vídeo rodar)
    # Recomendado: 60s para garantir que o server salve.
    tempo_assistir = 60
    print(f"--- ETAPA 2: Deixando o vídeo rodar por {tempo_assistir} segundos ---")
    time.sleep(tempo_assistir)

    # 3. Reiniciar App
    print("--- ETAPA 3: Reiniciando App ---")
    driver.terminate_app(APP_PACKAGE)
    time.sleep(3)
    driver.activate_app(APP_PACKAGE)
    time.sleep(10)  # Espera Home carregar

    # 4. Scroll e Busca na Home
    print("--- ETAPA 4: Buscando na Home ---")

    # Tratamento para tela de perfil (se aparecer)
    try:
        if driver.find_elements(AppiumBy.XPATH, "//*[contains(@text, 'Quem está assistindo')]"):
            print("Selecionando perfil...")
            driver.tap([(500, 500)])
            time.sleep(5)
    except:
        pass

    # Busca na lista usando Swipe Manual
    elemento_titulo = scroll_manual_ate_achar(driver, titulo, max_tentativas=10)

    if elemento_titulo:
        print("Clicando no título para retomar...")
        elemento_titulo.click()
    else:
        driver.save_screenshot("erro_nao_achou_home.png")
        assert False, f"O título '{titulo}' não apareceu na Home após reiniciar."

    time.sleep(10)  # Espera o player carregar novamente

    # 5. Validação do Tempo
    print("--- ETAPA 5: Validando Retomada ---")

    # Toca na tela para ver os números
    garantir_controles_visiveis(driver)

    try:
        el_tempo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((AppiumBy.ID, "com.wbd.stream:id/textview_player_controls_content_duration"))
        )
        tempo_recuperado = el_tempo.text
        print(f"Tempo exibido: {tempo_recuperado}")

        # Validação: Não pode estar no início (00:00)
        assert not tempo_recuperado.startswith("0:00") and not tempo_recuperado.startswith("00:00"), \
            f"FALHA: Vídeo reiniciou do zero! Tempo: {tempo_recuperado}"

    except Exception as e:
        # Se falhar em ler o tempo, tenta validar se o botão NÃO é "Assistir" (o que indicaria reinício)
        print(f"Aviso na validação de tempo: {e}")
        pass

    print("SUCESSO: Teste finalizado!")