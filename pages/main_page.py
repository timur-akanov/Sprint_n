from __future__ import annotations

import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait

from locators.main_page_locators import MainPageLocators
from pages.base_page import BasePage


class MainPage(BasePage):
    @allure.step("Заполнить поля Откуда и Куда")
    def fill_addresses(self, address_from: str, address_to: str) -> None:
        from_input = self.wait_visible(MainPageLocators.FROM_INPUT)
        from_input.clear()
        from_input.send_keys(address_from)

        to_input = self.wait_visible(MainPageLocators.TO_INPUT)
        to_input.clear()
        to_input.send_keys(address_to)
        to_input.send_keys(Keys.ENTER)

    @allure.step("Дождаться готовности маршрута")
    def wait_route_ready(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: "Такси ~" in self.body_text() and "В пути" in self.body_text()
        )

    @allure.step("Дождаться отображения точек маршрута на карте")
    def wait_map_points(self, timeout: int = 15) -> None:
        WebDriverWait(self.driver, timeout).until(
            lambda driver: len(driver.find_elements(*MainPageLocators.MAP_POINTS)) >= 2
        )

    @allure.step("Получить количество точек маршрута на карте")
    def map_points_count(self) -> int:
        return len(self.driver.find_elements(*MainPageLocators.MAP_POINTS))

    @allure.step("Получить значение поля Откуда")
    def from_value(self) -> str:
        return self.find(MainPageLocators.FROM_INPUT).get_attribute("value") or ""

    @allure.step("Получить значение поля Куда")
    def to_value(self) -> str:
        return self.find(MainPageLocators.TO_INPUT).get_attribute("value") or ""
