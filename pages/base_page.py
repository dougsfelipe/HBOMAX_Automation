from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.timeout = 20

    def find_element(self, locator):
        return self.driver.find_element(*locator)

    def find_elements(self, locator):
        return self.driver.find_elements(*locator)

    def wait_for_element(self, locator, timeout=None):
        if timeout is None:
            timeout = self.timeout
        wait = WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def wait_and_click(self, locator, timeout=None):
        if timeout is None:
            timeout = self.timeout
        wait = WebDriverWait(self.driver, timeout)
        element = wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return element

    def click(self, locator):
        self.find_element(locator).click()

    def send_keys(self, locator, text):
        element = self.wait_for_element(locator)
        element.click()
        element.send_keys(text)
    
    def is_visible(self, locator, timeout=5):
        try:
            self.wait_for_element(locator, timeout)
            return True
        except TimeoutException:
            return False

    def press_enter(self):
        self.driver.press_keycode(66)
    
    def back(self):
        self.driver.back()

    def get_text(self, locator):
        return self.wait_for_element(locator).text
