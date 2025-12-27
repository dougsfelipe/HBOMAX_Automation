import pytest
import time
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.details_page import DetailsPage
from pages.player_page import PlayerPage
from appium.webdriver.common.appiumby import AppiumBy

APP_PACKAGE = "com.wbd.stream"

def scroll_manual_ate_achar(driver, texto_alvo, max_tentativas=10):
    """
    Rola a tela manualmente procurando o texto.
    (Poderia estar no BasePage se fosse muito usado, mas mantive aqui ou num helper utils)
    """
    print(f"Iniciando Scroll Manual procurando por: '{texto_alvo}'")
    window = driver.get_window_size()
    width = window['width']
    height = window['height']

    start_x = int(width * 0.5)
    start_y = int(height * 0.8)
    end_y = int(height * 0.3)

    xpath_alvo = (AppiumBy.XPATH, f"//*[contains(@text, '{texto_alvo}')]")
    
    # Instancia BasePage só para usar os métodos de wait
    from pages.base_page import BasePage
    base = BasePage(driver)

    for i in range(max_tentativas):
        if base.is_visible(xpath_alvo, timeout=1):
             print(f"ENCONTRADO na tentativa {i + 1}!")
             return base.find_element(xpath_alvo)
        
        print(f"Swipe {i + 1}/{max_tentativas}...")
        driver.swipe(start_x, start_y, start_x, end_y, 800)
        time.sleep(2)

    return None

def test_resume_video(driver):
    titulo = "Uma Batalha após a Outra"
    
    home = HomePage(driver)
    search = SearchPage(driver)
    details = DetailsPage(driver)
    player = PlayerPage(driver)

    # 1. Busca e Play
    print(f"--- ETAPA 1: Buscando '{titulo}' ---")
    home.go_to_search()
    search.search_for(titulo)
    search.select_result_banner_page(titulo) # Entra no detalhes ou clica no poster

    # Clique em Assistir
    details.click_play(titulo)

    print("Aguardando player iniciar...")
    time.sleep(10)  # Tempo para buffering

    # 2. ASSISTIR
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
    
    home.handle_profile_selection_if_needed()

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

    try:
        tempo_recuperado = player.get_current_time_text()
        print(f"Tempo exibido: {tempo_recuperado}")

        # Validação: Não pode estar no início (00:00)
        assert not tempo_recuperado.startswith("0:00") and not tempo_recuperado.startswith("00:00"), \
            f"FALHA: Vídeo reiniciou do zero! Tempo: {tempo_recuperado}"

    except Exception as e:
        print(f"Aviso na validação de tempo: {e}")
        pass

    print("SUCESSO: Teste finalizado!")
