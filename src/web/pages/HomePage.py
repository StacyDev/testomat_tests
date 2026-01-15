from playwright.sync_api import Page, expect


class HomePage:
    def __init__(self, page: Page):
        self.page = page
        self.loc_menu_header = self.page.locator("#headerMenuWrapper")
        self.loc_login_lnk = self.page.locator(".login-item[href*='sign_in']")
        self.loc_sign_up_lnk = self.page.locator(".start-item[href*='sign_up']")

    def open(self):
        self.page.goto("https://testomat.io")

    def is_loaded(self):
        expect(self.loc_menu_header).to_be_visible()
        expect(self.loc_login_lnk).to_be_visible()
        expect(self.loc_sign_up_lnk).to_be_visible()

    def open_login_page_by_click(self):
        self.loc_login_lnk.click()
