from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.base_page import BasePage


class CareersPage(BasePage):

    # Job listing locators
    JOB_CARDS        = (By.CSS_SELECTOR, ".job-card, .job-listing, article, [class*='job'], [class*='career-item']")
    JOB_TITLE_LINKS  = (By.CSS_SELECTOR, "a[href*='job'], a[href*='career'], h2 a, h3 a, .job-title a")
    VIEW_DETAILS_LINK = (By.XPATH, "//a[contains(text(),'View details')]")

    def __init__(self, driver):
        super().__init__(driver)

    def get_job_count(self):
        try:
            cards = self.find_all(*self.JOB_CARDS)
            return len(cards)
        except Exception:
            return 0

    def click_view_details_for_job(self, job_title_text: str):
        """
        Finds the job card containing job_title_text and clicks its View details link.
        Uses XPath to scope the View details link within the matching card.
        """
        xpath = (
            f"//a[contains(., '{job_title_text}')]"
            f"/ancestor::*[self::article or self::div or self::li][1]"
            f"//a[contains(., 'View details')]"
        )
        link = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        link.click()

    def open_job(self, job_title_text: str):
        """
        Clicks the job title link. The job opens in a new tab, so switch to it.
        """
        link = WebDriverWait(self.driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[normalize-space()='{job_title_text}']"))
        )
        existing = set(self.driver.window_handles)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", link)
        link.click()
        WebDriverWait(self.driver, 15).until(lambda d: len(d.window_handles) > len(existing))
        new_tab = (set(self.driver.window_handles) - existing).pop()
        self.driver.switch_to.window(new_tab)

    def is_job_visible(self, job_title_text: str) -> bool:
        try:
            xpath = f"//*[contains(text(), '{job_title_text}')]"
            el = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, xpath))
            )
            return el.is_displayed()
        except Exception:
            return False
