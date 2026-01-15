from faker import Faker
from playwright.sync_api import Page

from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectsPage import ProjectsPage
from tests.conftest import Config


def test_login_invalid(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.open_login_page_by_click()

    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    invalid_password = Faker().password(length=10)
    login_page.login(configs.email, invalid_password)
    login_page.is_invalid_message_visible()

def test_login_success(page: Page, configs: Config):
    home_page = HomePage(page)
    home_page.open()
    home_page.is_loaded()
    home_page.open_login_page_by_click()

    login_page = LoginPage(page)
    login_page.open()
    login_page.is_loaded()
    login_page.login(configs.email, configs.password)
    projects_page = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.is_login_ok_msg_visible()
