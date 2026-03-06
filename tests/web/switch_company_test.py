import pytest
from playwright.sync_api import expect

from src.web.application import Application
from tests.fixtures.infrastructure_handler import DEFAULT_COMPANY


@pytest.mark.smoke
def test_project_page_header(remove_test_projects, logged_app: Application):
    proj_page = logged_app.projects_page.is_loaded().open_company_projects(DEFAULT_COMPANY)

    expect(proj_page.get_free_plan_label_locator()).to_be_visible()
    proj_page.get_free_plan_label_locator().hover(timeout=500)
    expect(proj_page.get_tooltip_locator()).to_be_visible()
    expect(proj_page.get_tooltip_locator()).to_contain_text("You have a free subscription")
