from faker import Faker
from playwright.sync_api import Page

from src.web.pages.CreateProjectPage import CreateProjectPage
from src.web.pages.CreateProjectPageAI import CreateProjectPageAI
from src.web.pages.SingleProjectPage import SingleProjectPage


def test_new_page_elements(page: Page, login):
    create_project_page = CreateProjectPage(page)
    create_project_page.open()
    create_project_page.is_loaded()


def test_new_page_elements_ai(page: Page, login):
    create_project_page = CreateProjectPageAI(page)
    create_project_page.open()
    create_project_page.is_loaded()


def test_new_project_creation(page: Page, login):
    project_name = Faker().company()

    (CreateProjectPage(page)
     .open()
     .is_loaded()
     .set_project_type("classic")
     .fill_project_name(project_name)
     .click_submit_btn())

    SingleProjectPage(page, project_name).is_loaded()
