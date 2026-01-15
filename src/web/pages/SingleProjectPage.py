from playwright.sync_api import Page, expect, Dialog


def handle_dialog(dialog: Dialog):
    print(f"Dialog message: {dialog.message}")
    dialog.accept()


class SingleProjectPage:
    def __init__(self, page: Page, project_name: str):
        self.page = page
        self.project_name = project_name
        self.loc_proj_title_lbl = self.page.locator(".sticky-header h2", has_text=self.project_name)
        self.loc_proj_settings_menu = self.page.locator(".md-icon-cog")
        self.loc_admin_btn = self.page.locator(".red-btn")
        self.loc_delete_proj_btn = self.page.locator(".red-btn")
        self.loc_expand_menu_btn = self.page.locator("button.btn-open")
        self.loc_logo_img = self.page.locator(".logo-full")

    def is_loaded(self):
        expect(self.loc_proj_title_lbl).to_be_visible()

    def open_project_settings(self):
        self.page.once("dialog", handle_dialog)
        self.loc_proj_settings_menu.click()

    def trigger_and_confirm_project_delete(self):
        self.page.once("dialog", handle_dialog)
        self.loc_admin_btn.click()
        self.page.once("dialog", handle_dialog)
        self.loc_delete_proj_btn.click()

    def expand_project_side_menu(self):
        expect( self.loc_expand_menu_btn).to_be_visible()
        self.loc_expand_menu_btn.click()

    def click_testomat_logo(self):
        expect(self.loc_logo_img).to_be_visible()
        self.loc_logo_img.click()

    def return_to_projects_list(self):
        self.expand_project_side_menu()
        self.click_testomat_logo()
