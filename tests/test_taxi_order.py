from __future__ import annotations

import allure
import pytest

from data import TAXI_DESCRIPTIONS


class TestTaxiOrder:
    @allure.title("Taxi order form has 6 tariffs and one active tariff")
    def test_taxi_form_has_tariffs_and_active_item(self, taxi_page):
        taxi_page.call_taxi()
        text = taxi_page.body_text()

        assert taxi_page.tariffs_count() == 6
        assert taxi_page.active_tariffs_count() == 1
        for expected_name in TAXI_DESCRIPTIONS:
            assert expected_name in text

    @pytest.mark.xfail(reason="Known app bug: tooltip i-button becomes non-interactable for some tariffs")
    @allure.title("Taxi tariff descriptions on hover match TЗ")
    def test_taxi_tariff_descriptions_match_tz(self, taxi_page):
        taxi_page.call_taxi()

        for tariff_name, expected_description in TAXI_DESCRIPTIONS.items():
            taxi_page.hover_tariff_info(tariff_name)
            assert taxi_page.tariff_description(tariff_name) == expected_description

    @allure.title("Taxi order form contains required fields")
    def test_taxi_form_contains_required_fields(self, taxi_page):
        taxi_page.call_taxi()

        assert taxi_page.order_fields_visible()
