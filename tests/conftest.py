import os
from dataclasses import dataclass
from typing import Any, Generator

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Locator, Browser, StorageState, BrowserContext

from src.web.Application import Application

load_dotenv()


@dataclass(frozen=True)
class Config:
    base_url: str
    base_app_url: str
    email: str
    password: str


DEFAULT_PROJ_CLASSIC = "Classic Project1"
DEFAULT_PROJ_BDD = "BDD Project1"
DEFAULT_COMPANY = "Free Projects"


@pytest.fixture(scope="session")
def configs():
    return Config(
        base_app_url=f"{os.getenv("BASE_APP_URL")}/users/sign_in",
        email=os.getenv("EMAIL"),
        password=os.getenv("PASSWORD"),
        base_url=os.getenv("BASE_URL")
    )


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chromium",
        "headless": False,
        "slow_mo": 100,  # interval between actions
        "timeout": 60000,  # maximal timeout for each test
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict) -> dict:
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1280, "height": 720},
        "device_scale_factor": 1,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "test-result/videos/",
        "permissions": ["geolocation"]
    }


# this fixture creates 1 session/context for the whole file (module)
@pytest.fixture(scope="module")
def shared_browser_context(browser: Browser, browser_context_args: dict) -> Generator[
    BrowserContext, None, None]:
    context = browser.new_context(**browser_context_args)
    try:
        yield context
    finally:
        context.close()


# this fixture allows reusing context (cookies/cache)
@pytest.fixture(scope="function")
def app_shared_page(shared_browser_context: BrowserContext, request) -> Generator[Application,
None, None]:
    shared_browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page: Page = shared_browser_context.new_page()

    yield Application(page)

    video_path = None
    try:
        if page.video:
            video_path = page.video.path()
        failed = is_test_failed(request)
        record_trace_if_failed(failed, shared_browser_context, request)
    finally:
        try:
            shared_browser_context.tracing.stop()
        except:
            pass
        page.close()
        shared_browser_context.clear_cookies()

        if video_path and not is_test_failed(request):
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
            except Exception as e:
                print(f"Failed to delete video: {e}")


def is_test_failed(request) -> bool:
    if hasattr(request.node, "rep_call"):
        return request.node.rep_call.failed
    return True


def record_trace_if_failed(has_failed: bool, context: BrowserContext, request):
    if has_failed:
        trace_path = f"test-result/custom-fixture-traces/{request.node.name}/trace.zip"
        context.tracing.stop(path=trace_path)  # when providing path argument tracing is stopped
        # with saving
    else:
        context.tracing.stop()


@pytest.fixture(scope="module")
def logged_in_storage(shared_browser_context: BrowserContext, configs: Config) -> StorageState:
    page: Page = shared_browser_context.new_page()  # temporary page for login
    temp_app = Application(page)

    do_login_steps(temp_app, configs)

    # capture Cookies/LocalStorage
    storage = shared_browser_context.storage_state()

    page.close()
    return storage


@pytest.fixture(scope="function")
def auth_app(browser: Browser, browser_context_args: dict, logged_in_storage: StorageState,
             request) -> \
        Generator[Application, None, None]:
    context_params = {
        **browser_context_args,
        "storage_state": logged_in_storage
    }

    context = browser.new_context(**context_params)

    context.tracing.start(screenshots=True, snapshots=True, sources=True)
    page: Page = context.new_page()
    if page.url == "about:blank":
        page.goto(browser_context_args.get("base_url"))

    yield Application(page)

    video_path = None
    if page.video:
        video_path = page.video.path()

    try:
        failed = is_test_failed(request)
        record_trace_if_failed(failed, context, request)
    finally:
        try:
            context.tracing.stop()
        except:
            pass
        page.close()
        context.clear_cookies()
        context.close()

        if video_path and not is_test_failed(request):
            try:
                if os.path.exists(video_path):
                    os.remove(video_path)
            except Exception as e:
                print(f"Failed to delete video: {e}")


@pytest.fixture(scope="function")
def remove_test_projects(auth_app: Application, configs: Config):
    app = auth_app
    delete_multiple_projects(app, DEFAULT_COMPANY, DEFAULT_PROJ_CLASSIC)
    delete_multiple_projects(app, DEFAULT_COMPANY, DEFAULT_PROJ_BDD)


@pytest.fixture
def remove_non_default_test_projects(auth_app: Application, configs: Config) -> Generator[list,
None, None]:
    project_container: list = []

    yield project_container

    if project_container:
        project_name = project_container[0]
        delete_multiple_projects(auth_app, DEFAULT_COMPANY, project_name)


@pytest.fixture(scope="function")
def create_test_project(auth_app: Application, configs: Config, remove_test_projects):
    app = auth_app
    (app.projects_page.is_loaded()
     .open_company_projects(DEFAULT_COMPANY)
     .click_create_project())
    do_create_project_steps(app, "classic", DEFAULT_PROJ_CLASSIC)


@pytest.fixture(scope="function")
def create_multiple_projects(auth_app: Application, configs: Config, remove_test_projects):
    app = auth_app
    (app.projects_page.is_loaded()
     .open_company_projects(DEFAULT_COMPANY)
     .click_create_project())
    do_create_project_steps(app, "classic", DEFAULT_PROJ_CLASSIC)
    app.projects_page.click_create_project()
    do_create_project_steps(app, "bdd", DEFAULT_PROJ_BDD)


def delete_multiple_projects(auth_app: Application, company_name: str, project_name: str):
    app = auth_app
    (app.projects_page.is_loaded()
     .open_company_projects(company_name))
    project_items: list[Locator] = app.projects_page.get_projects_list_by_name(project_name)

    while len(project_items) > 0:
        project_items[0].click()

        (app.single_project_page.is_loaded()
         .open_project_settings()
         .trigger_and_confirm_project_delete()
         .return_to_projects_list())

        project_items = (app.projects_page.is_loaded()
                         .get_projects_list_by_name(project_name))


def do_login_steps(app: Application, configs: Config):
    (app.login_page
     .open()
     .is_loaded()
     .login(configs.email, configs.password))


def do_create_project_steps(app: Application, proj_type: str, project_name):
    (app.create_project_page.is_loaded()
     .create_project(proj_type, project_name))
    (app.single_project_page.is_loaded()
     .return_to_projects_list())
