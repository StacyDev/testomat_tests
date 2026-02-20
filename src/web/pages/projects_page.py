from playwright.sync_api import Locator, Page, TimeoutError, expect


class ProjectsPage:
    def __init__(self, page: Page):
        self.page = page
        self._loc_enterprise_plan_lbl = self.page.get_by_text("Enterprise Plan")
        self._loc_plan_tippy_ttip = self.page.locator("[data-tippy-root]")
        self._loc_free_plan_lbl = self.page.get_by_text("Free Plan")
        self._loc_proj_wrapper = self.page.locator("ul li h3")
        self._loc_comp_select = self.page.locator("#content-desktop select#company_id")
        self._loc_no_proj_lbl = self.page.get_by_text("You have not created any projects yet")
        self._loc_proj_wrapper_grid = self.page.locator(".tab-content#grid")
        self._loc_login_ok_msg = self.page.locator(
            ".common-flash-success-right", has_text="Signed in successfully"
        )
        self._loc_create_proj_btn = self.page.locator(".common-btn-primary", has_not_text="project")
        self._loc_search_inp = self.page.locator("#content-desktop input#search")

    def get_enterprise_plan_label_locator(self) -> Locator:
        return self._loc_enterprise_plan_lbl

    def get_free_plan_label_locator(self) -> Locator:
        return self._loc_free_plan_lbl

    def get_tooltip_locator(self) -> Locator:
        return self._loc_plan_tippy_ttip

    def is_loaded(self) -> ProjectsPage:
        expect(self._loc_comp_select).to_be_visible()
        return self

    def is_project_list_loaded(self) -> ProjectsPage:
        if self.has_projects():
            expect(self._loc_proj_wrapper_grid).to_be_visible()
        return self

    def is_signin_success_msg_visible(self) -> ProjectsPage:
        expect(self._loc_login_ok_msg).to_be_visible()
        return self

    def open_company_projects(self, target_company: str) -> ProjectsPage:
        companies_list = self._loc_comp_select
        expect(self._loc_comp_select).to_be_visible()
        companies_list.click()
        companies_list.select_option(target_company)
        self.is_project_list_loaded()
        return self

    def click_create_project(self):
        self._loc_create_proj_btn.click()

    def enter_project(self, project_name: str) -> ProjectsPage:
        item = self._loc_proj_wrapper.filter(has_text=project_name).first
        item.click()
        return self

    def search_project(self, project_name: str) -> ProjectsPage:

        expect(self._loc_search_inp).to_be_visible()
        self._loc_search_inp.type(project_name)
        return self

    def is_login_ok_msg_visible(self) -> ProjectsPage:
        expect(self._loc_login_ok_msg).to_be_visible()
        return self

    def get_projects_list_by_name(self, project_name) -> list[Locator]:
        return self._loc_proj_wrapper.filter(has_text=project_name).all()

    def get_all_projects_list(self) -> list[Locator]:
        return self._loc_proj_wrapper.all()

    def has_projects(self) -> bool:
        try:
            locator = self._loc_no_proj_lbl
            locator.wait_for(state="visible", timeout=3000)
            return False

        except TimeoutError:
            return True

    def get_project_list_locator(self) -> Locator:
        return self._loc_proj_wrapper
