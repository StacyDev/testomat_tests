from playwright.sync_api import Page, expect


class CreateProjectPage:
    def __init__(self, page: Page):
        self.page = page
        self.loc_bdd_rbtn = self.page.locator("#bdd-help-text")
        self.loc_classic_rbtn = self.page.locator("#classical-help-text")
        self.loc_create_btn = self.page.locator("[value='Create']")
        self.loc_proj_name_inp = self.page.locator("input#project_title")

    def is_loaded(self):
        expect(self.loc_proj_name_inp).to_be_visible()

    def create_project(self, project_type: str, project_name: str):
        if project_type == "classic":
            self.loc_classic_rbtn.click()
        elif project_type == "bdd":
            self.loc_bdd_rbtn.click()
        self.loc_proj_name_inp.type(project_name)
        self.loc_create_btn.click()
