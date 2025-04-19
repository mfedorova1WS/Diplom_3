class BasePage:
    def __init__(self, driver):
        self.driver = driver

    def open(self, url):
        self.driver.get(url)

    def get_element(self, locator):
        return self.driver.find_element(*locator)

    def click(self, locator):
        self.get_element(locator).click()

    def enter_text(self, locator, text):
        self.get_element(locator).send_keys(text)

    def is_visible(self, locator):
        return self.get_element(locator).is_displayed()
