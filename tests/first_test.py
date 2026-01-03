import os

from faker import Faker
from playwright.sync_api import Page, expect



def test_creating_classic_project(page: Page, configs):
    page.goto(configs.base_app_url)
    login(page, configs.email, configs.password)

    open_company_projects(page, "Free Projects")
    project_name = "Classic Project1"
    create_project(page, "classic", project_name)

    expect(page.locator(".sticky-header h2")).to_have_text(project_name)
    expect(page.locator("#welcometotestomatio")).to_have_text("Welcome to Testomat.io")


def test_creating_bdd_project(page: Page, configs):
    # arrange
    page.goto(configs.base_app_url)
    login(page, configs.email, configs.password)

    # act
    open_company_projects(page, "Free Projects")
    project_name = "BDD Project1"
    create_project(page, "bdd", project_name)

    # assert
    expect(page.locator(".sticky-header h2")).to_have_text(project_name)
    expect(page.locator("#welcometotestomatio")).to_have_text("Welcome to Testomat.io")


def test_login_valid_creds(page: Page, configs):
    # arrange
    open_login_page(page, configs)

    # act
    login(page, configs.email, configs.password)

    # assert
    expect(page.locator(".common-flash-success-right")).to_have_text('Signed in successfully')

def test_login_invalid_creds(page: Page, configs):
    # arrange
    open_login_page(page, configs)

    # act
    invalid_password=Faker().password(length=10)
    print(invalid_password)
    login(page, configs.email, invalid_password)

    # assert
    expect(page.locator("#content-desktop").get_by_text('Invalid Email or password.', exact=False)).to_be_visible()

def test_opening_project_python_manufacture(page: Page, configs):
    page.goto(configs.base_app_url)
    login(page, configs.email, configs.password)

    target_project: str = "python manufacture"
    search_project(page, target_project)
    open_project(page, target_project)

    expect(page.locator(".breadcrumbs-page-second-level", has_text="Tests")).to_be_visible()


def test_opening_company_free_projects(page: Page, configs):
    # arrange
    page.goto(f"{os.getenv("BASE_APP_URL")}")
    login(page, configs.email, configs.password)

    # act
    companies_list = page.locator("select#company_id")
    expect(companies_list).to_be_visible()
    companies_list.click()
    companies_list.select_option("Free Projects")

    # assert
    target_project: str = "python manufacture"
    search_project(page, target_project)

    project_locator = page.locator("ul li h3", has_text=target_project)
    expect(project_locator).to_be_hidden()

    expect(page.get_by_text("Enterprise trial plan", exact=False)).to_be_visible()


def create_project(page: Page, project_type: str, project_name: str):
    page.locator(".common-btn-primary", has_not_text="project").click()
    if project_type == "classic":
        page.click("#classical-help-text")
    elif project_type == "bdd":
        page.click("#bdd-help-text")
    page.type("#project_title", project_name)
    page.click("[value='Create']")


def open_project(page: Page, target_proj_name: str):
    project_locator = page.locator("ul li h3", has_text=target_proj_name)
    expect(project_locator).to_be_visible()
    project_locator.click()


def search_project(page: Page, target_project: str):
    search_locator = page.locator("#content-desktop input#search")
    expect(search_locator).to_be_visible()
    search_locator.type(target_project)


def login(page: Page, email: str, password: str):
    page.get_by_role("textbox",
                     name="name@email.com").type(email)
    page.locator("#content-desktop input#user_password").type(password)
    page.click("#content-desktop input[type='submit']")


def open_login_page(page: Page, configs: dict):
    page.goto(configs.base_url)
    page.click(".login-item[href*='sign_in']")


def open_company_projects(page: Page, target_company: str):
    companies_list = page.locator("select#company_id")
    expect(companies_list).to_be_visible()
    companies_list.click()
    companies_list.select_option(target_company)
