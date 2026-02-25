from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

BySelector = tuple[By, str]
SelectorOrElement = BySelector | WebElement


class Wait:
    DEFAULT_TIMEOUT = 10
    DEFAULT_POLL = 0.2
    IGNORED_EXCEPTIONS = (NoSuchElementException, StaleElementReferenceException)

    def __init__(self, driver: WebDriver, timeout: int = DEFAULT_TIMEOUT):
        self.driver = driver
        self.timeout = timeout
        self._wait = WebDriverWait(
            driver,
            timeout,
            poll_frequency=self.DEFAULT_POLL,
            ignored_exceptions=self.IGNORED_EXCEPTIONS,
        )

    def _is_locator(self, target: SelectorOrElement) -> bool:
        return isinstance(target, tuple) and len(target) == 2

    def _set_custom_timeout_if_any(self, custom_timeout: int = None) -> WebDriverWait | None:
        if custom_timeout:
            return WebDriverWait(self.driver, custom_timeout, poll_frequency=self.DEFAULT_POLL)
        return self._wait

    def for_visible(self, target: SelectorOrElement, custom_timeout: int = None) -> WebElement:
        local_wait = self._set_custom_timeout_if_any(custom_timeout)
        if self._is_locator(target):
            return local_wait.until(EC.visibility_of_element_located(target))

        return self._wait.until(EC.visibility_of(target))

    def for_invisible(self, target: SelectorOrElement, custom_timeout: int = None) -> WebElement:
        local_wait = self._set_custom_timeout_if_any(custom_timeout)
        if self._is_locator(target):
            return local_wait.until(EC.invisibility_of_element_located(target))

        return self._wait.until(EC.invisibility_of_element(target))

    def for_clickable(self, target: SelectorOrElement, custom_timeout: int = None) -> WebElement:
        local_wait = self._set_custom_timeout_if_any(custom_timeout)
        return local_wait.until(EC.element_to_be_clickable(target))

    def for_all_present(self, locator, custom_timeout: int = None) -> list[WebElement]:
        local_wait = self._set_custom_timeout_if_any(custom_timeout)

        return local_wait.until(EC.presence_of_all_elements_located(locator))

    def for_element_present(self, locator, custom_timeout: int = None) -> WebElement:
        local_wait = self._set_custom_timeout_if_any(custom_timeout)
        return local_wait.until(EC.presence_of_element_located(locator))

    def for_condition(self, condition, custom_timeout: int = None) -> WebElement:
        wait = self._set_custom_timeout_if_any(custom_timeout)
        return wait.until(condition)

    def until(self, condition):
        return self._wait.until(condition)

    def find_now(self, locator) -> list[WebElement]:
        return self.driver.find_elements(*locator)
