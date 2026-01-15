from playwright.sync_api import Page
from playwright.sync_api import expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.loc_sign_in_block = self.page.locator("#content-desktop form#new_user")
        self.loc_email_inp = self.page.get_by_role("textbox", name="name@email.com")
        self.loc_password_inp = self.page.locator("#content-desktop input#user_password")
        self.loc_submit_btn = self.page.locator("#content-desktop input[type='submit']")
        self.loc_invalid_creds_msg = self.page.locator("#content-desktop").get_by_text('Invalid Email or password.',
                                                                                       exact=False)

    def open(self):
        self.page.goto("/users/sign_in")

    def is_loaded(self):
        expect(self.loc_sign_in_block).to_be_visible()

    def login(self, email: str, password: str):
        self.loc_email_inp.type(email)
        self.loc_password_inp.type(password)
        self.loc_submit_btn.click()

    def is_invalid_message_visible(self):
        expect(self.loc_invalid_creds_msg).to_be_visible()
