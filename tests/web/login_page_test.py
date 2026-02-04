import pytest
from faker import Faker

from src.web.Application import Application
from tests.conftest import Config


@pytest.mark.regression
def test_login_invalid(app: Application, configs: Config):
    (app.home_page
     .open()
     .is_loaded()
     .open_login_page_by_click())

    (app.login_page
     .open()
     .is_loaded())
    invalid_password = Faker().password(length=10)
    app.login_page.login(configs.email, invalid_password)
    app.login_page.is_invalid_message_visible()


@pytest.mark.regression
@pytest.mark.smoke
def test_login_success(app: Application, configs: Config):
    (app.home_page
     .open()
     .is_loaded()
     .open_login_page_by_click())

    (app.login_page
     .open()
     .is_loaded())
    app.login_page.login(configs.email, configs.password)

    (app.projects_page
     .is_loaded()
     .is_login_ok_msg_visible())
