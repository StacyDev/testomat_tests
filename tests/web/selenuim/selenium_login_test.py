import pytest

from src.web.selenium.selenium_application import SeleniumApplication
from tests.fixtures.config import Config
from tests.web.login_page_test import fake

invalid_login_data = [
    # --- Format & Empty Fields ---
    pytest.param("", "", id="empty_credentials"),
    pytest.param("placeholder_email", "", id="missing_password"),
    pytest.param(fake.user_name(), "placeholder_password", id="invalid_email_format"),
    # --- Authentication Logic ---
    pytest.param(fake.email(), fake.password(10), id="non_existent_user"),
    pytest.param("placeholder_email", "wrong_password_123", id="wrong_password"),
    # --- Security & Edge Cases ---
    pytest.param(
        f"{fake.lexify('?' * 1000)}@gmail.com",
        fake.password(10),
        id="extreme_long_login",
    ),
    pytest.param("placeholder_email", fake.password(1000), id="extreme_long_password"),
    pytest.param("admin' OR '1'='1", "placeholder_password", id="sql_injection_attempt_email"),
    pytest.param("placeholder_email", "admin' OR '1'='1", id="sql_injection_attempt_password"),
    pytest.param(
        "<script>alert(1)</script>@test.com",
        "placeholder_password",
        id="xss_payload_in_email",
    ),
]


def fill_out_test_data_placeholders(configs: Config, data_item: str) -> str:
    if "placeholder_email" in data_item:
        data_item = data_item.replace("placeholder_email", configs.email)

    if "placeholder_password" in data_item:
        data_item = data_item.replace("placeholder_password", configs.password)

    return data_item


@pytest.mark.parametrize("email, password", invalid_login_data)
def test_login_invalid_creds(
    selenium_app: SeleniumApplication, configs: Config, email, password
) -> None:
    email_value = fill_out_test_data_placeholders(configs, email)
    password_value = fill_out_test_data_placeholders(configs, password)
    (
        selenium_app.login_page.open(configs.base_sing_in_url)
        .is_loaded()
        .login(email_value, password_value)
    )
    selenium_app.login_page.is_invalid_message_visible()


valid_login_data = [
    pytest.param(
        f"   {'placeholder_email'}   ",
        "placeholder_password",
        id="leading_and_trailing_space_in_email",
    ),
    pytest.param("placeholder_email", "placeholder_password", id="valid_credential"),
]


@pytest.mark.parametrize("email, password", valid_login_data)
def test_login_valid_creds(
    selenium_app: SeleniumApplication, configs: Config, email, password
) -> None:
    email_value = fill_out_test_data_placeholders(configs, email)
    password_value = fill_out_test_data_placeholders(configs, password)
    (
        selenium_app.login_page.open(configs.base_sing_in_url)
        .is_loaded()
        .login(email_value, password_value)
    )
    (selenium_app.projects_page.is_loaded().is_login_ok_msg_visible())
