from __future__ import annotations

import re

import allure
from selenium.webdriver.support.ui import WebDriverWait

from locators.route_page_locators import RoutePageLocators
from pages.main_page import MainPage


class RoutePage(MainPage):
    @staticmethod
    def _mode_locator(mode_name: str) -> tuple[str, str]:
        return (
            "xpath",
            RoutePageLocators.MODE_XPATH_TEMPLATE.format(mode_name=mode_name),
        )

    @allure.step("Получить текст блока маршрута")
    def route_text(self) -> str:
        return self.body_text()

    @allure.step("Проверить наличие сводки маршрута")
    def has_route_summary(self) -> bool:
        text = self.route_text()
        return "Такси ~" in text and "В пути" in text

    @allure.step("Выбрать вид маршрута: {mode_name}")
    def select_mode(self, mode_name: str) -> None:
        self.find(self._mode_locator(mode_name)).click()

    @allure.step("Проверить активность вида маршрута: {mode_name}")
    def mode_is_active(self, mode_name: str) -> bool:
        element = self.find(self._mode_locator(mode_name))
        return "active" in element.get_attribute("class")

    @allure.step("Получить стоимость и время маршрута")
    def current_price_and_time(self) -> tuple[str, str]:
        text = self.route_text()
        price_match = re.search(r"(Такси|Драйв|Авто)\s*~?\s*\d+\s*руб\.|Авто\s+Бесплатно", text)
        time_match = re.search(r"В пути\s*\d+\s*мин\.|В пути 0 мин\.", text)
        return (price_match.group(0) if price_match else "", time_match.group(0) if time_match else "")

    @allure.step("Получить количество доступных типов передвижения")
    def custom_types_count(self) -> int:
        return len(self.driver.find_elements(*RoutePageLocators.CUSTOM_TYPES))

    @allure.step("Выбрать тип передвижения Драйв")
    def select_drive_type(self) -> None:
        self.find(RoutePageLocators.DRIVE_TYPE).click()

    @allure.step("Проверить активность типа Драйв")
    def drive_type_is_active(self) -> bool:
        return "active" in self.find(RoutePageLocators.DRIVE_TYPE).get_attribute("class")

    @allure.step("Проверить видимость кнопки Вызвать такси")
    def call_taxi_button_visible(self) -> bool:
        return "Вызвать такси" in self.route_text()

    @allure.step("Проверить видимость кнопки Забронировать")
    def book_button_visible(self) -> bool:
        return "Забронировать" in self.route_text()

    @allure.step("Дождаться блока выбора маршрута")
    def wait_route_selection_block(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: "Оптимальный" in self.route_text() and "Быстрый" in self.route_text() and "Свой" in self.route_text()
        )

