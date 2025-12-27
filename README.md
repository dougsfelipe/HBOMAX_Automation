# Automação Mobile HBO Max (Android)

Este projeto contém testes automatizados E2E (Ponta a Ponta) para o aplicativo Android da HBO Max (agora Max) utilizando **Appium**, **Python** e **Pytest**. O projeto está estruturado usando o padrão **Page Object Model (POM)** para melhor manutenibilidade e escalabilidade.

##  Funcionalidades Automatizadas

O foco deste projeto foi o desenvolvimento e automação de casos de testes para funcionalidades críticas do aplicativo. Abaixo estão os cenários detalhados.

###  Funcionalidade 1: Player de Vídeo (Controle de Reprodução)

| ID | Título do Caso | Pré-condições | Passos para execução | Resultado Esperado | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CT-01** | **Retomada de Conteúdo** | Usuário logado e na página de um título (ex: Shrek). | 1. Clicar em “Assistir” e assistir por 60s.<br>2. Fechar o app totalmente.<br>3. Reabrir e rolar até “Continuar Assistindo”.<br>4. Clicar no título na lista. | O vídeo deve iniciar exatamente onde parou (60 seg), sem reiniciar do zero. | ✅ **Automatizado** |
| **CT-02** | **Alteração de Áudio** | Usuário deu play em algum título. | 1. Com vídeo rodando, abrir menu de áudio.<br>2. Trocar idioma (Inglês -> Português). | O áudio deve ser alterado de forma rápida sem travar o vídeo. | ⚠️ **Manual** |

> **Nota sobre o CT-02:** Este caso de teste não foi automatizado devido à complexidade técnica de validar a mudança efetiva da faixa de áudio (análise de som) via Appium em um ambiente de emulação.

###  Funcionalidade 2: Minha Lista

| ID | Título do Caso | Pré-condições | Passos para execução | Resultado Esperado | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CT-03** | **Adicionar título à Lista** | Usuário logado. | 1. Clicar na busca (Menu Inferior).<br>2. Abrir menu (três pontos) no banner.<br>3. Clicar em "+" (Add à lista).<br>4. Ir para Home > Minha Lista. | O ícone deve mudar de estado (check) e o filme deve aparecer visível na lista. | ✅ **Automatizado** |
| **CT-04** | **Remover título da Lista** | Filme já adicionado. | 1. Acessar "Minha Lista".<br>2. Clicar no menu do título.<br>3. Clicar em remover. | O item deve sumir da lista imediatamente e o sistema deve confirmar a remoção. | ✅ **Automatizado** |

###  Funcionalidade 3: Busca por Títulos

| ID | Título do Caso | Pré-condições | Passos para execução | Resultado Esperado | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **CT-05** | **Busca por Título Existente** | Usuário logado. | 1. Clicar na lupa (Menu Inferior).<br>2. Buscar título existente (ex: "Smiling Friends"). | O título correto deve ser exibido nos resultados da busca. | ✅ **Automatizado** |
| **CT-06** | **Busca por Título Inexistente** | Usuário logado. | 1. Clicar na lupa (Menu Inferior).<br>2. Buscar termo inexistente (ex: "boucha"). | Não deve aparecer nenhum título e exibir a mensagem: *"Parece que não temos esse conteúdo..."* | ✅ **Automatizado** |

---

##  Demo da Execução

Você pode ver um exemplo completo de todos os testes rodando no link abaixo:

 **[Assistir Vídeo da Execução dos Testes](https://drive.google.com/file/d/1sH4c8zZWYfibKu6t96PEjZvYuuoR4FF6/view?usp=sharing)**

---

##  Desafios e Dificuldades Gerais

Durante o desenvolvimento da automação, foram encontrados diversos desafios técnicos e comportamentais da aplicação:

1.  **IDs Dinâmicos e Controladores:** Os IDs de acessibilidade e localizadores dos botões (como titulo do banner) mudam dependendo do título selecionado (ex: *"Assistir Shrek"* vs *"Assistir Batman"*), exigindo estratégias de locators dinâmicos (XPath).
2.  **Player de Vídeo Nativo:** A interação com a barra do player (Pause/Play) e os controles que somem automaticamente da tela exigiu o uso de coordenadas e comandos de toque específicos para manter a interface ativa.
3.  **Pop-ups Intermitentes:** O aparecimento aleatório de pop-ups (avaliação do app, novidades, etc.) durante a execução dos testes pode interferir no fluxo.
4.  **Login Abstraído:** Devido a mecanismos de segurança (como CAPTCHA e bloqueios de automação na tela de login), optou-se por realizar os testes com o **usuário já logado**, abstraindo a etapa de autenticação.
5.  **Inconsistência na Busca:** Alguns títulos aparecem em ordens diferentes nos resultados da busca dependendo do momento, exigindo validações mais flexíveis.
6.  **Rebranding (Max vs HBO Max):** A recente mudança da marca e do aplicativo dificultou a busca por documentação e soluções de problemas na internet, pois muito conteúdo ainda se refere à versão antiga do app.

---

##  Tecnologias

- [Python 3.x](https://www.python.org/)
- [Appium](https://appium.io/)
- [Pytest](https://docs.pytest.org/)
- [Selenium](https://www.selenium.dev/)

##  Estrutura do Projeto
```
Mobile_Tests/
├── pages/                  # Page Objects (Locators & Methods)
│   ├── base_page.py        # Base class with common wrappers
│   ├── home_page.py
│   ├── search_page.py
│   ├── details_page.py
│   └── player_page.py
├── tests/                  # Test Scripts
│   ├── test_search.py
│   ├── test_my_list.py
│   └── test_playback_resume.py
├── conftest.py             # Shared Fixtures & Driver Setup
├── report.html             # Generated Test Report (Ignored by Git)
├── screenshots/            # Error Screenshots (Ignored by Git)
└── README.md               # Project Documentation
```

##  Pré-requisitos

1.  **Python 3.x** instalado.
2.  **Servidor Appium** instalado e rodando (padrão: `http://127.0.0.1:4723`).
3.  **Android SDK** configurado.
4.  **Emulador Android/Dispositivo** conectado.
5.  **App HBO Max** (`com.wbd.stream`) instalado no dispositivo.

##  Instalação

1.  Clone o repositório:
    ```bash
    git clone [https://github.com/dougsfelipe/HBOMAX_Automation.git](https://github.com/dougsfelipe/HBOMAX_Automation.git)
    cd HBOMAX_Automation
    ```

2.  Crie e ative um ambiente virtual (opcional, mas recomendado):
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  Instale as dependências via requirements:
    ```bash
    pip install -r requirements.txt
    ```

## Executando os Testes

```bash
pytest -v
  ```

## Rodar com Relatório HTML

Gera um arquivo report.html no diretório raiz.
```bash
pytest -v --html=report.html --self-contained-html
```

### Rodar caso de teste específico
```bash
pytest tests/test_playback_resume.py
```

### Run specific test case
```bash
pytest tests/test_search.py::test_search_existing_title
```

## Relatórios e Debug

- **HTML Report**: Após rodar com a flag --html, abra o arquivo report.html no seu navegador para ver os resultados detalhados.
- **Screenshots**: Se um teste falhar, um screenshot é tirado automaticamente e salvo no diretório screenshots/. Ele também é incorporado diretamente no relatório HTML.
