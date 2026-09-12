from __future__ import annotations

import allure
import pytest

from data import PHONE_NUMBER


class TestTaxiPreparation:
    @pytest.mark.xfail(reason="Known app bug: the phone field is not directly interactable with normal Selenium typing")
    def test_phone_input_is_not_interactable_without_js(self, taxi_page):
        assert taxi_page.try_fill_phone_by_typing(PHONE_NUMBER) == PHONE_NUMBER


    @allure.title("Taxi preparation exposes phone, payment and comment fields")
    def test_taxi_preparation_shows_order_fields(self, taxi_page):
        taxi_page.call_taxi()
        text = taxi_page.body_text()

        assert "Телефон" in text
        assert "Способ оплаты" in text
        assert "Наличные" in text
        assert "Комментарий водителю" in text

    @allure.title("Switching between Оптимальный and Быстрый changes active tab and route info")
    def test_switching_between_optimal_and_fast(self, prepared_route_page):
        prepared_route_page.select_mode("Оптимальный")
        optimal_price, optimal_time = prepared_route_page.current_price_and_time()

        prepared_route_page.select_mode("Быстрый")
        fast_price, fast_time = prepared_route_page.current_price_and_time()

        assert prepared_route_page.mode_is_active("Быстрый")
        assert optimal_price != ""
        assert fast_price != ""
        assert optimal_time != ""
        assert fast_time != ""
        assert (optimal_price, optimal_time) != (fast_price, fast_time)

    @allure.title("Switching to Свой enables movement types and keeps taxi action")
    def test_switching_to_custom_mode_enables_types(self, prepared_route_page):
        prepared_route_page.select_mode("Свой")

        assert prepared_route_page.mode_is_active("Свой")
        assert prepared_route_page.custom_types_count() == 6
        assert prepared_route_page.call_taxi_button_visible()

    @allure.title("Selecting Быстрый keeps the taxi call button active")
    def test_fast_mode_has_call_taxi_button(self, prepared_route_page):
        prepared_route_page.select_mode("Быстрый")

        assert prepared_route_page.mode_is_active("Быстрый")
        assert prepared_route_page.call_taxi_button_visible()

    @allure.title("Selecting Свой and type Драйв enables booking button")
    def test_custom_drive_mode_has_booking_button(self, prepared_route_page):
        prepared_route_page.select_mode("Свой")
        prepared_route_page.select_drive_type()

        assert prepared_route_page.drive_type_is_active()
        assert prepared_route_page.book_button_visible()
