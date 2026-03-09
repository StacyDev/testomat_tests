import json
import os
from pathlib import Path
from typing import Generator

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, ViewportSize, expect

from src.web.application import Application
from tests.conftest import TEST_RESULT_DIR
from tests.fixtures.config import Config
from tests.fixtures.cookie_helper import CookieHelper, clear_browser_state

STORAGE_STATE_PATH = Path("test-result/.auth/storage_state.json")
FREE_PROJECT_STATE_PATH = Path("test-result/.auth/free_project_state.json")
TRACES_DIR = Path("test-result/traces")


def get_or_create_context(
    browser: Browser, base_url: str, storage_path: Path
) -> tuple[BrowserContext, bool]:
    # returns context and flag, indicating if login is needed
    # if storage exist load it with no login, else create fresh context and login
    has_state = storage_path.exists()
    viewport_size: ViewportSize = {"width": 1280, "height": 720}
    kwargs = {
        "base_url": base_url,
        "viewport": viewport_size,
        "device_scale_factor": 1,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "permissions": ["geolocation"],
    }
    if os.getenv("CI", "false").lower() != "true":
        kwargs["record_video_dir"] = str(TEST_RESULT_DIR / "videos/")

    if has_state:
        kwargs["storage_state"] = str(storage_path)

    context = browser.new_context(**kwargs)
    return context, not has_state  # needs login = True if no stat


def save_storage_state(context: BrowserContext, storage_path: Path) -> None:
    storage_path.parent.mkdir(parents=True, exist_ok=True)
    context.storage_state(path=storage_path)


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
def app(
    browser_instance: Browser, configs: Config, request: pytest.FixtureRequest
) -> Generator[Application, None, None]:
    context = build_browser_context(browser_instance, configs.base_sing_in_url)
    page: Page = context.new_page()
    start_tracing(context)
    yield Application(page)

    stop_tracing_preserving_failed_case_tracing(page, request)
    page.close()
    context.close()


@pytest.fixture(scope="session")
def logged_page(browser_instance: Browser, configs: Config) -> Generator[Page, None, None]:
    context, needs_login = get_or_create_context(
        browser_instance, configs.base_url_app, STORAGE_STATE_PATH
    )

    page: Page = context.new_page()

    if needs_login:
        app = Application(page)
        (app.login_page.open().is_loaded().login(configs.email, configs.password))

        app.projects_page.is_loaded().open_company_projects("QA Club Lviv")
        save_storage_state(context, STORAGE_STATE_PATH)
        create_free_project_storage_state()

    yield page
    context.close()


@pytest.fixture(scope="function")
def logged_app(
    logged_page: Page, request: pytest.FixtureRequest
) -> Generator[Application, None, None]:
    start_tracing(logged_page.context)
    logged_page.goto("/projects")
    yield Application(logged_page)

    stop_tracing_preserving_failed_case_tracing(logged_page, request)


@pytest.fixture(scope="function")
def cookies(logged_page: Page) -> CookieHelper:
    return CookieHelper(logged_page.context)


@pytest.fixture(scope="module")
def shared_browser(browser_instance: Browser, configs: Config) -> Generator[Page, None, None]:
    context = build_browser_context(browser_instance, configs.base_sing_in_url)
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
    context, needs_login = get_or_create_context(
        browser_instance, configs.base_url_app, FREE_PROJECT_STATE_PATH
    )

    page: Page = context.new_page()

    if needs_login:
        app = Application(page)
        (app.login_page.open().is_loaded().login(configs.email, configs.password))

        app.projects_page.is_loaded().open_company_projects("Free Projects")
        expect(app.projects_page.get_free_plan_label_locator()).to_be_visible()

        save_storage_state(context, FREE_PROJECT_STATE_PATH)
        # create_free_project_storage_state()

    yield page
    context.close()


@pytest.fixture(scope="function")
def free_project_app(
    free_project_page: Page, request: pytest.FixtureRequest
) -> Generator[Application, None, None]:
    start_tracing(free_project_page.context)
    free_project_page.goto("/projects")
    yield Application(free_project_page)

    stop_tracing_preserving_failed_case_tracing(free_project_page, request)
    free_project_page.close()


def start_tracing(context: BrowserContext) -> None:
    context.tracing.start(screenshots=True, snapshots=True, sources=True)


def stop_tracing_preserving_failed_case_tracing(page: Page, request: pytest.FixtureRequest) -> None:
    failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    if failed:
        allure.attach(
            page.screenshot(), name="screenshot", attachment_type=allure.attachment_type.PNG
        )
        trace_path = TRACES_DIR / f"{request.node.name}.zip"
        trace_path.parent.mkdir(parents=True, exist_ok=True)
        page.context.tracing.stop(path=str(trace_path))

        allure.attach.attach(
            str(trace_path),
            name="trace",
            extension="zip",
            attachment_type="application/vnd.allure.playwright-trace",
        )

    else:
        page.context.tracing.stop()
