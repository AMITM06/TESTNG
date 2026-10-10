from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    def open(self, url):
        self.driver.get(url)

    def find(self, by, value):
        return self.wait.until(EC.presence_of_element_located((by, value)))

    def find_visible(self, by, value):
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    def find_all(self, by, value):
        self.wait.until(EC.presence_of_all_elements_located((by, value)))
        return self.driver.find_elements(by, value)

    def click(self, by, value):
        self.wait.until(EC.element_to_be_clickable((by, value))).click()

    def type(self, by, value, text):
        el = self.find_visible(by, value)
        el.clear()
        el.send_keys(text)

    def get_text(self, by, value):
        return self.find_visible(by, value).text.strip()

    def is_displayed(self, by, value):
        try:
            return self.find_visible(by, value).is_displayed()
        except Exception:
            return False

    def get_title(self):
        return self.driver.title

    def get_current_url(self):
        return self.driver.current_url
