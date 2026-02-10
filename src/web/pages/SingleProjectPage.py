from typing import Self

from playwright.sync_api import Page, expect, Dialog, Locator

from src.web.components.SideBar import SideBar
from src.web.pages.ProjectsPage import ProjectsPage


def handle_dialog(dialog: Dialog):
    print(f"Dialog message: {dialog.message}")
    dialog.accept()


class SingleProjectPage:

    def __init__(self, page: Page):
        self.page = page
        self.side_bar = SideBar(page)
        self._loc_proj_title_lbl = self.page.locator(".sticky-header h2")
        self._loc_proj_settings_menu = self.page.locator(".md-icon-cog")
        self._loc_admin_btn = self.page.locator(".red-btn")
        self._loc_delete_proj_btn = self.page.locator(".red-btn")
        self._loc_expand_menu_btn = self.page.locator("button.btn-open")
        self._loc_logo_img = self.page.locator(".logo-full")
        self._loc_new_test_suite_inp = self.page.locator("input[placeholder='First Suite']")
        self._loc_new_test_suite_btn = self.page.get_by_role("button", name="Suite")

    def is_loaded(self) -> SingleProjectPage:
        # self.page.pause()
        self.side_bar.is_loaded()
        expect(self._loc_proj_title_lbl).to_be_visible()
        expect(self._loc_new_test_suite_inp).to_be_visible()
        return self

    def open_project_settings(self) -> SingleProjectPage:
        self.page.once("dialog", handle_dialog)
        (self.side_bar
         .expand_menu()
         .click_settings())
        return self

    def trigger_and_confirm_project_delete(self) -> SingleProjectPage:
        self.page.once("dialog", handle_dialog)
        self._loc_admin_btn.click()
        self.page.once("dialog", handle_dialog)
        self._loc_delete_proj_btn.click()
        return self

    def return_to_projects_list(self) -> ProjectsPage:
        (self.side_bar
         .expand_menu()
         .click_testomat_logo())
        return ProjectsPage(self.page)

    def get_project_title_locator(self) -> Locator:
        return self._loc_proj_title_lbl
