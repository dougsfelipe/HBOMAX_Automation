import pytest
import time
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.details_page import DetailsPage
from selenium.common.exceptions import TimeoutException
from appium.webdriver.common.appiumby import AppiumBy

def test_add_to_my_list(driver):
    nome_filme = "The Last of Us"
    
    home = HomePage(driver)
    search = SearchPage(driver)
    details = DetailsPage(driver)

    # 1. Busca e entra nos detalhes
    home.go_to_search()
    search.search_for(nome_filme)
    search.select_result(nome_filme)

    # 2. Interagir com o Popup de Minha Lista
    # A lógica complexa de toggle foi movida para o Page Object
    details.add_to_list_if_not_present()

    # 3. VALIDAÇÃO
    print("Navegando para validar...")
    home.go_to_home() # Volta para início de forma segura
    home.go_to_my_stuff()

    # 4. Validar se o filme está lá
    print(f"Verificando a lista...")
    
    # Aqui poderíamos criar um MyStuffPage, mas vamos usar o método genérico do BasePage/SearchPage por simplicidade ou adicionar aqui
    # Como a validação é só checar se o título existe, usamos is_result_displayed do SearchPage que é genérico ou direto do driver
    xpath_filme = (AppiumBy.XPATH, f"//*[contains(@text, '{nome_filme}')]")
    
    if details.is_visible(xpath_filme, timeout=10):
         print("SUCESSO: O filme apareceu na lista 'Minhas Coisas'!")
    else:
        print("FALHA: Filme não encontrado. XML da tela atual:")
        print(driver.page_source)
        assert False, "Filme não encontrado na aba Minhas Coisas."


def test_remove_from_list(driver):
    """
    Cenário:
    1. Buscar e entrar nos detalhes.
    2. GARANTIR que o item está na lista.
    3. Remover.
    4. Validar que SUMIU.
    """
    nome_filme = "The Last of Us"
    
    home = HomePage(driver)
    search = SearchPage(driver)
    details = DetailsPage(driver)

    # 1. Busca e entra nos detalhes
    home.go_to_search()
    search.search_for(nome_filme)
    search.select_result(nome_filme)

    # 2. Garantir que está na lista antes de remover
    details.ensure_item_in_list()
    
    # 3. Remover
    details.remove_from_list()

    # 4. VALIDAÇÃO
    print("Navegando para validar a ausência...")
    details.back() # Fecha detalhes
    home.go_to_home()
    home.go_to_my_stuff()

    print(f"Verificando se '{nome_filme}' sumiu da lista...")
    xpath_filme = (AppiumBy.XPATH, f"//*[contains(@text, '{nome_filme}')]")

    # Check negativo
    if not details.is_visible(xpath_filme, timeout=5):
        print("SUCESSO: O filme não foi encontrado na lista (Timeout esperado).")
    else:
        print("FALHA: O filme ainda está na lista!")
        assert False, f"O título '{nome_filme}' deveria ter sido removido, mas ainda está visível."
