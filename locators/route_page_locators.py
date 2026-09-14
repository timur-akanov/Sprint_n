from selenium.webdriver.common.by import By


class RoutePageLocators:
    MODE_XPATH_TEMPLATE = "//div[contains(@class,'mode') and normalize-space()='{mode_name}']"
    CUSTOM_TYPES = (By.CSS_SELECTOR, "div.type")
    DRIVE_TYPE = (By.CSS_SELECTOR, "div.type.drive")
