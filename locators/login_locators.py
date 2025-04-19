from selenium.webdriver.common.by import By


class LoginLocators:
    EMAIL_INPUT = (By.NAME, "name")
    PASSWORD_INPUT = (By.NAME, "Пароль")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти']")
    RESTORE_PASSWORD_BUTTON = (By.LINK_TEXT, "Восстановить пароль")
    LOGIN_FORM = (By.CLASS_NAME, "Auth_form__3qKeq")