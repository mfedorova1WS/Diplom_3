from selenium.webdriver.common.by import By


class BaseLocators:
    LOGO = (By.CLASS_NAME, "AppHeader_header__logo__2D0X2")
    CONSTRUCTOR_BUTTON = (By.XPATH, "//p[text()='Конструктор']")
    ORDER_FEED_BUTTON = (By.XPATH, '//p[@class="AppHeader_header__linkText__3q_va ml-2" and text()="Лента Заказов"]')
    PROFILE_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
