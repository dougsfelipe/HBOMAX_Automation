from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class SearchPage(BasePage):
    # Locators
    SEARCH_INPUT = (AppiumBy.CLASS_NAME, "android.widget.EditText")
    
    def search_for(self, term):
        self.send_keys(self.SEARCH_INPUT, term)
        print("Enviando ENTER...")
        self.press_enter()
        # Pequena espera para carregamento dos resultados
        time.sleep(3) 

    def is_result_displayed(self, title):
        xpath_result = (AppiumBy.XPATH, f"//*[contains(@text, '{title}')]")
        return self.is_visible(xpath_result, timeout=10)




    def select_result(self, title):
        xpath_result = (AppiumBy.XPATH, f"//*[contains(@text, '{title}')]")
        self.wait_and_click(xpath_result)

    def select_result_banner_page(self, title):
        # O 'contains' resolve o problema dos caracteres invisíveis 
        xpath_result = (AppiumBy.XPATH, f"//android.widget.TextView[contains(@text, '{title}')]")
        self.wait_and_click(xpath_result)


    def get_error_message(self, partial_text):
        xpath_error = (AppiumBy.XPATH, f"//*[contains(@text, '{partial_text}')]")
        if self.is_visible(xpath_error):
            return self.get_text(xpath_error)
        return None
