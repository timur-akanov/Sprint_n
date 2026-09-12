from __future__ import annotations

import allure

from data import ADDRESS_FROM, TAXI_DESCRIPTIONS


class TestRouteSelection:
    @allure.title("Route selection block contains all tariffs")
    def test_route_selection_block_contains_all_tariffs(self, prepared_route_page):
        text = prepared_route_page.route_text()
        prepared_route_page.wait_route_selection_block()

        assert "Вызвать такси" in text
        for tariff_name in TAXI_DESCRIPTIONS:
            assert tariff_name in text

    @allure.title("Route selection block for same addresses shows free auto route")
    def test_route_selection_with_same_addresses(self, route_page):
        route_page.fill_addresses(ADDRESS_FROM, ADDRESS_FROM)
        route_page.wait_route_selection_block()
        route_page.wait_for_text("В пути 0 мин.")
        text = route_page.route_text()

        assert "Авто Бесплатно" in text
        assert "В пути 0 мин." in text
