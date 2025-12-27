import pytest
import time
from appium import webdriver
from appium.options.common.base import AppiumOptions

APP_PACKAGE = "com.wbd.stream"

@pytest.fixture(scope="session")
def driver_session():
    options = AppiumOptions()
    options.load_capabilities({
        "platformName": "Android",
        "appium:automationName": "UiAutomator2",
        "appium:appPackage": APP_PACKAGE,
        "appium:appWaitActivity": "*",
        "appium:ensureWebviewsHavePages": True,
        "appium:nativeWebScreenshot": True,
        "appium:newCommandTimeout": 3600,
        "appium:connectHardwareKeyboard": True,
        "appium:noReset": True,
        "appium:adbExecTimeout": 60000,
    })

    print("Conectando ao Appium...")
    drv = webdriver.Remote("http://127.0.0.1:4723", options=options)
    
    # Força o app a abrir explicitamente
    print("Forçando a abertura do App...")
    drv.activate_app(APP_PACKAGE)
    time.sleep(5)
    
    yield drv
    
    drv.quit()

@pytest.fixture(autouse=True)
def reset_app_para_home(driver_session):
    driver = driver_session
    # Garante que o app está ativo antes do teste
    driver.activate_app(APP_PACKAGE)
    
    yield
    
    # Teardown: Reinicia app para garantir estado limpo para o próximo teste
    print("\n[Teardown] Reiniciando app...")
    try:
        driver.terminate_app(APP_PACKAGE)
        time.sleep(2)
        driver.activate_app(APP_PACKAGE)
        time.sleep(5) 
    except Exception as e:
        print(f"Erro no teardown: {e}")

@pytest.fixture
def driver(driver_session):
    return driver_session

# --- HOOKS PARA REPORT E SCREENSHOT ---

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Executa o resto dos hooks para obter o relatório
    outcome = yield
    report = outcome.get_result()

    # Apenas se for uma falha ou setup error
    if report.when == 'call' or report.when == "setup":
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            # Tenta pegar o driver da fixture 'driver' ou 'driver_session'
            driver = None
            if "driver" in item.funcargs:
                driver = item.funcargs["driver"]
            elif "driver_session" in item.funcargs:
                driver = item.funcargs["driver_session"]
            
            if driver:
                add_screenshot_to_report(report, driver)

def add_screenshot_to_report(report, driver):
    import os
    try:
        screenshots_dir = os.path.join(os.getcwd(), "screenshots")
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        timestamp = time.strftime("%Y%m%d-%H%M%S")
        screenshot_name = f"screenshot_{timestamp}.png"
        screenshot_path = os.path.join(screenshots_dir, screenshot_name)
        
        # Salva localmente na pasta correta
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot salvo em: {screenshot_path}")
        
        # Anexa ao HTML (requer pytest-html)
        # O extra deve ser adicionado ao report
        if not hasattr(report, 'extra'):
             report.extra = []
        
        # Lê a imagem em base64 para embedar
        import base64
        screenshot_b64 = driver.get_screenshot_as_base64()
        html = f'<div><img src="data:image/png;base64,{screenshot_b64}" alt="screenshot" style="width:600px;height:auto;" onclick="window.open(this.src)" align="right"/></div>'
        
        # Adiciona como HTML extra
        from pytest_html import extras
        report.extra.append(extras.html(html))
        
    except Exception as e:
        print(f"Erro ao tirar screenshot: {e}")
