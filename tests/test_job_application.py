import pytest
from pages.careers_page import CareersPage
from pages.job_detail_page import JobDetailPage
from data.test_data import (
    QA_LEAD_JOB_TITLE, VALID_APPLICANT, EDUCATION_DURATION, INVALID_FORMAT_CASES,
)

# Phrases that would indicate the application was accepted
SUCCESS_MARKERS = ["thank you", "successfully submitted", "application submitted", "application received"]

# The CAPTCHA cannot be automated, so it is always left empty and always reports an error.
UNAVOIDABLE_ERRORS = {"CAPTCHA cannot be empty."}


def fill_valid_application(form: JobDetailPage, overrides: dict = None):
    """
    Fill every mandatory field with valid data except Resume and CAPTCHA.
    overrides replaces the valid value of a field (by form label) with another value.
    """
    values = {**VALID_APPLICANT, **(overrides or {})}
    for label in ("First Name", "Last Name", "Email", "LinkedIn Profile URL"):
        form.fill_text_field(label, values[label])
    for label in ("City", "Zip/Postal Code"):
        form.fill_lookup_field(label, values[label])
    form.fill_text_field("Job Title", values["Job Title"])
    form.add_skill(values["Skill Set"])
    for label in ("Experience in Years", "Expected Salary", "Current Salary", "Notice period"):
        form.fill_text_field(label, values[label])
    form.add_education_row()
    for label in ("Institute / School", "Major / Department", "Degree", "Graduation College Name"):
        form.fill_education_field(label, values[label])
    form.select_education_duration(**EDUCATION_DURATION)


def open_application_form(driver) -> JobDetailPage:
    """Careers page -> QA Lead job -> Apply For Job."""
    CareersPage(driver).open_job(QA_LEAD_JOB_TITLE)
    form = JobDetailPage(driver)
    form.decline_cookies()
    form.click_apply()
    return form


def assert_not_submitted(form: JobDetailPage, driver, job_url: str):
    assert form.is_submit_button_displayed(), "Form is gone after submit, application may have been accepted"
    assert driver.current_url == job_url
    page_text = form.get_page_text().lower()
    assert not any(marker in page_text for marker in SUCCESS_MARKERS), "Success message displayed"


class TestJobApplicationValidation:

    def test_qa_lead_application_without_resume_shows_error(self, careers_driver):
        form = open_application_form(careers_driver)
        job_url = careers_driver.current_url

        # Fill all mandatory fields except exactly one: Resume (no file is attached)
        fill_valid_application(form)
        form.click_submit()

        # The missing field is reported
        errors = form.wait_for_error_messages()
        assert form.expected_error_for("Resume") in errors, f"No Resume error found. Errors: {errors}"

        # No field that was filled is reported as an error
        unexpected = [e for e in errors
                      if e != form.expected_error_for("Resume") and e not in UNAVOIDABLE_ERRORS]
        assert not unexpected, f"Filled fields were rejected: {unexpected}"

        assert_not_submitted(form, careers_driver, job_url)

    @pytest.mark.parametrize("label, bad_value", INVALID_FORMAT_CASES,
                             ids=[f"{label}={value}" for label, value in INVALID_FORMAT_CASES])
    def test_qa_lead_application_with_invalid_format_shows_error(self, careers_driver, label, bad_value):
        form = open_application_form(careers_driver)
        job_url = careers_driver.current_url

        # Every mandatory field is valid except one field holding a badly formatted value.
        # Resume is not attached, so its error is expected as well and ignored below.
        fill_valid_application(form, overrides={label: bad_value})
        form.click_submit()

        errors = form.wait_for_error_messages()
        assert form.invalid_error_for(label) in errors, f"No format error for {label}={bad_value!r}. Errors: {errors}"

        # Only the bad field (plus the always-missing Resume and CAPTCHA) is reported
        allowed = {form.invalid_error_for(label), form.expected_error_for("Resume")} | UNAVOIDABLE_ERRORS
        unexpected = [e for e in errors if e not in allowed]
        assert not unexpected, f"Valid fields were rejected: {unexpected}"

        assert_not_submitted(form, careers_driver, job_url)
