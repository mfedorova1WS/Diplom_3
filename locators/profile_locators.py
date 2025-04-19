from selenium.webdriver.common.by import By


class ProfileLocators:
    HISTORY_TAB = (By.XPATH, "//a[text()='История заказов']")
    LOGOUT_BUTTON = (By.XPATH, "//button[text()='Выход']")
    ORDER_HISTORY_NUMBERS = (By.CSS_SELECTOR, "ul.OrderHistory_profileList__374GU p.text_type_digits-default")
