from selenium.webdriver.common.by import By


class RestorePasswordLocators:
    EMAIL_INPUT = (By.NAME, "name")
    RESTORE_BUTTON = (By.CSS_SELECTOR, "button.button_button_type_primary__1O7Bx")
    PASSWORD_FIELD = (By.NAME, "Введите новый пароль")
