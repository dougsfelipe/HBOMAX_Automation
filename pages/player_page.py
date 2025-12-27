from appium.webdriver.common.appiumby import AppiumBy
from pages.base_page import BasePage
import time

class PlayerPage(BasePage):
    # Locators
    DURATION_TIME = (AppiumBy.ID, "com.wbd.stream:id/textview_player_controls_content_duration")

    def tap_center_to_show_controls(self):
        window = self.driver.get_window_size()
        self.driver.tap([(int(window['width'] / 2), int(window['height'] / 2))])
        time.sleep(1)

    def get_current_time_text(self):
        self.tap_center_to_show_controls()
        return self.get_text(self.DURATION_TIME)
