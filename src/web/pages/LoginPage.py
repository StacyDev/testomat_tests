from playwright.sync_api import Page
from playwright.sync_api import expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self._loc_sign_in_block = self.page.locator("#content-desktop form#new_user")
        self._loc_email_inp = self.page.get_by_role("textbox", name="name@email.com")
        self._loc_password_inp = self.page.locator("#content-desktop input#user_password")
        self._loc_submit_btn = self.page.locator("#content-desktop input[type='submit']")
        self._loc_invalid_creds_msg = self.page.locator("#content-desktop").get_by_text(
            'Invalid Email or password.',
            exact=False)

    def open(self) -> LoginPage:
        self.page.goto("/users/sign_in")
        return self

    def is_loaded(self) -> LoginPage:
        expect(self._loc_sign_in_block).to_be_visible()
        return self

    def login(self, email: str, password: str):
        self._loc_email_inp.type(email)
        self._loc_password_inp.type(password)
        self._loc_submit_btn.click()

    def is_invalid_message_visible(self) -> LoginPage:
        expect(self._loc_invalid_creds_msg).to_be_visible()
        return self
