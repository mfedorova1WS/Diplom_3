from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from locators.base_locators import BaseLocators
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):
    def open_and_login(self, email, password):
        self.open("https://stellarburgers.nomoreparties.site/")
        self.go_to_login_page()
        from pages.login_page import LoginPage
        login_page = LoginPage(self.driver)
        login_page.login(email, password)

    def click_ingredient(self):
        self.click(MainPageLocators.INGREDIENT_ITEM)

    def go_to_order_feed(self):
        button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(BaseLocators.ORDER_FEED_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def is_modal_opened(self):
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_TITLE)
        )
        return self.is_visible(MainPageLocators.MODAL_TITLE)

    def close_modal(self):
        close_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.MODAL_CLOSE_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", close_button)


    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    def add_ingredient_by_name(self, name):
        locator = (By.XPATH, f"//p[text()='{name}']/ancestor::li")
        self.click(locator)

    def get_ingredient_counter(self, name):
        try:
            ingredient_locator = (
            By.XPATH, f"//p[text()='{name}']/ancestor::a[contains(@class, 'BurgerIngredient_ingredient__')]")

            ingredient = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(ingredient_locator)
            )

            counter = ingredient.find_element(By.CSS_SELECTOR, "p[class*='counter_counter__num']")
            return int(counter.text)
        except Exception as e:
            print(f"Не удалось найти счетчик: {str(e)}")
            return 0

    def add_ingredient_by_drag_and_drop(self, ingredient_name):
        ingredient_locator = (
            By.XPATH,
            f"//p[text()='{ingredient_name}']/ancestor::a[contains(@class, 'BurgerIngredient_ingredient__')]"
        )

        ingredient = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(ingredient_locator)
        )

        constructor = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.CONSTRUCTOR_AREA)
        )

        # drag-and-drop
        ActionChains(self.driver) \
            .move_to_element(ingredient) \
            .pause(1) \
            .click_and_hold() \
            .pause(1) \
            .move_to_element(constructor) \
            .pause(1) \
            .release() \
            .pause(1) \
            .perform()

        # Дополнительная проверка через JS
        self.driver.execute_script("""
        arguments[0].dispatchEvent(new Event('drop', { bubbles: true }));
        """, constructor)


    def is_order_modal_displayed(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.ORDER_SUCCESS)
            ).is_displayed()
        except:
            return False

    def get_order_number(self):
        # Ждём появления модалки
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4"))
        )

        # Ждём, пока исчезнет индикатор загрузки (модалка станет активной)
        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(
                (By.CSS_SELECTOR, "div.Modal_modal__P3_V5 img.Modal_modal__loading__3534A"))
        )

        # Получаем и возвращаем финальный номер
        order_number = self.driver.find_element(By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4 h2").text.strip()
        return order_number

    def go_to_login_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
        ).click()

    def click_profile_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.PROFILE_BUTTON)
        )
        profile_button = self.driver.find_element(*MainPageLocators.PROFILE_BUTTON)
        self.driver.execute_script("arguments[0].click();", profile_button)

    def create_order(self, ingredient_name: str):
        """
        Метод для добавления ингредиента в заказ и ожидания появления модального окна с номером заказа.
        """
        self.add_ingredient_by_drag_and_drop(ingredient_name)
        self.click_order_button()
        # Ожидаем появления модального окна с номером заказа
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class, 'modal') and .//p[contains(text(), 'Ваш заказ')]]"))
        )
        # Получаем номер заказа из модального окна
        order_number = self.get_order_number()
        return order_number

    def wait_for_order_feed_to_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//ul[contains(@class, 'OrderFeed_list__OLh59')]"))
        )