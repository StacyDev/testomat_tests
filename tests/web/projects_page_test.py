from playwright.sync_api import Page, expect

from src.web.pages.CreateProjectPage import CreateProjectPage
from src.web.pages.ProjectsPage import ProjectsPage
from src.web.pages.SingleProjectPage import SingleProjectPage
from tests.conftest import DEFAULT_PROJ_CLASSIC, DEFAULT_COMPANY, DEFAULT_PROJ_BDD


def test_creating_classic_project(page: Page, remove_test_projects):
    projects_page = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.open_company_projects(DEFAULT_COMPANY)
    expect(projects_page.loc_proj_lst).to_have_count(0)
    project_name = DEFAULT_PROJ_CLASSIC
    projects_page.click_create_project()

    create_project_page = CreateProjectPage(page)
    create_project_page.is_loaded()
    create_project_page.create_project("classic", project_name)

    expect(page.locator(".sticky-header h2", has_text=project_name)).to_be_visible()
    single_project_page = SingleProjectPage(page, project_name)
    single_project_page.is_loaded()
    single_project_page.return_to_projects_list()
    projects_page.is_loaded()
    expect(projects_page.loc_proj_lst).to_have_count(1)


def test_creating_bdd_project(page: Page, remove_test_projects):
    projects_page = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.open_company_projects(DEFAULT_COMPANY)

    print(f"Number of projects {len(projects_page.get_all_projects_list())}")
    expect(projects_page.loc_proj_lst).to_have_count(0)
    project_name = DEFAULT_PROJ_BDD
    projects_page.click_create_project()

    create_project_page = CreateProjectPage(page)
    create_project_page.is_loaded()
    create_project_page.create_project("bdd", project_name)

    expect(page.locator(".sticky-header h2", has_text=project_name)).to_be_visible()
    single_project_page = SingleProjectPage(page, project_name)
    single_project_page.is_loaded()
    single_project_page.return_to_projects_list()
    projects_page.is_loaded()
    expect(projects_page.loc_proj_lst).to_have_count(1)


def test_deleting_project(page: Page, create_test_project):
    projects_page = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.open_company_projects(DEFAULT_COMPANY)
    projects_page.enter_project(DEFAULT_PROJ_CLASSIC)
    single_project_page = SingleProjectPage(page, DEFAULT_PROJ_CLASSIC)
    single_project_page.is_loaded()
    single_project_page.open_project_settings()
    single_project_page.trigger_and_confirm_project_delete()
    single_project_page.return_to_projects_list()

    expect(projects_page.loc_proj_lst).to_have_count(0)


def test_project_search(page: Page, create_multiple_projects):
    projects_page = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.is_project_list_loaded()
    projects_page.search_project(DEFAULT_PROJ_CLASSIC)

    expect(projects_page.loc_proj_lst.filter(visible=True)).to_have_count(1)
    expect(projects_page.loc_proj_lst.filter(visible=True)).to_have_text(DEFAULT_PROJ_CLASSIC)


def test_project_search_part_name(page: Page, create_multiple_projects):
    projects_page = ProjectsPage(page)
    projects_page.is_loaded()
    projects_page.is_project_list_loaded()
    projects_page.search_project(str.capitalize("BD"))

    expect(projects_page.loc_proj_lst.filter(visible=True)).to_have_count(1)
    expect(projects_page.loc_proj_lst.filter(visible=True)).to_have_text(DEFAULT_PROJ_BDD)
