from selenium.webdriver.common.by import By


class MainPageLocators:
    INGREDIENT_BLOCK = (By.CLASS_NAME, "BurgerIngredients_ingredients__menuContainer__Xu3Mo")
    INGREDIENT_COUNTER = (By.CSS_SELECTOR, "[class*='counter_counter__num']")
    INGREDIENT_ITEM = (By.XPATH, ".//div[contains(@class, 'BurgerIngredient_ingredient')]")
    ORDER_BUTTON = (By.XPATH, "//button[text()='Оформить заказ']")
    MODAL_CLOSE_BUTTON = (By.XPATH, "//button[contains(@class, 'Modal_modal__close')]")
    MODAL_TITLE = (By.CSS_SELECTOR, ".Modal_modal__contentBox__sCy8X.pt-10.pb-15")
    CONSTRUCTOR_AREA = (By.CLASS_NAME, "BurgerConstructor_basket__29Cd7")
    ORDER_NUMBER = (By.XPATH, "//nav//p[text()='Личный Кабинет']")
    ORDER_SUCCESS = (By.XPATH, "//*[contains(text(), 'идентификатор заказа')]")
    LOGIN_BUTTON = (By.XPATH, "//button[text()='Войти в аккаунт']")
    PROFILE_BUTTON = (By.XPATH, "//p[text()='Личный Кабинет']")
    MODAL_ORDER_SECTION = (By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4")
    MODAL_LOADING_INDICATOR = (By.CSS_SELECTOR, "div.Modal_modal__P3_V5 img.Modal_modal__loading__3534A")
    ORDER_NUMBER_IN_MODAL = (By.CSS_SELECTOR, "section.Modal_modal_opened__3ISw4 h2")
    ORDER_MODAL_TITLE_TEXT = (By.XPATH, "//div[contains(@class, 'modal') and .//p[contains(text(), 'Ваш заказ')]]")
    ORDER_FEED_LIST = (By.XPATH, "//ul[contains(@class, 'OrderFeed_list__OLh59')]")