from typing import Self

from playwright.sync_api import Page, expect

from src.web.pages.SingleProjectPage import SingleProjectPage


class CreateProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self._loc_form_container = self.page.locator("#content-desktop .new_project")
        self._loc_bdd_rbtn = self._loc_form_container.locator("#bdd")
        self._loc_classic_rbtn = self._loc_form_container.locator("#classical")
        self._loc_proj_name_inp = self._loc_form_container.locator("input#project_title")
        self._loc_create_btn = self._loc_form_container.locator("input[type='submit']")
        self._loc_how_to_btn = self.page.get_by_text("How to start?")
        self._loc_demo_data_cbox = self.page.locator("#content-desktop #demo-btn")
        self._loc_demo_data_lbl = self.page.locator("#content-desktop label[for='demo-btn']")
        self._loc_title_lbl = self.page.locator("#content-desktop h2")

    def is_loaded(self) -> Self:
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
        return self

    def create_project(self, project_type: str, project_name: str) -> Self:
        self.set_project_type(project_type)
        self.fill_project_name(project_name)
        self.click_submit_btn()
        return self

    def set_project_type(self, project_type: str) -> Self:
        if project_type == "classic":
            self._loc_classic_rbtn.click()
        elif project_type == "bdd":
            self._loc_bdd_rbtn.click()
        return self

    def open(self) -> Self:
        self.page.goto("/projects/new")
        return self

    def fill_project_name(self, project_name: str) -> Self:
        self._loc_proj_name_inp.fill(project_name)
        return self

    def click_submit_btn(self)  -> Self:
        self._loc_create_btn.click()

        expect(self._loc_create_btn).to_be_hidden(timeout=10000)

        return self
