import allure
from pages.login_page import LoginPage
from pages.main_page import MainPage
from pages.order_page import OrderPage
from pages.profile_page import ProfilePage
from config.urls import Urls


@allure.feature("Order Feed")
class TestOrderFeed:

    @allure.story("Order modal opens from feed and shows correct order details")
    def test_order_modal_opens_from_feed(self, create_test_user, driver):
        email, password, access_token = create_test_user

        # Инициализация страниц
        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        # Авторизация и создание заказа
        main_page.open_and_login(email, password)
        order_number = main_page.create_order("Флюоресцентная булка R2-D3")
        main_page.close_modal()

        # Переход в ленту заказов
        main_page.go_to_order_feed()
        main_page.wait_for_order_feed_to_load()

        # Открытие модалки заказа из ленты
        modal_order_number = order_page.open_order_modal_by_number(order_number)

        assert modal_order_number == order_number, (
            f"Ожидался номер {order_number}, но в модалке {modal_order_number}"
        )


    @allure.story("Total completed orders counter increases after new order")
    def test_total_orders_counter_increases(self, create_test_user, driver):
        email, password, access_token = create_test_user

        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        # Логин и переход в ленту заказов
        main_page.open_and_login(email, password)
        main_page.go_to_order_feed()
        main_page.wait_for_order_feed_to_load()

        # Получаем значение счетчика до создания заказа
        total_before = order_page.get_total_orders_count()
        assert total_before.isdigit(), "Счетчик до заказа не является числом"

        # Переход на главную и оформление заказа
        main_page.open(Urls.BASE_URL)
        main_page.create_order("Флюоресцентная булка R2-D3")
        main_page.close_modal()

        # Переход обратно в ленту заказов и получаем новое значение счетчика
        main_page.go_to_order_feed()
        main_page.wait_for_order_feed_to_load()
        total_after = order_page.get_total_orders_count()

        # Проверка, что счетчик увеличился
        assert int(total_after) > int(total_before), (
            f"Счетчик не увеличился: было {total_before}, стало {total_after}"
        )


    @allure.story("Today's completed orders counter increases after new order")
    def test_today_orders_counter_increases(self, create_test_user, driver):
        email, password, access_token = create_test_user

        main_page = MainPage(driver)
        order_page = OrderPage(driver)

        # Логин и переход в ленту заказов
        main_page.open_and_login(email, password)
        main_page.go_to_order_feed()
        main_page.wait_for_order_feed_to_load()

        # Получаем значение счетчика "за сегодня" до заказа
        today_before = order_page.get_today_orders_count()
        assert today_before.isdigit(), "Счетчик 'за сегодня' до заказа не является числом"

        # Переход на главную и оформление заказа
        main_page.open(Urls.BASE_URL)
        main_page.create_order("Флюоресцентная булка R2-D3")
        main_page.close_modal()

        # Возвращаемся в ленту заказов
        main_page.go_to_order_feed()
        main_page.wait_for_order_feed_to_load()
        today_after = order_page.get_today_orders_count()

        # Проверка, что значение увеличилось
        assert int(today_after) > int(today_before), (
            f"Счетчик 'за сегодня' не увеличился: было {today_before}, стало {today_after}"
        )


    @allure.story("Order number appears in 'In Progress' section after placing an order")
    def test_order_appears_in_progress(self, create_test_user, driver):
        email, password, access_token = create_test_user

        # Страницы
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        login_page = LoginPage(driver)

        # Логин
        main_page.open(Urls.BASE_URL)
        main_page.go_to_login_page()
        login_page.login(email, password)

        # Создание заказа
        ingredient_name = "Флюоресцентная булка R2-D3"
        order_number = main_page.create_order(ingredient_name)
        main_page.close_modal()

        # Переход в ленту заказов
        main_page.go_to_order_feed()
        assert main_page.is_order_feed_opened()

        # Проверка, что номер заказа отображается в разделе "В работе"
        in_progress_orders = order_page.get_in_progress_order_numbers()
        assert order_number in in_progress_orders, f"Номер заказа {order_number} не найден в разделе 'В работе'"


    @allure.story("User orders appear in feed and order history")
    def test_user_order_appears_in_feed_and_history(self, create_test_user, driver):
        email, password, access_token = create_test_user

        # Инициализация страниц
        main_page = MainPage(driver)
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)

        # Логин и оформление заказа
        main_page.open_and_login(email, password)
        order_number = main_page.create_order("Флюоресцентная булка R2-D3")
        main_page.close_modal()

        # Проверка, что заказ виден в ленте заказов
        main_page.go_to_order_feed()
        main_page.wait_for_order_feed_to_load()
        modal_order_number = order_page.open_order_modal_by_number(order_number)
        assert modal_order_number == order_number, (
            f"Ожидался номер {order_number} в ленте заказов, но в модалке {modal_order_number}"
        )

        # Проверка, что заказ есть в истории заказов
        main_page.click_profile_button()
        profile_page.go_to_history()

        # Убеждаемся, что в истории есть номер этого заказа
        history_order_numbers = profile_page.get_order_history_numbers()
        assert order_number in history_order_numbers, (
            f"Ожидался номер {order_number} в истории заказов, но он не найден. Найдено: {history_order_numbers}"
        )

