from __future__ import annotations

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver

    def open(self, url: str) -> None:
        self.driver.get(url)

    def find(self, locator: tuple[str, str]):
        return self.driver.find_element(*locator)

    def wait_visible(self, locator: tuple[str, str], timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(ec.visibility_of_element_located(locator))

    def wait_clickable(self, locator: tuple[str, str], timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(ec.element_to_be_clickable(locator))

    def body_text(self) -> str:
        return self.driver.execute_script("return document.body.innerText")

    def wait_for_text(self, text: str, timeout: int = 10) -> None:
        WebDriverWait(self.driver, timeout).until(lambda driver: text in self.body_text())

    def set_input_value(self, element, value: str) -> None:
        self.driver.execute_script(
            """
            const el = arguments[0];
            const nextValue = arguments[1];
            const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(el, nextValue);
            el.dispatchEvent(new Event('input', { bubbles: true }));
            el.dispatchEvent(new Event('change', { bubbles: true }));
            """,
            element,
            value,
        )

