import pytest
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.fixtures.config import Config


def test_selenium_login_and_search(driver: WebDriver, configs: Config):
    wait = WebDriverWait(
        driver, 10, 0.1, ignored_exceptions=[NoSuchElementException, StaleElementReferenceException]
    )

    login_txt_selector: str = "#content-desktop #user_email"
    password_txt_selector: str = "#content-desktop #user_password"
    btn_selector: str = "#content-desktop input[type='submit']"
    comp_select_wrapper: str = "#content-desktop select#company_id"

    driver.get(configs.base_url_app)
    if driver.find_element(By.CSS_SELECTOR, login_txt_selector).is_displayed():
        driver.find_element(By.CSS_SELECTOR, login_txt_selector).send_keys(configs.email)
        driver.find_element(By.CSS_SELECTOR, password_txt_selector).send_keys(configs.password)
        driver.find_element(By.CSS_SELECTOR, btn_selector).click()

    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, comp_select_wrapper)))
    driver.find_element(By.CSS_SELECTOR, comp_select_wrapper).click()
