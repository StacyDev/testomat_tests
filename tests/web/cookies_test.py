from src.web.application import Application
from tests.fixtures.cookie_helper import CookieHelper


def test_add_feature_flag_cookie(logged_app: Application, cookies: CookieHelper):
    cookies.add("feature_flag", "dark_mode_enabled", "app.testomat.io")

    assert cookies.exists("feature_flag")
    assert cookies.get_value("feature_flag") == "dark_mode_enabled"

    logged_app.page.reload()
