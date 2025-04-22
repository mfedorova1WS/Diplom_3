import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from locators.base_locators import BaseLocators
from pages.base_page import BasePage
from locators.main_page_locators import MainPageLocators


class MainPage(BasePage):

    @allure.step("Открытие сайта и авторизация пользователя")
    def open_and_login(self, email, password):
        self.open("https://stellarburgers.nomoreparties.site/")
        self.go_to_login_page()
        from pages.login_page import LoginPage
        login_page = LoginPage(self.driver)
        login_page.login(email, password)

    @allure.step("Клик по ингредиенту")
    def click_ingredient(self):
        self.click(MainPageLocators.INGREDIENT_ITEM)

    @allure.step("Переход в ленту заказов")
    def go_to_order_feed(self):
        button = WebDriverWait(self.driver, 5).until(
            EC.presence_of_element_located(BaseLocators.ORDER_FEED_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    @allure.step("Проверка, что модальное окно открыто")
    def is_modal_opened(self):
        WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_TITLE)
        )
        return self.is_visible(MainPageLocators.MODAL_TITLE)

    @allure.step("Закрытие модального окна")
    def close_modal(self):
        close_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.MODAL_CLOSE_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", close_button)

    @allure.step("Клик по кнопке 'Оформить заказ'")
    def click_order_button(self):
        self.click(MainPageLocators.ORDER_BUTTON)

    @allure.step("Добавление ингредиента по имени: {name}")
    def add_ingredient_by_name(self, name):
        locator = (By.XPATH, f"//p[text()='{name}']/ancestor::li")
        self.click(locator)

    @allure.step("Получение значения счётчика для ингредиента: {name}")
    def get_ingredient_counter(self, name):
        try:
            ingredient_locator = (
                By.XPATH, f"//p[text()='{name}']/ancestor::a[contains(@class, 'BurgerIngredient_ingredient__')]")

            ingredient = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(ingredient_locator)
            )

            counter = ingredient.find_element(*MainPageLocators.INGREDIENT_COUNTER)
            return int(counter.text)
        except Exception as e:
            print(f"Не удалось найти счетчик: {str(e)}")
            return 0

    @allure.step("Добавление ингредиента перетаскиванием: {ingredient_name}")
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

        self.driver.execute_script(""" 
        arguments[0].dispatchEvent(new Event('drop', { bubbles: true }));
        """, constructor)

    @allure.step("Проверка, что модалка с заказом отображается")
    def is_order_modal_displayed(self):
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located(MainPageLocators.ORDER_SUCCESS)
            ).is_displayed()
        except:
            return False

    @allure.step("Получение номера заказа из модального окна")
    def get_order_number(self):
        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.MODAL_ORDER_SECTION)
        )

        WebDriverWait(self.driver, 15).until(
            EC.invisibility_of_element_located(MainPageLocators.MODAL_LOADING_INDICATOR)
        )

        order_number = self.driver.find_element(*MainPageLocators.ORDER_NUMBER_IN_MODAL).text.strip()
        return order_number

    @allure.step("Переход на страницу логина")
    def go_to_login_page(self):
        WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable(MainPageLocators.LOGIN_BUTTON)
        ).click()

    @allure.step("Клик по кнопке профиля")
    def click_profile_button(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.PROFILE_BUTTON)
        )
        profile_button = self.driver.find_element(*MainPageLocators.PROFILE_BUTTON)
        self.driver.execute_script("arguments[0].click();", profile_button)

    @allure.step("Создание заказа с ингредиентом: {ingredient_name}")
    def create_order(self, ingredient_name: str):
        self.add_ingredient_by_drag_and_drop(ingredient_name)
        self.click_order_button()

        WebDriverWait(self.driver, 15).until(
            EC.visibility_of_element_located(MainPageLocators.ORDER_MODAL_TITLE_TEXT)
        )

        order_number = self.get_order_number()
        return order_number

    @allure.step("Ожидание загрузки ленты заказов")
    def wait_for_order_feed_to_load(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(MainPageLocators.ORDER_FEED_LIST)
        )
    @allure.step("Проверка, что открыта страница ленты заказов")
    def is_order_feed_opened(self):
        current_url = self.driver.current_url
        return "feed" in current_url or "order" in current_url