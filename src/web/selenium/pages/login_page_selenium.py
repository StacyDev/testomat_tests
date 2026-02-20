from selenium.webdriver.common.by import By

from src.web.selenium.core.driver_actions import DriverActions
from src.web.selenium.core.element_actions import ElementActions


class LoginPageSelenium:
    def __init__(self, driver_actions: DriverActions, element_actions: ElementActions):
        self.driver_actions = driver_actions
        self.element_actions = element_actions

        self._loc_sign_in_block: tuple[By | str, str] = (
            By.CSS_SELECTOR,
            "#content-desktop form#new_user",
        )
        self._loc_email_inp: tuple[By | str, str] = (
            By.CSS_SELECTOR,
            "#content-desktop #user_email",
        )
        self._loc_password_inp: tuple[By | str, str] = (
            By.CSS_SELECTOR,
            "#content-desktop input#user_password",
        )
        self._loc_submit_btn: tuple[By | str, str] = (
            By.CSS_SELECTOR,
            "#content-desktop input[type='submit']",
        )
        self._loc_invalid_creds_msg: tuple[By | str, str] = (
            By.XPATH,
            "//*[@id='content-desktop']//p[contains(text(), 'Invalid Email or password.')]",
        )

    def open(self, url: str) -> LoginPageSelenium:
        self.driver_actions.open_url(url)
        return self

    def is_loaded(self) -> LoginPageSelenium:
        self.element_actions.wait.for_element_present(self._loc_sign_in_block)
        self.element_actions.wait.for_visible(self._loc_email_inp)
        self.element_actions.wait.for_visible(self._loc_password_inp)
        self.element_actions.wait.for_visible(self._loc_submit_btn)
        return self

    def login(self, email: str, password: str):
        self.element_actions.type_text(self._loc_email_inp, email)
        self.element_actions.type_text(self._loc_password_inp, password)
        self.element_actions.click(self._loc_submit_btn)

    def is_invalid_message_visible(self) -> LoginPageSelenium:
        self.element_actions.wait.for_visible(self._loc_invalid_creds_msg)
        return self
