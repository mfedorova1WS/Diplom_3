from selenium.webdriver.common.by import By

class OrderLocators:
    BUN_ITEM = (By.XPATH, "//section//p[text()='Флюоресцентная булка R2-D3']")
    CONSTRUCTOR_DROP_ZONE = (By.XPATH, "//section[contains(@class, 'BurgerConstructor_basket')]")
    PLACE_ORDER_BUTTON = (By.XPATH, "//button[contains(text(), 'Оформить заказ')]")
    ORDER_MODAL = (By.CLASS_NAME, "Modal_modal__container__Wo2l_")  # общий контейнер модалки
    ORDER_NUMBER_IN_MODAL = (By.XPATH, "//div[contains(@class, 'Modal_modal__container')]/div/p[contains(@class,'text_type_digits-large')]")
    MODAL_CLOSE_BUTTON = (By.CLASS_NAME, "Modal_modal__close_modified__3V9Zu")
    FEED_ORDER_NUMBERS = (By.XPATH, "//ul[contains(@class, 'OrderFeed_order_list')]/li//p[contains(@class, 'text_type_digits-default')]")
    FEED_ORDER_TITLES = (By.XPATH, "//ul[contains(@class, 'OrderFeed_order_list')]/li")
    FEED_ORDER_CARD = lambda order_number: (By.XPATH, f"//li[.//p[text()='{order_number}']]")
    MODAL_ORDER_NUMBER = (By.XPATH, "//p[@class='text text_type_digits-default mb-10 mt-5']")
    TOTAL_ORDERS_COUNT = (By.XPATH,"//p[text()='Выполнено за все время:']/following-sibling::p[contains(@class, 'OrderFeed_number__')]")
    TODAY_ORDERS_COUNT = (By.XPATH,"//p[text()='Выполнено за сегодня:']/following-sibling::p[contains(@class, 'OrderFeed_number__')]")
    IN_PROGRESS_ORDER_NUMBERS = (By.CSS_SELECTOR,"ul.OrderFeed_orderListReady__1YFem li.text_type_digits-default")