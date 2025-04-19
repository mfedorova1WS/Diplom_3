from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.restore_password_locators import RestorePasswordLocators

class RestorePasswordPage(BasePage):
    def enter_email(self, email):
        self.enter_text(RestorePasswordLocators.EMAIL_INPUT, email)

    def click_restore(self):
        self.click(RestorePasswordLocators.RESTORE_BUTTON)

    def is_password_field_active(self):
        """Проверяет, что поле для ввода нового пароля активно и отображается"""
        try:
            password_field = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(RestorePasswordLocators.PASSWORD_FIELD)
            )
            return password_field.is_displayed() and password_field.is_enabled()
        except:
            return False