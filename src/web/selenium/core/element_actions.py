from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

from src.web.selenium.core.waits import Wait


class ElementActions:
    def __init__(self, wait_wrapper: Wait):
        self.wait = wait_wrapper

    def click(self, locator: tuple[By, str]):
        self.wait.for_visible(locator)
        self.wait.for_clickable(locator).click()

    def type_text(self, locator: tuple[By, str], text: str):
        self.wait.for_visible(locator).send_keys(text)

    def clear(self, locator: tuple[By, str]):
        self.wait.for_visible(locator).clear()

    def double_click(self, locator: tuple[By, str]):
        self.wait.for_visible(locator).click()

    def select_value(self, locator: tuple[By, str], value: str):
        ddown_element = self.wait.for_visible(locator)
        select: Select = Select(ddown_element)
        select.select_by_visible_text(value)
