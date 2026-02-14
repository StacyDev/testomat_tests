from typing import Generator

import pytest
from playwright.sync_api import Locator

from src.web.application import Application
from tests.fixtures.config import Config

DEFAULT_PROJ_CLASSIC = "Classic Project1"
DEFAULT_PROJ_BDD = "BDD Project1"
DEFAULT_COMPANY = "Free Projects"


@pytest.fixture(scope="function")
def remove_test_projects(logged_app: Application):
    app = logged_app
    delete_multiple_projects(app, DEFAULT_COMPANY, DEFAULT_PROJ_CLASSIC)
    delete_multiple_projects(app, DEFAULT_COMPANY, DEFAULT_PROJ_BDD)


@pytest.fixture
def remove_non_default_test_projects(logged_app: Application) -> Generator[list, None, None]:
    project_container: list = []

    yield project_container

    if project_container:
        project_name = project_container[0]
        delete_multiple_projects(logged_app, DEFAULT_COMPANY, project_name)


@pytest.fixture(scope="function")
def create_test_project(logged_app: Application, remove_test_projects):
    app = logged_app
    (app.projects_page.is_loaded().open_company_projects(DEFAULT_COMPANY).click_create_project())
    do_create_project_steps(app, "classic", DEFAULT_PROJ_CLASSIC)


@pytest.fixture(scope="function")
def create_multiple_projects(logged_app: Application, remove_test_projects):
    app = logged_app
    (app.projects_page.is_loaded().open_company_projects(DEFAULT_COMPANY).click_create_project())
    do_create_project_steps(app, "classic", DEFAULT_PROJ_CLASSIC)
    app.projects_page.click_create_project()
    do_create_project_steps(app, "bdd", DEFAULT_PROJ_BDD)


def delete_multiple_projects(logged_app: Application, company_name: str, project_name: str):
    app = logged_app
    (app.projects_page.is_loaded().open_company_projects(company_name))
    project_items: list[Locator] = app.projects_page.get_projects_list_by_name(project_name)

    while len(project_items) > 0:
        project_items[0].click()

        (
            app.single_project_page.is_loaded()
            .open_project_settings()
            .trigger_and_confirm_project_delete()
            .return_to_projects_list()
        )

        project_items = app.projects_page.is_loaded().get_projects_list_by_name(project_name)


def do_login_steps(app: Application, configs: Config):
    (app.login_page.open().is_loaded().login(configs.email, configs.password))


def do_create_project_steps(app: Application, proj_type: str, project_name):
    (app.create_project_page.is_loaded().create_project(proj_type, project_name))
    (app.single_project_page.is_loaded().return_to_projects_list())
