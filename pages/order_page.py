from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from locators.order_locators import OrderLocators
from pages.base_page import BasePage
import time

class OrderPage(BasePage):
    def drag_bun_to_constructor(self):
        bun = self.driver.find_element(*OrderLocators.BUN_ITEM)
        target = self.driver.find_element(*OrderLocators.CONSTRUCTOR_DROP_ZONE)
        ActionChains(self.driver).drag_and_drop(bun, target).perform()

    def place_order(self):
        self.click(OrderLocators.PLACE_ORDER_BUTTON)

    def wait_for_order_modal_and_get_number(self):
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(OrderLocators.ORDER_MODAL)
        )
        order_number_elem = self.driver.find_element(OrderLocators.ORDER_NUMBER_IN_MODAL)
        return order_number_elem.text.strip()

    def close_order_modal(self):
        self.click(OrderLocators.MODAL_CLOSE_BUTTON)

    def scroll_to_order(self, order_number, max_scrolls=10):
        target_xpath = f"//p[contains(text(), '#0{order_number}')]"

        for _ in range(max_scrolls):
            try:
                element = self.driver.find_element(By.XPATH, target_xpath)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                return element
            except NoSuchElementException:
                self.driver.execute_script("window.scrollBy(0, window.innerHeight);")
                time.sleep(1)
        raise Exception(f"Не удалось найти заказ #{order_number} после {max_scrolls} прокруток")

    def open_order_modal_by_number(self, order_number, max_scrolls=10):
        order_card = self.scroll_to_order(order_number)
        order_card.click()

        # Ожидаем появления модалки и получаем номер заказа
        modal_order_number_element = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(OrderLocators.MODAL_ORDER_NUMBER)
        )
        return modal_order_number_element.text.strip().lstrip('#0')

    def get_total_orders_count(self):
        total_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(OrderLocators.TOTAL_ORDERS_COUNT)
        )
        return total_elem.text.strip()

    def get_today_orders_count(self):
        today_elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(OrderLocators.TODAY_ORDERS_COUNT)
        )
        return today_elem.text.strip()

    def get_in_progress_order_numbers(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(OrderLocators.IN_PROGRESS_ORDER_NUMBERS)
        )
        elements = self.driver.find_elements(*OrderLocators.IN_PROGRESS_ORDER_NUMBERS)
        # Удаляем ноль впереди и возвращаем список номеров заказов в виде строк
        return [elem.text.lstrip('0') for elem in elements]

