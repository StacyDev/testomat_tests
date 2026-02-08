import pytest
from _pytest.mark import ParameterSet
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config, configs

fake = Faker()

invalid_login_data = [
    # --- Format & Empty Fields ---
    pytest.param("", "", id="empty_credentials"),
    pytest.param("placeholder_email", "", id="missing_password"),
    pytest.param(fake.user_name(), "placeholder_password", id="invalid_email_format"),

    # --- Authentication Logic ---
    pytest.param(fake.email(), fake.password(10), id="non_existent_user"),
    pytest.param("placeholder_email", "wrong_password_123", id="wrong_password"),

    # --- Security & Edge Cases ---
    pytest.param(f"{fake.lexify('?' * 1000)}@gmail.com", fake.password(10),
                 id="extreme_long_login"),
    pytest.param("placeholder_email", fake.password(1000), id="extreme_long_password"),
    pytest.param("admin' OR '1'='1", "placeholder_password", id="sql_injection_attempt_email"),
    pytest.param("placeholder_email", "admin' OR '1'='1", id="sql_injection_attempt_password"),
    pytest.param("<script>alert(1)</script>@test.com", "placeholder_password",
                 id="xss_payload_in_email")
]


def fill_out_test_data_placeholders(configs: Config, data_item: str) -> str:
    if "placeholder_email" in data_item:
        data_item = data_item.replace("placeholder_email", configs.email)

    if "placeholder_password" in data_item:
        data_item = data_item.replace("placeholder_password", configs.password)

    return data_item


@pytest.mark.regression
@pytest.mark.parametrize("email, password", invalid_login_data)
def test_login_invalid(app_shared_page: Application, configs: Config, email, password):
    email_value = fill_out_test_data_placeholders(configs, email)
    password_value = fill_out_test_data_placeholders(configs, password)

    (app_shared_page.login_page
     .open()
     .is_loaded())

    app_shared_page.login_page.login(email_value, password_value)
    app_shared_page.login_page.is_invalid_message_visible()


valid_login_data = [
    # --- Format & Empty Fields ---
    pytest.param(f"   {"placeholder_email"}   ", "placeholder_password",
                 id="leading_and_trailing_space_in_email"),
    pytest.param("placeholder_email", "placeholder_password", id="valid_credential")]


@pytest.mark.regression
@pytest.mark.smoke
@pytest.mark.parametrize("email, password", valid_login_data)
def test_login_success(app_shared_page: Application, configs: Config, email, password):
    app = app_shared_page
    email_value = fill_out_test_data_placeholders(configs, email)
    password_value = fill_out_test_data_placeholders(configs, password)

    (app.login_page
     .open()
     .is_loaded())
    app.login_page.login(email_value, password_value)

    (app.projects_page
     .is_loaded()
     .is_login_ok_msg_visible())
