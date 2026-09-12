from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class MainPage(BasePage):
    FROM_INPUT = (By.ID, "from")
    TO_INPUT = (By.ID, "to")

    def fill_addresses(self, address_from: str, address_to: str) -> None:
        from_input = self.wait_visible(self.FROM_INPUT)
        from_input.clear()
        from_input.send_keys(address_from)

        to_input = self.wait_visible(self.TO_INPUT)
        to_input.clear()
        to_input.send_keys(address_to)
        to_input.send_keys(Keys.ENTER)

    def wait_route_ready(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: "Такси ~" in self.body_text() and "В пути" in self.body_text()
        )

    def wait_map_points(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: len(driver.find_elements(By.CSS_SELECTOR, "div[class*='placemark-overlay']")) >= 2
        )

    def map_points_count(self) -> int:
        return len(self.driver.find_elements(By.CSS_SELECTOR, "div[class*='placemark-overlay']"))

    def from_value(self) -> str:
        return self.find(self.FROM_INPUT).get_attribute("value")

    def to_value(self) -> str:
        return self.find(self.TO_INPUT).get_attribute("value")
