from selenium.webdriver.common.by import By


class MainPageLocators:
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")
    MAP_POINTS = (By.CSS_SELECTOR, "div[class*='placemark-overlay']")
