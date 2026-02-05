from re import search

import pytest
from playwright.sync_api import expect

from src.web.Application import Application
from tests.conftest import DEFAULT_PROJ_CLASSIC, DEFAULT_COMPANY, DEFAULT_PROJ_BDD, \
    remove_test_projects

create_project_data = [
    pytest.param(DEFAULT_COMPANY, DEFAULT_PROJ_CLASSIC, "classic", id="create_classic_project"),
    pytest.param(DEFAULT_COMPANY, DEFAULT_PROJ_BDD, "bdd", id="create_bdd_project")
]


@pytest.mark.regression
@pytest.mark.parametrize("company, project_name, project_type", create_project_data)
def test_creating_project(app: Application, remove_test_projects, company, project_name,
                          project_type):
    # arrange
    (app.projects_page
     .is_loaded()
     .open_company_projects(company)
     .is_project_list_loaded())

    projects_num_before = len(app.projects_page.get_all_projects_list())

    app.projects_page.click_create_project()

    # act
    (app.create_project_page
     .is_loaded()
     .create_project(project_type, project_name))

    # assert
    (app.single_project_page
     .is_loaded()
     .return_to_projects_list())

    projects_lst_after = (app.projects_page
                          .is_loaded()
                          .is_project_list_loaded()
                          .get_project_list_locator())

    expect(projects_lst_after).to_have_count(projects_num_before + 1)


@pytest.mark.regression
def test_deleting_project(app: Application, create_test_project):
    (app.projects_page
     .is_loaded()
     .open_company_projects(DEFAULT_COMPANY))

    projects_num_before = len(app.projects_page.get_all_projects_list())

    app.projects_page.enter_project(DEFAULT_PROJ_CLASSIC)

    (app.single_project_page
     .is_loaded()
     .open_project_settings()
     .trigger_and_confirm_project_delete()
     .return_to_projects_list())

    expect(app.projects_page.get_project_list_locator()).to_have_count(projects_num_before - 1)


search_project_data = [
    pytest.param(DEFAULT_PROJ_CLASSIC, DEFAULT_PROJ_CLASSIC, id="search_project_by_full_name"),
    pytest.param("BD",DEFAULT_PROJ_BDD, id="search_project_by_first_two_characters_upper_case")
]


@pytest.mark.regression
@pytest.mark.parametrize("search_value, expected_project_name", search_project_data)
def test_project_search(app: Application, create_multiple_projects, search_value, expected_project_name):
    (app.projects_page
     .is_loaded()
     .is_project_list_loaded()
     .search_project(search_value))

    expect(app.projects_page.get_project_list_locator().filter(visible=True)).to_have_count(1)
    expect(app.projects_page.get_project_list_locator().filter(visible=True)).to_have_text(
        expected_project_name)

