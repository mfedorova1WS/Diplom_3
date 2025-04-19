import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from pages.login_page import LoginPage
import random
import string
from utils.api_helper import create_user, delete_user
from selenium.webdriver.support import expected_conditions as EC


# Параметр для указания браузера через командную строку
def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Browser to run tests on. Options: chrome, firefox")
    parser.addoption("--email", action="store", default="your_email@example.com")
    parser.addoption("--password", action="store", default="your_password")


# Фикстура для выбора браузера
@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")

    if browser == "chrome":
        options = Options()
        options.add_argument("--start-maximized")  # Максимизировать окно браузера
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield driver
    driver.quit()


# Фикстура для логина
@pytest.fixture
def login(request, driver):
    def _login(email=None, password=None):
        email = email or request.config.getoption("--email")
        password = password or request.config.getoption("--password")

        login_page = LoginPage(driver)
        login_page.open("https://stellarburgers.nomoreparties.site/login")
        login_page.enter_email(email)
        login_page.enter_password(password)
        login_page.click_login()

        # Ожидаем перехода на главную страницу после авторизации
        WebDriverWait(driver, 10).until(
            EC.url_to_be("https://stellarburgers.nomoreparties.site/")
        )

    return _login


# Фикстура для авторизованного пользователя
@pytest.fixture
def authorized_user(driver, login):
    """Фикстура для предварительно авторизованного пользователя"""
    login()
    yield driver


# Генерация случайной почты для теста
def random_email():
    return "test_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)) + "@yandex.ru"


# Фикстура для создания тестового пользователя
@pytest.fixture
def create_test_user():
    email = random_email()
    password = "strongpassword123"
    name = "autotest_user"

    # Создаем пользователя через API
    response = create_user(email, password, name)
    access_token = response.get("accessToken")

    yield email, password, access_token

    # Удаляем пользователя после теста
    if access_token:
        delete_user(access_token)
