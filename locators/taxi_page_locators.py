from selenium.webdriver.common.by import By


class TaxiPageLocators:
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(@class,'button round') and contains(., 'Вызвать такси')]")
    PHONE_INPUT = (By.ID, "phone")
    SUBMIT_ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Ввести номер и заказать')]")
    DETAILS_BUTTON = (By.XPATH, "//button[contains(., 'Детали')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Отменить')]")
    TARIFF_CARDS = (By.CSS_SELECTOR, "div.tcard")
    TARIFF_TITLES = (By.CSS_SELECTOR, "div.tcard-title")
    TARIFF_BUTTON = (By.CSS_SELECTOR, "button.tcard-i")
    TARIFF_DESCRIPTION = (By.CSS_SELECTOR, "div.i-dPrefix")
    TARIFF_CARD_XPATH_TEMPLATE = "//div[contains(@class,'tcard')][.//div[contains(@class,'tcard-title') and normalize-space()='{tariff_title}']]"
    LAPTOP_CHECKBOX = (By.XPATH, "//*[contains(text(), 'Столик для ноутбука')]")
