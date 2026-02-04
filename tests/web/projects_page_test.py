import pytest
from playwright.sync_api import expect

from src.web.Application import Application
from tests.conftest import DEFAULT_PROJ_CLASSIC, DEFAULT_COMPANY, DEFAULT_PROJ_BDD


@pytest.mark.regression
def test_creating_classic_project(app: Application, remove_test_projects):
    # arrange
    (app.projects_page
     .is_loaded()
     .open_company_projects(DEFAULT_COMPANY)
     .is_project_list_loaded())

    projects_num_before = len(app.projects_page.get_all_projects_list())

    app.projects_page.click_create_project()

    # act
    project_name = DEFAULT_PROJ_CLASSIC

    (app.create_project_page
     .is_loaded()
     .create_project("classic", project_name))

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
def test_creating_bdd_project(app: Application, remove_test_projects):
    (app.projects_page
     .is_loaded()
     .open_company_projects(DEFAULT_COMPANY)
     .is_project_list_loaded())

    projects_num_before = len(app.projects_page.get_all_projects_list())

    project_name = DEFAULT_PROJ_BDD
    app.projects_page.click_create_project()

    (app.create_project_page
     .is_loaded()
     .create_project("bdd", project_name))

    app.single_project_page.is_loaded()
    expect(app.single_project_page.get_project_title_locator()).to_have_text(project_name)
    app.single_project_page.return_to_projects_list()

    project_num_after = (app.projects_page
                         .is_loaded()
                         .get_project_list_locator())
    expect(project_num_after).to_have_count(projects_num_before + 1)


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


@pytest.mark.regression
def test_project_search(app: Application, create_multiple_projects):
    (app.projects_page
     .is_loaded()
     .is_project_list_loaded()
     .search_project(DEFAULT_PROJ_CLASSIC))

    expect(app.projects_page.get_project_list_locator().filter(visible=True)).to_have_count(1)
    expect(app.projects_page.get_project_list_locator().filter(visible=True)).to_have_text(
        DEFAULT_PROJ_CLASSIC)


@pytest.mark.regression
@pytest.mark.smoke
def test_project_search_part_name(app: Application, create_multiple_projects):
    (app.projects_page
     .is_loaded()
     .is_project_list_loaded()
     .search_project(str.capitalize("BD")))

    expect(app.projects_page.get_project_list_locator().filter(visible=True)).to_have_count(1)
    expect(app.projects_page.get_project_list_locator().filter(visible=True)).to_have_text(
        DEFAULT_PROJ_BDD)
