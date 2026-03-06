from __future__ import annotations

from enum import Enum

from playwright.sync_api import Page, expect


class CreateProjectPage:
    class DemoData(Enum):
        CODECEPT = "CodeceptJS Demo Project"
        CUCUMBER = "CucumberJS Demo Project"
        CYPRESS = "Cypress Demo Project"
        JEST = "Jest Demo Project"
        TESTCAFE = "TestCafe Demo Project"
        WEBDRIVER = "Webdriverio Demo Project"
        PROTRACTOR = "Protractor Demo"
        CODECEPTION = "Codeception Demo"

    def __init__(self, page: Page):
        self.page = page

        self._loc_form_container = self.page.locator("#content-desktop .new_project")
        self._loc_bdd_rbtn = self._loc_form_container.locator("#bdd")
        self._loc_classic_rbtn = self._loc_form_container.locator("#classical")
        self._loc_title_lbl = self.page.locator("#content-desktop h2")
        self._loc_proj_name_inp = self._loc_form_container.locator("input#project_title")
        self._loc_create_btn = self._loc_form_container.locator("input[type='submit']")
        self._loc_how_to_btn = self.page.get_by_text("How to start?")
        self._loc_demo_data_cbox = self.page.locator("#content-desktop #demo-btn")
        self._loc_demo_data_lbl = self.page.locator("#content-desktop label[for='demo-btn']")

        self._loc_demo_form = self.page.locator("div#demo-form")

        self._loc_btn_create_demo = self._loc_demo_form.get_by_role("button", name="Create Demo")

    def is_loaded(self) -> CreateProjectPage:  # noqa: F821
        expect(self._loc_form_container).to_be_visible()
        expect(self._loc_bdd_rbtn).to_contain_text("BDD")
        expect(self._loc_classic_rbtn).to_contain_text("Classical")
        expect(self._loc_create_btn).to_be_visible()
        expect(self._loc_proj_name_inp).to_be_visible()
        expect(self._loc_how_to_btn).to_be_visible()
        expect(self._loc_demo_data_cbox).to_be_visible()
        expect(self._loc_demo_data_lbl).to_be_visible()
        expect(self._loc_title_lbl).to_be_visible()
        expect(self._loc_title_lbl).to_have_text("New Project")
        expect(self._loc_demo_data_cbox).not_to_be_checked(timeout=10000)
        expect(self._loc_demo_form).to_be_hidden()
        return self

    def check_demo_data(self) -> CreateProjectPage:  # noqa: F821
        expect(self._loc_demo_data_cbox).not_to_be_checked(timeout=10000)
        self._loc_demo_data_cbox.click()
        expect(self._loc_demo_form).to_be_visible()

        for option in self.DemoData:
            expect(self._loc_demo_form.get_by_role("button", name=option.value)).to_be_visible()
        return self

    def uncheck_demo_data(self) -> CreateProjectPage:  # noqa: F821
        expect(self._loc_demo_data_cbox).to_be_unchecked(timeout=10000)
        self._loc_demo_data_cbox.click()
        expect(self._loc_demo_form).to_be_hidden()

        for option in self.DemoData:
            expect(self._loc_demo_form.get_by_role("button", name=option.value)).to_be_hidden()
        return self

    def set_project_type(self, project_type: str) -> CreateProjectPage:  # noqa: F821
        if project_type == "classic":
            self._loc_classic_rbtn.click()
        elif project_type == "bdd":
            self._loc_bdd_rbtn.click()
        return self

    def open(self) -> CreateProjectPage:  # noqa: F821
        self.page.goto("/projects/new")
        return self

    def fill_project_name(self, project_name: str) -> CreateProjectPage:  # noqa: F821
        self._loc_proj_name_inp.fill(project_name)
        return self

    def click_submit_btn(self):
        self._loc_create_btn.click()
        expect(self._loc_create_btn).to_be_hidden(timeout=10000)

    def create_project(self, project_type: str, project_name: str):
        self.set_project_type(project_type)
        self.fill_project_name(project_name)
        self.click_submit_btn()

    def create_project_with_demo_data(
        self, project_type: str, project_name: str, demo_data: DemoData
    ):
        self.set_project_type(project_type)
        self.fill_project_name(project_name)
        self.check_demo_data()
        self.pick_demo_data(demo_data)
        self.click_submit_btn()

    # noqa: F821
    def pick_demo_data(self, demo_option: DemoData) -> CreateProjectPage:
        self._loc_demo_form.get_by_role("button", name=demo_option.value).click()
        return self
