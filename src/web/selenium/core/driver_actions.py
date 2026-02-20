from selenium.webdriver.support import expected_conditions as EC

from src.web.selenium.core.waits import Wait


class DriverActions:
    def __init__(self, driver, wait: Wait):
        self.driver = driver
        self.wait = wait

    def open_url(self, url):
        self.driver.get(url)

    def switch_to_tab(self, tab_index):
        handles = self.driver.window_handles
        if len(handles) > tab_index:
            self.driver.switch_to.window(handles[tab_index])

    def handle_alert(self, accept=True):
        alert = self._wait.until(EC.alert_is_present())
        if accept:
            alert.accept()
        else:
            alert.dismiss()

    def clear_session(self):
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.refresh()
