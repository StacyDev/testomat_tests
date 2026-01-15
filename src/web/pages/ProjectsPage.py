from playwright.sync_api import Page, expect, Locator, TimeoutError


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self.loc_proj_lst = self.page.locator("ul li h3")
        self.loc_comp_select = self.page.locator("#content-desktop select#company_id")
        self.loc_no_proj_lbl = self.page.get_by_text("You have not created any projects yet")
        self.loc_proj_lst_grid = self.page.locator("#grid")
        self.loc_login_ok_msg = self.page.locator(".common-flash-success-right", has_text="Signed in successfully")
        self.loc_create_proj_btn = self.page.locator(".common-btn-primary", has_not_text="project")
        self.loc_search_inp = self.page.locator("#content-desktop input#search")

    def is_loaded(self):
        expect(self.loc_comp_select).to_be_visible()

    def is_project_list_loaded(self):
        if self.has_projects():
            expect(self.loc_proj_lst_grid).to_be_visible()

    def has_projects(self) -> bool:
        try:
            locator = self.loc_no_proj_lbl
            locator.wait_for(state="visible", timeout=1000)
            return False

        except TimeoutError:
            return True

    def is_signin_success_msg_visible(self):
        expect(self.loc_login_ok_msg).to_be_visible()

    def open_company_projects(self, target_company: str):
        companies_list = self.loc_comp_select
        expect(self.loc_comp_select).to_be_visible()
        companies_list.click()
        companies_list.select_option(target_company)
        self.is_project_list_loaded()

    def click_create_project(self):
        self.loc_create_proj_btn.click()

    def enter_project(self, project_name: str):
        item = self.loc_proj_lst.filter(has_text=project_name).first
        item.click()

    def get_projects_list_by_name(self, project_name) -> list[Locator]:
        return self.loc_proj_lst.filter(has_text=project_name).all()

    def get_all_projects_list(self) -> list[Locator]:
        return self.loc_proj_lst.all()

    def search_project(self, project_name: str):

        expect(self.loc_search_inp).to_be_visible()
        self.loc_search_inp.type(project_name)

    def is_login_ok_msg_visible(self):
        expect(self.loc_login_ok_msg).to_be_visible()
