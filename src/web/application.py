from playwright.sync_api import Page

from src.web.pages.create_project_page import CreateProjectPage
from src.web.pages.home_page import HomePage
from src.web.pages.login_page import LoginPage
from src.web.pages.projects_page import ProjectsPage
from src.web.pages.single_project_page import SingleProjectPage


class Application:
    def __init__(self, page: Page):
        self.page = page
        self.home_page = HomePage(self.page)
        self.login_page = LoginPage(self.page)
        self.projects_page = ProjectsPage(self.page)
        self.create_project_page = CreateProjectPage(self.page)
        self.single_project_page = SingleProjectPage(self.page)
