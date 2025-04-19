from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.profile_locators import ProfileLocators
class ProfilePage(BasePage):

    def is_profile_page_opened(self):
        return WebDriverWait(self.driver, 10).until(
            EC.url_contains("/account/profile")
        )

    def go_to_history(self):
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable(ProfileLocators.HISTORY_TAB)
        )
        self.click(ProfileLocators.HISTORY_TAB)

    def get_order_history_numbers(self):
        # Дождаться загрузки хотя бы одного заказа в истории
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located(ProfileLocators.ORDER_HISTORY_NUMBERS)
        )
        # Получаем все элементы с номерами
        elements = self.driver.find_elements(*ProfileLocators.ORDER_HISTORY_NUMBERS)
        # Возвращаем список номеров без # и нулей впереди
        return [
            el.text.strip().lstrip('#').lstrip('0') or '0'
            for el in elements
            if el.text.strip().lstrip('#').isdigit()
        ]

    def logout(self):
        self.click(ProfileLocators.LOGOUT_BUTTON)
