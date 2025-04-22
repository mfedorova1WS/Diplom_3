import allure
from locators.base_locators import BaseLocators
from locators.main_page_locators import MainPageLocators
from pages.main_page import MainPage
from config.urls import Urls


@allure.feature("Main functionality")
class TestMainFunctionality:

    @allure.story("Navigation via 'Constructor' button")
    def test_constructor_button_navigation(self, driver):
        page = MainPage(driver)
        page.open(Urls.BASE_URL)
        page.click(BaseLocators.CONSTRUCTOR_BUTTON)
        assert page.is_visible(MainPageLocators.INGREDIENT_BLOCK)


    @allure.story("Order feed link")
    def test_order_feed_navigation(self, driver):
        page = MainPage(driver)
        page.open(Urls.BASE_URL)
        page.go_to_order_feed()
        assert page.is_order_feed_opened()


    @allure.story("Ingredient modal behavior")
    def test_ingredient_modal(self, driver):
        page = MainPage(driver)
        page.open(Urls.BASE_URL)
        page.click_ingredient()
        # Ожидаем, что модальное окно открылось
        assert page.is_modal_opened()
        page.close_modal()


    @allure.story("Ingredient counter increases after drag and drop")
    def test_ingredient_counter_increases(self, driver):
        page = MainPage(driver)
        page.open(Urls.BASE_URL)
        ingredient_name = "Флюоресцентная булка R2-D3"
        # Получаем начальное значение счётчика
        initial_count = page.get_ingredient_counter(ingredient_name)
        # Добавляем ингредиент в заказ
        page.add_ingredient_by_drag_and_drop(ingredient_name)
        # Получаем новое значение счётчика
        new_count = page.get_ingredient_counter(ingredient_name)

        assert new_count == initial_count + 2, f"Ожидалось, что счётчик увеличится на 2, но было {initial_count}, стало {new_count}"


    @allure.story("Logged user can create an order")
    def test_logged_user_can_order(self, create_test_user, driver):
        email, password, access_token = create_test_user
        main_page = MainPage(driver)
        main_page.open(Urls.BASE_URL)
        # Логин
        main_page.open_and_login(email, password)
        order_number = main_page.create_order("Флюоресцентная булка R2-D3")
        # Проверка, что номер заказа отображается корректно
        assert order_number is not None, "Номер заказа не найден"
