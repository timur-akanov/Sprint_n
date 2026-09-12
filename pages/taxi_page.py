from __future__ import annotations

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.route_page import RoutePage


class TaxiPage(RoutePage):
    CALL_TAXI_BUTTON = (By.XPATH, "//button[contains(@class,'button round') and contains(., 'Вызвать такси')]")
    PHONE_INPUT = (By.ID, "phone")
    SUBMIT_ORDER_BUTTON = (By.XPATH, "//button[contains(., 'Ввести номер и заказать')]")
    DETAILS_BUTTON = (By.XPATH, "//button[contains(., 'Детали')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(., 'Отменить')]")

    def select_tariff(self, tariff_title: str) -> None:
        card = self.find(
            (
                By.XPATH,
                f"//div[contains(@class,'tcard')][.//div[contains(@class,'tcard-title') and normalize-space()='{tariff_title}']]",
            )
        )
        button = card.find_element(By.CSS_SELECTOR, "button.tcard-i")
        ActionChains(self.driver).move_to_element(card).perform()
        self.driver.execute_script("arguments[0].click();", button)

    def tariffs_count(self) -> int:
        return len(self.driver.find_elements(By.CSS_SELECTOR, "div.tcard"))

    def active_tariffs_count(self) -> int:
        cards = self.driver.find_elements(By.CSS_SELECTOR, "div.tcard")
        return len([card for card in cards if "active" in card.get_attribute("class")])

    def tariff_titles(self) -> list[str]:
        return [el.text.strip() for el in self.driver.find_elements(By.CSS_SELECTOR, "div.tcard-title") if el.text.strip()]

    def hover_tariff_info(self, tariff_title: str) -> None:
        card = self.find(
            (
                By.XPATH,
                f"//div[contains(@class,'tcard')][.//div[contains(@class,'tcard-title') and normalize-space()='{tariff_title}']]",
            )
        )
        i_button = card.find_element(By.CSS_SELECTOR, "button.tcard-i")
        ActionChains(self.driver).move_to_element(card).move_to_element(i_button).perform()

    def tariff_description(self, tariff_title: str) -> str:
        card = self.find(
            (
                By.XPATH,
                f"//div[contains(@class,'tcard')][.//div[contains(@class,'tcard-title') and normalize-space()='{tariff_title}']]",
            )
        )
        description = card.find_element(By.CSS_SELECTOR, "div.i-dPrefix")
        return description.text.strip()

    def fill_phone(self, phone_number: str) -> None:
        phone = self.find(self.PHONE_INPUT)
        self.set_input_value(phone, phone_number)

    def try_fill_phone_by_typing(self, phone_number: str) -> str:
        phone = self.find(self.PHONE_INPUT)
        phone.click()
        phone.send_keys(phone_number)
        return phone.get_attribute("value")

    def call_taxi(self) -> None:
        button = self.wait_clickable(self.CALL_TAXI_BUTTON)
        ActionChains(self.driver).move_to_element(button).click(button).perform()

    def order_fields_visible(self) -> bool:
        text = self.body_text()
        return all(
            part in text
            for part in ["Телефон", "Способ оплаты", "Комментарий водителю", "Требования к заказу"]
        )

    def submit_order(self) -> None:
        self.wait_clickable(self.SUBMIT_ORDER_BUTTON).click()

    def wait_search_window(self, timeout: int = 20) -> None:
        WebDriverWait(self.driver, timeout).until(lambda driver: "Поиск машины" in self.body_text())

    def wait_completed_order(self, timeout: int = 40) -> None:
        WebDriverWait(self.driver, timeout).until(lambda driver: "приедет" in self.body_text())

    def open_details(self) -> None:
        self.wait_clickable(self.DETAILS_BUTTON).click()

    def cancel_order(self) -> None:
        self.wait_clickable(self.CANCEL_BUTTON).click()

    def has_laptop_checkbox(self) -> bool:
        return "Столик для ноутбука" in self.body_text()

    def toggle_laptop_checkbox(self) -> None:
        self.find((By.XPATH, "//*[contains(text(), 'Столик для ноутбука')]")).click()
