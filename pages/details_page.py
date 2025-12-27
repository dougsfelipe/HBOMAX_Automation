from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class DetailsPage(BasePage):
    # Locators
    MENU_BUTTON = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Menu de') or starts-with(@content-desc, 'Menu de')]")
    MENU_POPUP_LIST_OPTION = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("lista")')
    MENU_POPUP_ADD = (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Adicione")')
    PLAY_BUTTON_ACCESSIBILITY = (AppiumBy.ACCESSIBILITY_ID, "Assistir") # Parcial, dinâmico
    PLAY_BUTTON_XPATH = (AppiumBy.XPATH, "//*[contains(@content-desc, 'Assistir') or contains(@content-desc, 'Play')]")

    def open_menu(self):
        print("Abrindo menu de opções...")
        self.wait_and_click(self.MENU_BUTTON)
        time.sleep(2)

    def get_list_button_text(self):
        # Assume que o menu já está aberto
        element = self.find_element(self.MENU_POPUP_LIST_OPTION)
        return element.text

    def click_list_option(self):
        self.wait_and_click(self.MENU_POPUP_LIST_OPTION)
        time.sleep(2) # Espera ação concluir

    def add_to_list_if_not_present(self):
        self.open_menu()
        text = self.get_list_button_text()
        
        if "Remover" in text or "Remove" in text:
            print("Item já na lista. Removendo para re-adicionar...")
            self.click_list_option()
            # Reabre menu
            self.open_menu()
            text = self.get_list_button_text()

        if "Adicione" in text or "Add" in text:
             print("Clicando em Adicionar...")
             self.click_list_option()
        else:
            raise Exception("Estado do botão de lista desconhecido: " + text)

    def ensure_item_in_list(self):
        """Garante que o item está na lista. Se não estiver, adiciona."""
        self.open_menu()
        text = self.get_list_button_text()
        if "Adicione" in text or "Add" in text:
            print("Item não estava na lista. Adicionando...")
            self.click_list_option()
        else:
            print("Item já estava na lista.")
            # Fecha o menu clicando fora ou voltando (aqui vamos só fechar o menu clicando no mesmo botão se for toggle ou back)
            # Como é um popup, clicar fora ou back costuma funcionar.
            self.back()
    
    def remove_from_list(self):
        self.open_menu()
        text = self.get_list_button_text()
        if "Remover" in text or "Remove" in text:
            print("Clicando em Remover...")
            self.click_list_option()
        else:
             raise Exception("Falha: Tentando remover item que não está na lista.")

    def click_play(self, title_hint=""):
        print(f"Tentando dar Play (Assistir ou Retomar)...")
        
        try:
            
            if title_hint:
                xpath_smart = (
                    f"//*[(contains(@content-desc, 'Assistir') or contains(@content-desc, 'Retome')) "
                    f"and contains(@content-desc, '{title_hint}')]"
                )
            else:
                # Se não passar o título, procura qualquer botão de ação principal
                xpath_smart = "//*[contains(@content-desc, 'Assistir') or contains(@content-desc, 'Retome')]"

            self.driver.find_element(AppiumBy.XPATH, xpath_smart).click()
            print(f"Botão de ação '{xpath_smart}' clicado com sucesso.")

        except Exception:
            # Fallback (Se falhar ou se o botão for apenas um ícone sem texto)
            print("Botão específico com texto não encontrado. Usando Fallback genérico...")
            self.wait_and_click(self.PLAY_BUTTON_XPATH)
