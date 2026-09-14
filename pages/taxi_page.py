from __future__ import annotations

import allure
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait

from locators.taxi_page_locators import TaxiPageLocators
from pages.route_page import RoutePage


class TaxiPage(RoutePage):
    @staticmethod
    def _tariff_card_locator(tariff_title: str) -> tuple[str, str]:
        return (
            "xpath",
            TaxiPageLocators.TARIFF_CARD_XPATH_TEMPLATE.format(tariff_title=tariff_title),
        )

    @allure.step("Выбрать тариф: {tariff_title}")
    def select_tariff(self, tariff_title: str) -> None:
        card = self.find(self._tariff_card_locator(tariff_title))
        button = card.find_element(*TaxiPageLocators.TARIFF_BUTTON)
        ActionChains(self.driver).move_to_element(card).perform()
        self.driver.execute_script("arguments[0].click();", button)

    @allure.step("Получить количество тарифов")
    def tariffs_count(self) -> int:
        return len(self.driver.find_elements(*TaxiPageLocators.TARIFF_CARDS))

    @allure.step("Получить количество активных тарифов")
    def active_tariffs_count(self) -> int:
        cards = self.driver.find_elements(*TaxiPageLocators.TARIFF_CARDS)
        return len([card for card in cards if "active" in card.get_attribute("class")])

    @allure.step("Получить названия тарифов")
    def tariff_titles(self) -> list[str]:
        return [el.text.strip() for el in self.driver.find_elements(*TaxiPageLocators.TARIFF_TITLES) if el.text.strip()]

    @allure.step("Навести курсор на иконку i тарифа: {tariff_title}")
    def hover_tariff_info(self, tariff_title: str) -> None:
        card = self.find(self._tariff_card_locator(tariff_title))
        i_button = card.find_element(*TaxiPageLocators.TARIFF_BUTTON)
        ActionChains(self.driver).move_to_element(card).move_to_element(i_button).perform()

    @allure.step("Получить описание тарифа: {tariff_title}")
    def tariff_description(self, tariff_title: str) -> str:
        card = self.find(self._tariff_card_locator(tariff_title))
        description = card.find_element(*TaxiPageLocators.TARIFF_DESCRIPTION)
        return description.text.strip()

    @allure.step("Заполнить поле телефона")
    def fill_phone(self, phone_number: str) -> None:
        phone = self.find(TaxiPageLocators.PHONE_INPUT)
        self.set_input_value(phone, phone_number)

    @allure.step("Попробовать заполнить телефон обычным вводом")
    def try_fill_phone_by_typing(self, phone_number: str) -> str:
        phone = self.find(TaxiPageLocators.PHONE_INPUT)
        phone.click()
        phone.send_keys(phone_number)
        return phone.get_attribute("value") or ""

    @allure.step("Нажать кнопку Вызвать такси")
    def call_taxi(self) -> None:
        button = self.wait_clickable(TaxiPageLocators.CALL_TAXI_BUTTON)
        ActionChains(self.driver).move_to_element(button).click(button).perform()

    @allure.step("Проверить видимость обязательных полей заказа")
    def order_fields_visible(self) -> bool:
        text = self.body_text()
        return all(
            part in text
            for part in ["Телефон", "Способ оплаты", "Комментарий водителю", "Требования к заказу"]
        )

    @allure.step("Нажать кнопку Ввести номер и заказать")
    def submit_order(self) -> None:
        self.wait_clickable(TaxiPageLocators.SUBMIT_ORDER_BUTTON).click()

    @allure.step("Дождаться окна Поиск машины")
    def wait_search_window(self, timeout: int = 20) -> None:
        WebDriverWait(self.driver, timeout).until(lambda driver: "Поиск машины" in self.body_text())

    @allure.step("Дождаться окна завершенного заказа")
    def wait_completed_order(self, timeout: int = 40) -> None:
        WebDriverWait(self.driver, timeout).until(lambda driver: "приедет" in self.body_text())

    @allure.step("Открыть окно Детали")
    def open_details(self) -> None:
        self.wait_clickable(TaxiPageLocators.DETAILS_BUTTON).click()

    @allure.step("Нажать кнопку Отменить")
    def cancel_order(self) -> None:
        self.wait_clickable(TaxiPageLocators.CANCEL_BUTTON).click()

    @allure.step("Проверить наличие чекбокса Столик для ноутбука")
    def has_laptop_checkbox(self) -> bool:
        return "Столик для ноутбука" in self.body_text()

    @allure.step("Включить чекбокс Столик для ноутбука")
    def toggle_laptop_checkbox(self) -> None:
        self.find(TaxiPageLocators.LAPTOP_CHECKBOX).click()
