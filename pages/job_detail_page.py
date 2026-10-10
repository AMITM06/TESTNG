from selenium.common.exceptions import (
    ElementClickInterceptedException,
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base.base_page import BasePage
from data.test_data import EMPTY_FIELD_ERROR, INVALID_FIELD_ERROR


class JobDetailPage(BasePage):
    """Job detail and application form (Zoho Recruit, cctech.zohorecruit.in)."""

    COOKIE_DECLINE   = (By.XPATH, "//div[contains(@class,'cw-cookie-banner')]//button[contains(.,'Decline')]")
    COOKIE_LAYER     = (By.CSS_SELECTOR, ".cw-cookie-freeze-layer")
    APPLY_BUTTON     = (By.XPATH, "//button[contains(.,'Apply For Job')]")
    SUBMIT_BUTTON    = (By.XPATH, "//button[@type='submit' and contains(.,'Submit Application')]")
    ERROR_MESSAGES   = (By.CSS_SELECTOR, ".cruxErrMsg")
    SKILL_INPUT      = (By.ID, "addSkills")
    PAGE_TEXT        = (By.TAG_NAME, "body")

    # Labels of the free-text inputs, mapped to the form's data-zcqa attribute
    TEXT_FIELDS = {
        "First Name": "manual_First_Name",
        "Last Name": "manual_Last_Name",
        "Email": "manual_Email",
        "LinkedIn Profile URL": "manual_LinkedIn_Profile_URL",
        "Job Title": "manual_Job_Title",
        "Experience in Years": "manual_Experience_in_Years",
        "Expected Salary": "manual_Expected_Salary",
        "Current Salary": "manual_Current_Salary",
        "Notice period": "manual_Notice_period",
    }
    # Address fields are autocomplete lookups
    LOOKUP_FIELDS = {
        "City": "rec_City",
        "Zip/Postal Code": "rec_Zip_Code",
    }
    # "Add" button of the Educational Details section (the number is the section's id in Zoho Recruit)
    EDUCATION_ADD_BUTTON = "button[id^='crc-tabular-add-btn'][id$='_44607000000169039']"
    # Education row 1 text inputs (prefix match, the suffix is a row index)
    EDUCATION_FIELDS = {
        "Institute / School": "_Institute_School",
        "Major / Department": "_Major_Department",
        "Degree": "_Degree",
        "Graduation College Name": "_Graduation_College_Name",
    }

    def __init__(self, driver):
        super().__init__(driver)

    # Page level actions
    def decline_cookies(self):
        """Dismiss the cookie banner; it overlays the page and blocks clicks."""
        try:
            WebDriverWait(self.driver, 8).until(EC.element_to_be_clickable(self.COOKIE_DECLINE)).click()
            WebDriverWait(self.driver, 8).until(EC.invisibility_of_element_located(self.COOKIE_LAYER))
        except Exception:
            pass  # banner not shown (already answered)

    def click_apply(self):
        self.wait.until(EC.element_to_be_clickable(self.APPLY_BUTTON)).click()
        self.wait.until(EC.visibility_of_element_located(self.SUBMIT_BUTTON))

    def click_submit(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", btn)
        btn.click()

    # Field helpers
    def _type_into(self, element, value):
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", element)
        element.clear()
        element.send_keys(value)

    def _click_when_ready(self, by, value):
        """Click an element that the page may re-render between lookup and click."""
        def attempt(driver):
            try:
                for el in driver.find_elements(by, value):
                    if el.is_displayed():
                        el.click()
                        return True
                return False
            except (StaleElementReferenceException, ElementClickInterceptedException, NoSuchElementException):
                return False
        self.wait.until(attempt)

    def fill_text_field(self, label: str, value: str):
        zcqa = self.TEXT_FIELDS[label]
        el = self.find_visible(By.CSS_SELECTOR, f"[data-zcqa='{zcqa}'] input")
        self._type_into(el, value)

    def fill_lookup_field(self, label: str, value: str):
        """Type into an autocomplete and pick the first suggestion."""
        zcqa = self.LOOKUP_FIELDS[label]
        el = self.find_visible(By.CSS_SELECTOR, f"[data-zcqa='{zcqa}'] lyte-autocomplete input")
        self._type_into(el, value)
        option_xpath = f"//lyte-drop-item[contains(normalize-space(), '{value}') ]"
        self._click_when_ready(By.XPATH, option_xpath)

    def add_skill(self, skill: str):
        chip = (By.XPATH, f"//*[normalize-space(text())='{skill}' and not(self::input) and not(self::script)]"
                          f"[ancestor::*[contains(@class,'kill')]]")
        # Suggestions load slowly now and then, so retype once if the chip does not show up.
        # Picking a chip adds the skill (proficiency defaults to Master).
        for attempt in (1, 2):
            self._type_into(self.find_visible(*self.SKILL_INPUT), skill)
            try:
                WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(chip))
                break
            except TimeoutException:
                if attempt == 2:
                    raise
        self._click_when_ready(*chip)
        # Close the skills panel
        self.driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)

    def add_education_row(self):
        add_btn = self.find_visible(By.CSS_SELECTOR, self.EDUCATION_ADD_BUTTON)
        self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", add_btn)
        add_btn.click()

    def fill_education_field(self, label: str, value: str):
        prefix = self.EDUCATION_FIELDS[label]
        el = self.find_visible(By.CSS_SELECTOR, f"[data-zcqa^='{prefix}_'] input")
        self._type_into(el, value)

    def select_education_duration(self, from_month, from_year, to_month, to_year):
        for part, value in (("from_month", from_month), ("from_year", from_year),
                            ("to_month", to_month), ("to_year", to_year)):
            dropdown = self.find_visible(By.CSS_SELECTOR, f"lyte-dropdown[id$='_1_{part}']")
            self.driver.execute_script("arguments[0].scrollIntoView({block:'center'});", dropdown)
            dropdown.click()
            self._click_when_ready(
                By.XPATH, f"//lyte-drop-item[normalize-space()='{value}' ]"
            )

    # Validation
    def get_error_messages(self) -> list:
        return [e.text.strip() for e in self.driver.find_elements(*self.ERROR_MESSAGES) if e.text.strip()]

    def wait_for_error_messages(self) -> list:
        self.wait.until(lambda d: len(self.get_error_messages()) > 0)
        return self.get_error_messages()

    def expected_error_for(self, label: str) -> str:
        return EMPTY_FIELD_ERROR.format(label=label)

    def invalid_error_for(self, label: str) -> str:
        return INVALID_FIELD_ERROR.format(label=label)

    def is_submit_button_displayed(self) -> bool:
        return self.is_displayed(*self.SUBMIT_BUTTON)

    def get_page_text(self) -> str:
        return self.driver.find_element(*self.PAGE_TEXT).text
