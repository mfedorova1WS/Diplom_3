import allure
from locators.base_locators import BaseLocators
from locators.main_page_locators import MainPageLocators
from pages.main_page import MainPage


@allure.feature("Main functionality")
def test_constructor_button_navigation(driver):
    page = MainPage(driver)
    page.open("https://stellarburgers.nomoreparties.site")
    page.click(BaseLocators.CONSTRUCTOR_BUTTON)
    assert page.is_visible(MainPageLocators.INGREDIENT_BLOCK)


@allure.feature("Main functionality")
def test_order_feed_navigation(driver):
    page = MainPage(driver)
    page.open("https://stellarburgers.nomoreparties.site/")
    page.go_to_order_feed()
    assert "feed" in driver.current_url or "order" in driver.current_url


@allure.feature("Main functionality")
def test_ingredient_modal(driver):
    page = MainPage(driver)
    page.open("https://stellarburgers.nomoreparties.site/")
    page.click_ingredient()
    # Ожидаем, что модальное окно открылось
    assert page.is_modal_opened()
    page.close_modal()


@allure.feature("Main functionality")
def test_ingredient_counter_increases(driver):
    page = MainPage(driver)
    page.open("https://stellarburgers.nomoreparties.site/")
    ingredient_name = "Флюоресцентная булка R2-D3"
    # Получаем начальное значение счётчика
    initial_count = page.get_ingredient_counter(ingredient_name)
    # Добавляем ингредиент в заказ
    page.add_ingredient_by_drag_and_drop(ingredient_name)
    # Получаем новое значение счётчика
    new_count = page.get_ingredient_counter(ingredient_name)

    assert new_count == initial_count + 2, f"Ожидалось, что счётчик увеличится на 2, но было {initial_count}, стало {new_count}"


def test_logged_user_can_order(create_test_user, driver):
    email, password, access_token = create_test_user
    main_page = MainPage(driver)
    main_page.open("https://stellarburgers.nomoreparties.site/")
    # Логин
    main_page.open_and_login(email, password)
    order_number = main_page.create_order("Флюоресцентная булка R2-D3")
    # Проверка, что номер заказа отображается корректно
    assert order_number is not None, "Номер заказа не найден"
