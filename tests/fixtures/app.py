import os
from pathlib import Path
from typing import Any, Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, StorageState, ViewportSize

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper
from tests.fixtures.infrastructure_handler import do_login_steps

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")


def build_browser_context(browser: Browser, base_url: str) -> BrowserContext:
    viewport_size: ViewportSize = {"width": 1280, "height": 720}
    return browser.new_context(
        base_url=base_url,
        viewport=viewport_size,
        device_scale_factor=1,
        locale="uk-UA",
        timezone_id="Europe/Kyiv",
        record_video_dir="test-result/videos/",
        permissions=["geolocation"],
    )


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config) -> Generator[Application, None, None]:
    context = build_browser_context(browser_instance, configs.base_app_url)
    page: Page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_context(
    browser_instance: Browser, configs: Config
) -> Generator[BrowserContext, None, None]:
    context = build_browser_context(browser_instance, configs.base_app_url)

    page: Page = context.new_page()
    app = Application(page)
    app.login_page.open().is_loaded().login(configs.email, configs.password)

    app.projects_page.is_loaded()
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(STORAGE_STATE_PATH))

    page.close()
    yield context
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_context: BrowserContext) -> Generator[Application, None, None]:
    page: Page = logged_context.new_page()
    page.goto("/")
    yield Application(page)
    page.close()


@pytest.fixture(scope="function")
def cookies(logged_context: BrowserContext) -> CookieHelper:
    return CookieHelper(logged_context)


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs: Config) -> Generator[Page, None, None]:
    context = build_browser_context(browser_instance, configs.base_app_url)
    page: Page = context.new_page()
    yield page
    page.close()
    context.close()
