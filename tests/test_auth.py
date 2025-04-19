import allure
from pages.login_page import LoginPage
from pages.restore_password_page import RestorePasswordPage


@allure.feature("Auth")
def test_password_recovery(driver):
    login_page = LoginPage(driver)
    login_page.open("https://stellarburgers.nomoreparties.site/login")
    login_page.go_to_restore_password()
    restore_page = RestorePasswordPage(driver)
    restore_page.enter_email("test@test.com")
    restore_page.click_restore()
    assert restore_page.is_password_field_active()
