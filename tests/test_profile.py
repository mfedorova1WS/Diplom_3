import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage


@allure.feature("Profile navigation")
@allure.story("Authorized user can open profile page")
def test_user_can_navigate_to_profile(create_test_user, driver):
    # Получаем данные нового пользователя
    email, password, access_token = create_test_user
    main_page = MainPage(driver)
    main_page.open("https://stellarburgers.nomoreparties.site/")
    # Авторизация
    main_page.go_to_login_page()
    login_page = LoginPage(driver)
    login_page.login(email, password)
    # Переходим в личный кабинет
    main_page.click_profile_button()
    profile_page = ProfilePage(driver)
    # Проверяем, что открылась страница профиля
    assert profile_page.is_profile_page_opened(), "Страница профиля не открылась после перехода"


@allure.feature("Profile navigation")
@allure.story("Authorized user can view order history")
def test_user_can_view_order_history(create_test_user, driver):
    # Создаем пользователя
    email, password, access_token = create_test_user
    # Вход
    main_page = MainPage(driver)
    main_page.open_and_login(email, password)
    # Переход в профиль
    main_page.click_profile_button()
    profile_page = ProfilePage(driver)
    # Переход к истории заказов
    profile_page.go_to_history()
    # Проверка, что мы действительно в этом разделе
    expected_url = "https://stellarburgers.nomoreparties.site/account/order-history"
    current_url = driver.current_url
    assert current_url == expected_url, f"Ожидался переход на {expected_url}, но текущий URL: {current_url}"


@allure.feature("Logout")
@allure.story("User can log out from profile page")
def test_user_can_logout_from_profile(create_test_user, driver):
    # 1. Создаем пользователя
    email, password, _ = create_test_user
    # Вход
    main_page = MainPage(driver)
    login_page = LoginPage(driver)
    main_page.open_and_login(email, password)
    # Переход в Личный кабинет
    main_page.click_profile_button()
    profile_page = ProfilePage(driver)
    assert profile_page.is_profile_page_opened(), "Страница профиля не открылась"
    # Выход
    profile_page.logout()
    # Проверка отображение формы входа
    assert login_page.is_login_form_displayed(), "Форма логина не отображается после выхода"