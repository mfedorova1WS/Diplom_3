from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.login_locators import LoginLocators


class LoginPage(BasePage):
    def go_to_restore_password(self):
        """Переход на страницу восстановления пароля"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(LoginLocators.RESTORE_PASSWORD_BUTTON)
        ).click()

    def enter_email(self, email):
        """Ввод email в поле авторизации"""
        email_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LoginLocators.EMAIL_INPUT)
        )
        email_field.clear()
        email_field.send_keys(email)

    def enter_password(self, password):
        """Ввод пароля в поле авторизации"""
        password_field = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(LoginLocators.PASSWORD_INPUT)
        )
        password_field.clear()
        password_field.send_keys(password)

    def click_login(self):
        """Клик по кнопке входа и ожидание перехода на главную страницу"""
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(LoginLocators.LOGIN_BUTTON)
        ).click()

        # Ожидаем либо смену URL, либо появление элемента на главной странице
        WebDriverWait(self.driver, 15).until(
            lambda driver: (
                    driver.current_url == "https://stellarburgers.nomoreparties.site/" or
                    "Неверный пароль" in driver.page_source  # Обработка ошибки авторизации
            )
        )

    def is_login_successful(self):
        """Проверка успешной авторизации"""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.url_to_be("https://stellarburgers.nomoreparties.site/")
            )
        except:
            return False

    def get_error_message(self):
        """Получение текста сообщения об ошибке"""
        try:
            error_locator = (By.XPATH, "//p[contains(@class, 'input__error')]")
            return WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(error_locator)
            ).text
        except:
            return None

    def login(self, email, password):
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()

    def is_login_form_displayed(self):
        return WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(LoginLocators.LOGIN_FORM)
        )
