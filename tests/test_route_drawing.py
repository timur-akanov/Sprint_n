from __future__ import annotations

import allure
import pytest

from data import ADDRESS_FROM, ADDRESS_TO


class TestRouteDrawing:
    @pytest.mark.xfail(reason="Known app bug: map placemark overlays are unstable and may not render in DOM")
    @allure.title("Route drawing for two preset addresses")
    def test_route_drawing_with_two_preset_addresses(self, prepared_route_page):
        prepared_route_page.wait_map_points()
        text = prepared_route_page.route_text()

        assert prepared_route_page.from_value() == ADDRESS_FROM
        assert prepared_route_page.to_value() == ADDRESS_TO
        assert "Такси ~" in text
        assert "В пути" in text
        assert prepared_route_page.map_points_count() >= 2

    @pytest.mark.xfail(reason="Known app bug: map placemark overlays are unstable and may not render in DOM")
    @allure.title("Route drawing works for reversed preset addresses")
    def test_route_drawing_with_reversed_addresses(self, route_page):
        route_page.fill_addresses(ADDRESS_TO, ADDRESS_FROM)
        route_page.wait_route_ready()
        route_page.wait_map_points()

        assert route_page.from_value() == ADDRESS_TO
        assert route_page.to_value() == ADDRESS_FROM
        assert route_page.map_points_count() >= 2
