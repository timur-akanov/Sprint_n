from __future__ import annotations

import os
from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager

from data import ADDRESS_FROM, ADDRESS_TO
from pages.drive_page import DrivePage
from pages.main_page import MainPage
from pages.route_page import RoutePage
from pages.taxi_page import TaxiPage

BASE_URL = os.environ.get("ROUTES_BASE_URL", "https://qa-routes.education-services.ru/")
HEADLESS = os.environ.get("HEADLESS", "1") == "1"


@pytest.fixture
def driver() -> Generator[webdriver.Chrome, None, None]:
    options = Options()
    options.add_argument("--window-size=1440,1200")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if HEADLESS:
        options.add_argument("--headless=new")
    service = Service(ChromeDriverManager().install())
    browser = webdriver.Chrome(service=service, options=options)
    yield browser
    browser.quit()


@pytest.fixture
def main_page(driver: webdriver.Chrome) -> MainPage:
    page = MainPage(driver)
    page.open(BASE_URL)
    return page


@pytest.fixture
def route_page(main_page: MainPage) -> RoutePage:
    return RoutePage(main_page.driver)


@pytest.fixture
def prepared_route_page(route_page: RoutePage) -> RoutePage:
    route_page.fill_addresses(ADDRESS_FROM, ADDRESS_TO)
    route_page.wait_route_ready()
    return route_page


@pytest.fixture
def taxi_page(prepared_route_page: RoutePage) -> TaxiPage:
    page = TaxiPage(prepared_route_page.driver)
    page.select_mode("Быстрый")
    return page


@pytest.fixture
def drive_page(prepared_route_page: RoutePage) -> DrivePage:
    return DrivePage(prepared_route_page.driver)

