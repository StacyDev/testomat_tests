import pytest
from faker import Faker
from playwright.sync_api import expect

from src.web.application import Application
from tests.fixtures.infrastructure_handler import DEFAULT_COMPANY


@pytest.mark.regression
@pytest.mark.smoke
def test_new_page_elements(logged_app: Application):
    (logged_app.create_project_page.open().is_loaded())


@pytest.mark.regression
def test_new_project_creation(
    logged_app: Application, remove_test_projects, remove_non_default_test_projects: list
):
    project_name = Faker().company()
    remove_non_default_test_projects.append(project_name)
    app = logged_app

    (app.projects_page.is_loaded().open_company_projects(DEFAULT_COMPANY).click_create_project())

    (
        app.create_project_page.open()
        .is_loaded()
        .set_project_type("classic")
        .fill_project_name(project_name)
        .click_submit_btn()
    )

    (app.single_project_page.is_loaded())

    expect(app.single_project_page.get_empty_project_title_locator()).to_be_visible()

    app.single_project_page.return_to_projects_list()

    expect(
        app.projects_page.get_project_list_locator().filter(has_text=project_name)
    ).to_be_visible()
