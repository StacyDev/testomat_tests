from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from src.web.selenium.core.driver_actions import DriverActions
from src.web.selenium.core.element_actions import ElementActions


class ProjectsPageSelenium:
    def __init__(self, driver_actions: DriverActions, element_actions: ElementActions):
        self.driver_actions = driver_actions
        self.element_actions = element_actions

        self._loc_comp_select: tuple[By | str, str] = (
            By.CSS_SELECTOR,
            "#content-desktop select#company_id",
        )
        self._loc_login_ok_msg: tuple[By | str, str] = (
            By.CSS_SELECTOR,
            "#content-desktop .common-flash-success-right",
        )

        self._loc_enterprise_plan_lbl = (
            By.XPATH,
            "//*[@id='content-desktop']//span[contains(., 'Enterprise plan')]",
        )
        self._loc_plan_tippy_ttip = (By.CSS_SELECTOR, "[data-tippy-root]")

        self._loc_free_plan_lbl = (
            By.XPATH,
            "//*[@id='content-desktop']//span[contains(., 'Free Plan')]",
        )
        self._loc_proj_wrapper = (By.CSS_SELECTOR, "ul>li>a")

        self._loc_no_proj_img = (By.CSS_SELECTOR, ".m-auto[src*='no-project']")
        self._loc_proj_wrapper_grid = (By.CSS_SELECTOR, ".tab-content#grid")

        self._loc_create_proj_btn = (
            By.CSS_SELECTOR,
            ".common-page-header-right [href='/projects/new']",
        )
        self._loc_search_inp = (By.CSS_SELECTOR, "#content-desktop input#search")

    def is_loaded(self) -> ProjectsPageSelenium:
        self.element_actions.wait.for_visible(self._loc_comp_select)
        return self

    def is_login_ok_msg_visible(self) -> ProjectsPageSelenium:
        self.element_actions.wait.for_visible(self._loc_login_ok_msg)

    def get_enterprise_plan_label(self) -> WebElement:
        return self.element_actions.wait.for_visible(self._loc_enterprise_plan_lbl)

    def get_free_plan_label(self) -> WebElement:
        return self.element_actions.wait.for_visible(self._loc_free_plan_lbl)

    def get_tooltip(self) -> WebElement:
        return self.element_actions.wait.for_visible(self._loc_plan_tippy_ttip)

    def is_project_list_loaded(self) -> ProjectsPageSelenium:
        if self.has_projects():
            self.element_actions.wait.for_visible(self._loc_proj_wrapper_grid)
        return self

    def open_company_projects(self, target_company: str) -> ProjectsPageSelenium:
        self.element_actions.select_value(self._loc_comp_select, target_company)
        self.is_project_list_loaded()
        return self

    def click_create_project(self):
        self.element_actions.click(self._loc_create_proj_btn)

    def enter_project(self, project_name: str) -> ProjectsPageSelenium:
        loc_project = (By.CSS_SELECTOR, f'[title="{project_name}"]')
        projects = self.element_actions.wait.for_all_present(loc_project)
        projects[0].click()
        return self

    def search_project(self, project_name: str) -> ProjectsPageSelenium:
        self.element_actions.type_text(self._loc_search_inp, project_name)
        return self

    def get_projects_list_by_name(self, project_name) -> list[Locator]:
        loc_project = (By.CSS_SELECTOR, f'[title="{project_name}"]')
        return self.element_actions.wait.for_all_present(loc_project)

    def get_all_projects_list(self) -> list[Locator]:
        return self.element_actions.wait.for_all_present(self._loc_proj_wrapper)

    def has_projects(self) -> bool:
        try:
            self.element_actions.wait.for_visible(self._loc_no_proj_img, 3)
            return False

        except TimeoutException:
            return True

    def get_project_list_locator(self) -> Locator:
        return self._loc_proj_wrapper

    def verify_found_project_titles_correct(self, search_term: str):
        self.element_actions.wait.until(lambda driver: self._check_content(search_term))
        return self

    def _check_content(self, search_term: str):
        visible_elements = [
            el
            for el in self.element_actions.wait.find_now(self._loc_proj_wrapper)
            if el.is_displayed()
        ]

        for el in visible_elements:
            title = str(el.get_attribute("title")).lower()
            if search_term.lower() not in title:
                return False

        return len(visible_elements) > 0
