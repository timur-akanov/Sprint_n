from __future__ import annotations

import allure
import pytest

from data import PHONE_NUMBER


class TestFullTaxiFlow:
    @allure.title("Full taxi flow: route, tariff, phone and order state")
    def test_full_taxi_flow(self, taxi_page):
        selected_tariff = "Сонный"

        taxi_page.select_tariff(selected_tariff)
        taxi_page.fill_phone(PHONE_NUMBER)
        taxi_page.call_taxi()

        text = taxi_page.body_text()
        assert "Ввести номер и заказать" in text
        assert "Маршрут составит 3 км. и займёт 3 мин." in text

    @pytest.mark.xfail(reason="Known app instability: option 'Столик для ноутбука' may be missing for selected tariff")
    @allure.title("Taxi order with laptop table option opens search window")
    def test_taxi_order_with_laptop_table(self, taxi_page):
        taxi_page.select_tariff("Рабочий")
        taxi_page.call_taxi()
        taxi_page.fill_phone(PHONE_NUMBER)

        assert taxi_page.has_laptop_checkbox()
        taxi_page.toggle_laptop_checkbox()
        taxi_page.submit_order()
        taxi_page.wait_search_window()

        assert "Поиск машины" in taxi_page.body_text()
        assert "Детали" in taxi_page.body_text()
        assert "Отменить" in taxi_page.body_text()

    @pytest.mark.xfail(reason="Known app instability: completed order state and details may not be reliably rendered")
    @allure.title("Taxi search timer ends with completed order details and cancel closes popup")
    def test_taxi_completed_order_details_and_cancel(self, taxi_page):
        taxi_page.select_tariff("Рабочий")
        taxi_page.call_taxi()
        taxi_page.fill_phone(PHONE_NUMBER)
        taxi_page.submit_order()

        taxi_page.wait_search_window()
        taxi_page.wait_completed_order()

        text = taxi_page.body_text()
        assert "приедет" in text
        assert "Детали" in text
        assert "Отменить" in text

        taxi_page.open_details()
        details_text = taxi_page.body_text()
        assert "Еще про поездку" in details_text
        assert "Стоимость" in details_text

        taxi_page.cancel_order()
        assert "Поиск машины" not in taxi_page.body_text()
