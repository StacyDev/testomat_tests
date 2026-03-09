from __future__ import annotations

import allure
from playwright.sync_api import Page, expect


class SideBar:
    def __init__(self, page: Page):
        self.page = page

        self._loc_side_menu = page.locator(".mainnav-menu")
        self._loc_collapsed_menu = page.locator(".mainnav-menu-not-expanded")
        self._loc_logo = self._loc_side_menu.locator(".logo-full")
        self._loc_expand_opt = self._loc_side_menu.locator("button.btn-open")
        self._loc_collapse_opt = self._loc_side_menu.locator("button.btn-close")

        self._loc_tests_menu = self._loc_side_menu.get_by_text("Tests", exact=False)
        self._loc_requirements_menu = self._loc_side_menu.get_by_text("Requirements", exact=False)
        self._loc_runs_menu = self._loc_side_menu.get_by_text("Runs", exact=False)
        self._loc_plans_menu = self._loc_side_menu.get_by_text("Plans", exact=False)
        self._loc_steps_menu = self._loc_side_menu.get_by_text("Steps", exact=False)
        self._loc_pulse_menu = self._loc_side_menu.get_by_text("Pulse", exact=False)
        self._loc_imports_menu = self._loc_side_menu.get_by_text("Imports", exact=False)
        self._loc_analytics_menu = self._loc_side_menu.get_by_text("Analytics", exact=False)
        self._loc_branches_menu = self._loc_side_menu.get_by_text("Branches", exact=False)
        self._loc_settings_menu = self._loc_side_menu.get_by_text("Settings", exact=False)

        self._loc_footer_help = self._loc_side_menu.get_by_text("Help", exact=False)
        self._loc_footer_projects = self._loc_side_menu.get_by_text("Projects", exact=False)
        self._loc_footer_user_menu = self._loc_side_menu.locator(".cursor-pointer")

    @allure.step
    def is_loaded(self) -> SideBar:
        expect(self._loc_collapsed_menu).to_be_visible()
        return self

    @allure.step
    def is_menu_collapsed(self) -> SideBar:
        expect(self.page.locator(".mainnav-menu-expanded")).to_be_hidden()
        return self

    @allure.step
    def is_menu_expanded(self) -> SideBar:
        expect(self.page.locator(".mainnav-menu-expanded")).to_be_visible()
        return self

    @allure.step
    def expand_menu(self) -> SideBar:
        if self._loc_expand_opt.is_visible():
            self._loc_expand_opt.click()
            expect(self.page.locator(".mainnav-menu-expanded")).to_be_visible()
        return self

    @allure.step
    def collapse_menu(self) -> SideBar:
        if self._loc_collapse_opt.is_visible():
            self._loc_collapse_opt.click()
            expect(self.page.locator(".mainnav-menu-expanded")).to_be_hidden()
        return self

    @allure.step
    def click_testomat_logo(self) -> SideBar:
        expect(self._loc_logo).to_be_visible()
        self._loc_logo.click()
        return self

    @allure.step
    def click_tests(self) -> SideBar:
        self._loc_tests_menu.click()
        return self

    @allure.step
    def click_requirements(self) -> SideBar:
        self._loc_requirements_menu.click()
        return self

    @allure.step
    def click_runs(self) -> SideBar:
        self._loc_runs_menu.click()
        return self

    @allure.step
    def click_plans(self) -> SideBar:
        self._loc_plans_menu.click()
        return self

    @allure.step
    def click_steps(self) -> SideBar:
        self._loc_steps_menu.click()
        return self

    @allure.step
    def click_pulse(self) -> SideBar:
        self._loc_pulse_menu.click()
        return self

    @allure.step
    def click_imports(self) -> SideBar:
        self._loc_imports_menu.click()
        return self

    @allure.step
    def click_analytics(self) -> SideBar:
        self._loc_analytics_menu.click()
        return self

    @allure.step
    def click_branches(self) -> SideBar:
        self._loc_branches_menu.click()
        return self

    @allure.step
    def click_settings(self) -> SideBar:
        self._loc_settings_menu.click()
        return self

    @allure.step
    def click_help(self) -> SideBar:
        self._loc_footer_help.click()
        return self

    @allure.step
    def click_projects(self) -> SideBar:
        self._loc_footer_projects.click()
        return self

    @allure.step
    def click_user_menu(self) -> SideBar:
        self._loc_footer_user_menu.click()
        return self

    @allure.step
    def is_expanded(self) -> SideBar:

        nav_items = [
            self._loc_logo,
            self._loc_tests_menu,
            self._loc_requirements_menu,
            self._loc_runs_menu,
            self._loc_plans_menu,
            self._loc_steps_menu,
            self._loc_pulse_menu,
            self._loc_imports_menu,
            self._loc_analytics_menu,
            self._loc_branches_menu,
            self._loc_settings_menu,
            self._loc_footer_help,
            self._loc_footer_projects,
            self._loc_footer_user_menu,
        ]

        for item in nav_items:
            expect(item).to_be_visible()

        return self
