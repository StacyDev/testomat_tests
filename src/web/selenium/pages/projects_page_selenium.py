from selenium.webdriver.common.by import By

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

    def is_loaded(self) -> ProjectsProjectPage:
        self.element_actions.wait.for_visible(self._loc_comp_select)
        return self

    def is_login_ok_msg_visible(self) -> ProjectsProjectPage:
        self.element_actions.wait.for_visible(self._loc_login_ok_msg)
