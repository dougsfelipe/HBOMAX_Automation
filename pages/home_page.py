from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage

class HomePage(BasePage):
    # Locators
    SEARCH_BUTTON_ID = (AppiumBy.ACCESSIBILITY_ID, "Buscar")
    SEARCH_BUTTON_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Busca') or contains(@content-desc, 'Search')]")
    
    HOME_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Início")
    MY_STUFF_BUTTON = (AppiumBy.ACCESSIBILITY_ID, "Minhas Coisas")
    
    PROFILE_ICON = (AppiumBy.ID, "com.wbd.stream:id/profile_icon") # Exemplo hipotético para seleção de perfil
    WHO_IS_WATCHING_TEXT = (AppiumBy.XPATH, "//*[contains(@text, 'Quem está assistindo')]")

    def go_to_search(self):
        try:
            self.wait_and_click(self.SEARCH_BUTTON_ID)
        except:
            self.wait_and_click(self.SEARCH_BUTTON_XPATH)

    def go_to_home(self):
        try:
            self.wait_and_click(self.HOME_BUTTON)
        except:
            # Tenta voltar se necessário
            self.back()
            self.wait_and_click(self.HOME_BUTTON)

    def go_to_my_stuff(self):
        self.wait_and_click(self.MY_STUFF_BUTTON)

    def handle_profile_selection_if_needed(self):
        if self.is_visible(self.WHO_IS_WATCHING_TEXT, timeout=5):
             print("Selecionando perfil...")
             # Tenta clicar no meio da tela ou em um perfil específico
             # Ajuste conforme necessário, aqui usando tap
             window = self.driver.get_window_size()
             self.driver.tap([(int(window['width'] / 2), int(window['height'] / 2))])
             # Aguarda carregamento
             import time
             time.sleep(5)
