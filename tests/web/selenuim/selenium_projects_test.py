import pytest

from src.web.selenium.selenium_application import SeleniumApplication

search_project_data = [
    pytest.param("Industrial", id="search_project_by_full_name"),
    pytest.param("Ind", id="search_project_by_first_two_characters_upper_case"),
]


@pytest.mark.regression
@pytest.mark.parametrize("search_value", search_project_data)
def test_project_search(selenium_logged_app: SeleniumApplication, search_value):
    (
        selenium_logged_app.projects_page.is_loaded()
        .is_project_list_loaded()
        .search_project(search_value)
        .verify_found_project_titles_correct(search_value)
    )
