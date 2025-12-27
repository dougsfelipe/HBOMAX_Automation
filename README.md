# HBO Max Mobile Automation

This project contains automated E2E tests for the HBO Max Android application using **Appium**, **Python**, and **Pytest**. The project is structured using the **Page Object Model (POM)** pattern for better maintainability and scalability.

## 🚀 Features

- **Page Object Model (POM)** architecture.
- **Pytest** framework for test execution and fixtures.
- **HTML Reporting** with `pytest-html`.
- **Automatic Screenshots** on test failure embedded in the report.
- **Centralized Configuration** via `conftest.py`.

## 🛠️ Technologies

- [Python 3.x](https://www.python.org/)
- [Appium](https://appium.io/)
- [Pytest](https://docs.pytest.org/)
- [Selenium](https://www.selenium.dev/)

## 📂 Project Structure

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

## ⚙️ Prerequisites

1.  **Python 3.x** installed.
2.  **Appium Server** installed and running (default: `http://127.0.0.1:4723`).
3.  **Android SDK** configured.
4.  **Android Emulator/Device** connected.
5.  **HBO Max App** (`com.wbd.stream`) installed on the device.

## 📦 Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/dougsfelipe/HBOMAX_Automation.git
    cd HBOMAX_Automation
    ```

2.  Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv .venv
    # Windows:
    .\.venv\Scripts\activate
    # Mac/Linux:
    source .venv/bin/activate
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Running Tests

### Run all tests
```bash
pytest -v
```

### Run with HTML Report
Generates a `report.html` file in the root directory.
```bash
pytest -v --html=report.html --self-contained-html
```

### Run specific test file
```bash
pytest tests/test_playback_resume.py
```

### Run specific test case
```bash
pytest tests/test_search.py::test_search_existing_title
```

## 📊 Reporting & Debugging

- **HTML Report**: After running with the `--html` flag, open `report.html` in your browser to view detailed results.
- **Screenshots**: If a test fails, a screenshot is automatically taken and saved in the `screenshots/` directory. It is also embedded directly into the HTML report.
