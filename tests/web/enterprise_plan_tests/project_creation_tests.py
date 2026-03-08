import pytest
from playwright.sync_api import expect

from src.api.testomat_api_client import ApiClient
from src.web.application import Application


@pytest.mark.regression
def test_opening_project(project_context: ApiClient, logged_app: Application) -> None:
    all_projects = project_context.get_projects()
    target_project_id = all_projects[1].id
    target_project_title = all_projects[1].title

    logged_app.single_project_page.open_by_id(target_project_id)
    logged_app.single_project_page.is_loaded()

    expect(logged_app.single_project_page.get_project_title_locator()).to_contain_text(
        target_project_title
    )
