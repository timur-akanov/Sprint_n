from __future__ import annotations

from pages.route_page import RoutePage


class DrivePage(RoutePage):
    def drive_section_visible(self) -> bool:
        text = self.body_text().lower()
        return "драйв" in text or "drive" in text
