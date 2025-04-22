import allure
from pages.main_page import MainPage
from pages.login_page import LoginPage
from pages.profile_page import ProfilePage
from config.urls import Urls


@allure.feature("Profile navigation")
class TestProfileNavigation:

    @allure.story("Authorized user can open profile page")
    def test_user_can_navigate_to_profile(self, create_test_user, driver):
        email, password, access_token = create_test_user
        main_page = MainPage(driver)
        main_page.open(Urls.BASE_URL)
        main_page.go_to_login_page()
        login_page = LoginPage(driver)
        login_page.login(email, password)
        main_page.click_profile_button()
        profile_page = ProfilePage(driver)
        assert profile_page.is_profile_page_opened(), "Страница профиля не открылась после перехода"


    @allure.story("Authorized user can view order history")
    def test_user_can_view_order_history(self, create_test_user, driver):
        email, password, access_token = create_test_user
        main_page = MainPage(driver)
        main_page.open_and_login(email, password)
        main_page.click_profile_button()
        profile_page = ProfilePage(driver)
        profile_page.go_to_history()
        expected_url = Urls.ORDER_HISTORY_URL
        current_url = driver.current_url
        assert current_url == expected_url, f"Ожидался переход на {expected_url}, но текущий URL: {current_url}"

    @allure.feature("Logout")
    @allure.story("User can log out from profile page")
    def test_user_can_logout_from_profile(self, create_test_user, driver):
        email, password, _ = create_test_user
        main_page = MainPage(driver)
        login_page = LoginPage(driver)
        main_page.open_and_login(email, password)
        main_page.click_profile_button()
        profile_page = ProfilePage(driver)
        assert profile_page.is_profile_page_opened(), "Страница профиля не открылась"
        profile_page.logout()
        assert login_page.is_login_form_displayed(), "Форма логина не отображается после выхода"