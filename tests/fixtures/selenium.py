from typing import Any, Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver

from src.web.selenium.core.driver_actions import DriverActions
from src.web.selenium.core.element_actions import ElementActions
from src.web.selenium.core.waits import Wait
from src.web.selenium.selenium_application import SeleniumApplication


@pytest.fixture(scope="module")
def driver(request) -> Generator[WebDriver, None, None]:
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Force desktop view
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def wait(driver) -> Wait:
    return Wait(driver, timeout=10)


@pytest.fixture(scope="function")
def element_actions(wait: Wait) -> ElementActions:
    return ElementActions(wait_wrapper=wait)


@pytest.fixture(scope="function")
def driver_actions(driver: WebDriver, wait: Wait) -> Generator[DriverActions, None, None]:
    yield DriverActions(driver=driver, wait=wait)
    driver.delete_all_cookies()
    driver.get("about:blank")


@pytest.fixture(scope="function")
def selenium_app(
    element_actions: ElementActions, driver_actions: DriverActions
) -> SeleniumApplication:
    return SeleniumApplication(element_actions, driver_actions)
