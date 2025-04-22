import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @allure.step("Открытие страницы по URL: {url}")
    def open(self, url):
        self.driver.get(url)

    @allure.step("Получение элемента по локатору: {locator}")
    def get_element(self, locator):
        return self.driver.find_element(*locator)

    @allure.step("Клик по элементу с локатором: {locator}")
    def click(self, locator):
        self.get_element(locator).click()

    @allure.step("Ввод текста: '{text}' в элемент с локатором: {locator}")
    def enter_text(self, locator, text):
        self.get_element(locator).send_keys(text)

    @allure.step("Проверка отображения элемента с локатором: {locator}")
    def is_visible(self, locator):
        return self.get_element(locator).is_displayed()
