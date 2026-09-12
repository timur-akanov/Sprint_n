from __future__ import annotations

import re

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.main_page import MainPage


class RoutePage(MainPage):
    def route_text(self) -> str:
        return self.body_text()

    def has_route_summary(self) -> bool:
        text = self.route_text()
        return "Такси ~" in text and "В пути" in text

    def select_mode(self, mode_name: str) -> None:
        self.find((By.XPATH, f"//div[contains(@class,'mode') and normalize-space()='{mode_name}']")).click()

    def mode_is_active(self, mode_name: str) -> bool:
        element = self.find((By.XPATH, f"//div[contains(@class,'mode') and normalize-space()='{mode_name}']"))
        return "active" in element.get_attribute("class")

    def current_price_and_time(self) -> tuple[str, str]:
        text = self.route_text()
        price_match = re.search(r"(Такси|Драйв|Авто)\s*~?\s*\d+\s*руб\.|Авто\s+Бесплатно", text)
        time_match = re.search(r"В пути\s*\d+\s*мин\.|В пути 0 мин\.", text)
        return (price_match.group(0) if price_match else "", time_match.group(0) if time_match else "")

    def custom_types_count(self) -> int:
        return len(self.driver.find_elements(By.CSS_SELECTOR, "div.type"))

    def select_drive_type(self) -> None:
        self.find((By.CSS_SELECTOR, "div.type.drive")).click()

    def drive_type_is_active(self) -> bool:
        return "active" in self.find((By.CSS_SELECTOR, "div.type.drive")).get_attribute("class")

    def call_taxi_button_visible(self) -> bool:
        return "Вызвать такси" in self.route_text()

    def book_button_visible(self) -> bool:
        return "Забронировать" in self.route_text()

    def wait_route_selection_block(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: "Оптимальный" in self.route_text() and "Быстрый" in self.route_text() and "Свой" in self.route_text()
        )

