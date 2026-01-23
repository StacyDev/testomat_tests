from playwright.sync_api import Page

from src.web.pages.CreateProjectPage import CreateProjectPage
from src.web.pages.HomePage import HomePage
from src.web.pages.LoginPage import LoginPage
from src.web.pages.ProjectsPage import ProjectsPage
from src.web.pages.SingleProjectPage import SingleProjectPage


class Application:

    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(self.page)
        self.login_page = LoginPage(self.page)
        self.projects_page = ProjectsPage(self.page)
        self.create_project_page = CreateProjectPage(self.page)
        self.single_project_page = SingleProjectPage(self.page)
