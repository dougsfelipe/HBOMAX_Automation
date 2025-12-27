import pytest
from pages.home_page import HomePage
from pages.search_page import SearchPage

def test_search_existing_title(driver):
    """
    CT-05: Busque por um Título Existente
    """
    home = HomePage(driver)
    search = SearchPage(driver)
    
    titulo_alvo = "SMILING FRIENDS"

    # Ação
    home.go_to_search()
    search.search_for(titulo_alvo)

    # Validação
    print("Validando se o título apareceu nos resultados...")
    if search.is_result_displayed(titulo_alvo):
        print(f"SUCESSO: Título '{titulo_alvo}' encontrado na tela.")
    else:
        driver.save_screenshot(f"erro_busca_{titulo_alvo}.png")
        assert False, f"O título '{titulo_alvo}' não foi exibido nos resultados da busca."

def test_search_non_existent_title(driver):
    """
    CT-06: Busque por um Título Inexistente
    """
    home = HomePage(driver)
    search = SearchPage(driver)

    termo_inexistente = "boucha"

    # Ação
    home.go_to_search()
    search.search_for(termo_inexistente)

    # Validação
    print("Validando mensagem de erro...")
    trecho_chave = "Parece que não temos esse conteúdo"
    
    msg = search.get_error_message(trecho_chave)
    
    if msg:
        print("SUCESSO: Mensagem de 'conteúdo não encontrado' exibida corretamente.")
        print(f"Texto encontrado: {msg}")
    else:
        driver.save_screenshot("erro_busca_negativa.png")
        # Verifica falso positivo
        if search.is_result_displayed(termo_inexistente):
            assert False, f"ERRO: A busca deveria falhar, mas encontrou resultados para '{termo_inexistente}'."
        
        assert False, f"A mensagem contendo '{trecho_chave}' não apareceu."
