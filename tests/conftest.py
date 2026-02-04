import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Locator

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


@pytest.fixture(scope="function")
def login(app: Application, configs):
    do_login_steps(app, configs)


@pytest.fixture(scope="function")
def remove_test_projects(app: Application, configs):
    do_login_steps(app, configs)
    delete_multiple_projects(app, DEFAULT_COMPANY, DEFAULT_PROJ_CLASSIC)
    delete_multiple_projects(app, DEFAULT_COMPANY, DEFAULT_PROJ_BDD)


@pytest.fixture
def remove_non_default_test_projects(app: Application, configs):
    project_container = []

    yield project_container

    if project_container:
        project_name = project_container[0]
        delete_multiple_projects(app, DEFAULT_COMPANY, project_name)


@pytest.fixture(scope="function")
def create_test_project(app: Application, configs, remove_test_projects):
    (app.projects_page.is_loaded()
     .open_company_projects(DEFAULT_COMPANY)
     .click_create_project())
    do_create_project_steps(app, "classic", DEFAULT_PROJ_CLASSIC)


@pytest.fixture(scope="function")
def app(page: Page) -> Application:
    return Application(page)


@pytest.fixture(scope="function")
def create_multiple_projects(app: Application, configs, remove_test_projects):
    (app.projects_page.is_loaded()
     .open_company_projects(DEFAULT_COMPANY)
     .click_create_project())
    do_create_project_steps(app, "classic", DEFAULT_PROJ_CLASSIC)
    app.projects_page.click_create_project()
    do_create_project_steps(app, "bdd", DEFAULT_PROJ_BDD)


@pytest.fixture(scope="session")
def browser_type_launch_args(browser_type_launch_args: dict) -> dict:
    return {
        **browser_type_launch_args,
        "channel": "chrome",
        "headless": False,
        "slow_mo": 150,  # interval between actions
        "timeout": 10000,  # maximal timeout for each test
    }


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args, playwright):
    return {
        **browser_context_args,
        "base_url": "https://app.testomat.io",
        "viewport": {"width": 1440, "height": 900},
        "device_scale_factor": 1,
        "locale": "uk-UA",
        "timezone_id": "Europe/Kyiv",
        "record_video_dir": "videos/",
        "permissions": ["geolocation"]
    }


def delete_multiple_projects(app: Application, company_name: str, project_name: str):
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
