import pytest
from playwright.sync_api import expect

from src.web.application import Application


@pytest.mark.regression
def test_project_page_header(free_project_app: Application):
    app: Application = free_project_app

    expect(app.projects_page.get_free_plan_label_locator()).to_be_visible()
    # assert not app.projects_page.has_projects()
    app.projects_page.get_free_plan_label_locator().hover(timeout=500)
    expect(app.projects_page.get_tooltip_locator()).to_be_visible()
    expect(app.projects_page.get_tooltip_locator()).to_contain_text("You have a free subscription")
