from __future__ import annotations

from playwright.sync_api import Page, expect

from src.web.pages.login_page import LoginPage


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self._loc_menu_header = self.page.locator("#headerMenuWrapper")
        self._loc_login_lnk = self.page.locator(".login-item[href*='sign_in']")
        self._loc_sign_up_lnk = self.page.locator(".start-item[href*='sign_up']")

    def open(self) -> HomePage:
        self.page.goto("https://testomat.io")
        return self

    def is_loaded(self) -> HomePage:
        expect(self._loc_menu_header).to_be_visible()
        expect(self._loc_login_lnk).to_be_visible()
        expect(self._loc_sign_up_lnk).to_be_visible()
        return self

    def open_login_page_by_click(self) -> LoginPage:
        self._loc_login_lnk.click()
        return LoginPage(self.page)
