from src.web.selenium.pages.login_page_selenium import LoginPageSelenium
from src.web.selenium.pages.projects_page_selenium import ProjectsPageSelenium


class SeleniumApplication:
    def __init__(self, element_actions, driver_actions):
        self.login_page = LoginPageSelenium(driver_actions, element_actions)
        self.projects_page = ProjectsPageSelenium(driver_actions, element_actions)
