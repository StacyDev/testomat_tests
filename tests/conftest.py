import os
from dataclasses import dataclass

import pytest
from dotenv import load_dotenv
from playwright.sync_api import Page, Locator

from src.web.pages.ProjectsPage import ProjectsPage
from src.web.pages.CreateProjectPage import CreateProjectPage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.SingleProjectPage import SingleProjectPage

load_dotenv()



@dataclass(frozen=True)
class Config:
    base_url: str
    base_app_url: str
    email: str
    password: str

DEFAULT_PROJ_CLASSIC = "Stacy Classic Project1"
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
def login(page: Page, configs):
    do_login_steps(page, configs)


@pytest.fixture(scope="function")
def remove_test_projects(page: Page, configs):
    do_login_steps(page, configs)
    delete_multiple_projects(page, DEFAULT_COMPANY, DEFAULT_PROJ_CLASSIC)
    delete_multiple_projects(page, DEFAULT_COMPANY, DEFAULT_PROJ_BDD)


@pytest.fixture(scope="function")
def create_test_project(page: Page, configs, remove_test_projects):
    projects_page: ProjectsPage = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.open_company_projects(DEFAULT_COMPANY)
    projects_page.click_create_project()
    do_create_project_steps(page, "classic", DEFAULT_PROJ_CLASSIC)


@pytest.fixture(scope="function")
def create_multiple_projects(page: Page, configs, remove_test_projects):
    projects_page: ProjectsPage = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.open_company_projects(DEFAULT_COMPANY)
    projects_page.click_create_project()
    do_create_project_steps(page, "classic", DEFAULT_PROJ_CLASSIC)
    projects_page.click_create_project()
    do_create_project_steps(page, "bdd", DEFAULT_PROJ_BDD)


def delete_multiple_projects(page: Page, company_name: str, project_name: str):
    projects_page: ProjectsPage = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.open_company_projects(company_name)
    project_items: list[Locator] = projects_page.get_projects_list_by_name(project_name)

    while len(project_items) > 0:
        project_items[0].click()

        single_project_page: SingleProjectPage = SingleProjectPage(page, project_name)
        single_project_page.is_loaded()
        single_project_page.open_project_settings()
        single_project_page.trigger_and_confirm_project_delete()
        single_project_page.return_to_projects_list()
        projects_page.is_loaded()
        project_items = projects_page.get_projects_list_by_name(project_name)


def do_login_steps(page: Page, configs: Config):
    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)


def do_create_project_steps(page: Page, proj_type: str, project_name: str):
    create_project_page = CreateProjectPage(page)
    create_project_page.is_loaded()
    create_project_page.create_project(proj_type, project_name)
    single_project_page = SingleProjectPage(page, project_name)
    single_project_page.is_loaded()
    single_project_page.return_to_projects_list()
