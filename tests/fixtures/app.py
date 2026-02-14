import json
from pathlib import Path
from typing import Generator

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, ViewportSize, expect

from src.web.application import Application
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper, clear_browser_state

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STATE_PATH = Path("test-result/.auth/free_project_state.json")


def create_free_project_storage_state() -> None:
    if not STORAGE_STATE_PATH.exists():
        return

    state = json.loads(STORAGE_STATE_PATH.read_text())
    for cookie in state.get("cookies", []):
        if cookie.get("name") == "company_id":
            cookie["value"] = ""
            break

    FREE_PROJECT_STATE_PATH.write_text(json.dumps(state, indent=2))


def build_browser_context(
    browser: Browser, base_url: str, storage_state: Path | None = None
) -> BrowserContext:
    viewport_size: ViewportSize = {"width": 1280, "height": 720}
    kwargs = {
        "base_url": base_url,
        "viewport": viewport_size,
        "device_scale_factor": 1,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "test-result/videos/",
        "permissions": ["geolocation"],
    }

    if storage_state and storage_state.exists():
        kwargs["storage_state"] = str(storage_state)

    return browser.new_context(**kwargs)


@pytest.fixture(scope="function")
def app(browser_instance: Browser, configs: Config) -> Generator[Application, None, None]:
    context = build_browser_context(browser_instance, configs.base_app_url)
    page: Page = context.new_page()
    yield Application(page)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_page(browser_instance: Browser, configs: Config) -> Generator[Page, None, None]:
    if STORAGE_STATE_PATH.exists():
        context = build_browser_context(
            browser_instance, configs.base_app_url, storage_state=STORAGE_STATE_PATH
        )
        yield context.new_page()
        context.close()
        return

    context = build_browser_context(browser_instance, configs.base_app_url)

    page: Page = context.new_page()
    app = Application(page)
    (app.login_page.open().is_loaded().login(configs.email, configs.password))

    app.projects_page.is_loaded().open_company_projects("QA Club Lviv")
    STORAGE_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(STORAGE_STATE_PATH))
    create_free_project_storage_state()

    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_app(logged_page: Page) -> Generator[Application, None, None]:
    logged_page.goto("/projects")
    yield Application(logged_page)


@pytest.fixture(scope="function")
def cookies(logged_page: Page) -> CookieHelper:
    return CookieHelper(logged_page.context)


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs: Config) -> Generator[Page, None, None]:
    context = build_browser_context(browser_instance, configs.base_app_url)
    page: Page = context.new_page()
    yield page
    page.close()
    context.close()


@pytest.fixture(scope="function")
def shared_page(shared_browser: Page) -> Generator[Application, None, None]:
    yield Application(shared_browser)
    clear_browser_state(shared_browser)


@pytest.fixture(scope="session")
def free_project_page(browser_instance: Browser, configs) -> Generator[Page, None, None]:
    if FREE_PROJECT_STATE_PATH.exists():
        context = build_browser_context(
            browser_instance, configs.base_app_url, storage_state=FREE_PROJECT_STATE_PATH
        )
        yield context.new_page()
        context.close()
        return

    context = build_browser_context(browser_instance, configs.base_app_url)

    page: Page = context.new_page()
    app = Application(page)
    (app.login_page.open().is_loaded().login(configs.email, configs.password))

    app.projects_page.is_loaded().open_company_projects("Free Projects")
    expect(app.projects_page.get_free_plan_label_locator()).to_be_visible()

    FREE_PROJECT_STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=str(FREE_PROJECT_STATE_PATH))

    yield page
    context.close()


@pytest.fixture(scope="function")
def free_project_app(free_project_page: Page) -> Generator[Application, None, None]:
    free_project_page.goto("/projects")
    yield Application(free_project_page)
    free_project_page.close()
