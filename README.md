# CCTech Careers Automation

Selenium and pytest UI tests for the CCTech careers page (https://www.cctech.co.in/careers) and the
Zoho Recruit application form it links to (cctech.zohorecruit.in).

## Setup

```
pip install -r requirements.txt
```

Chrome is the default browser (`config/config.py`, `BROWSER`). Selenium Manager downloads the matching
driver automatically, so no driver setup is needed.

## Running tests

```
pytest                                   # everything
pytest tests/test_job_application.py     # application form validation only
```

Every run writes an HTML report to `reports/report.html` and one full-page screenshot per test to
`reports/screenshots/`. The same screenshot is embedded in the report. Both are overwritten or added to
on each run, so copy the report out if you need to keep a particular run.

## Structure

```
config/        Settings: base URL, browser, timeouts
data/          Test data (job title, applicant values, expected messages)
pages/         Page objects
  base/        BasePage: shared find, click, type and wait helpers
  careers_page.py     Careers listing page (open a job, which opens in a new tab)
  job_detail_page.py  Job detail page and application form
tests/         Test cases and conftest.py (driver fixtures, screenshot hook)
  test_job_application.py  Application form negative tests (missing Resume, invalid formats)
utils/         driver_factory.py: browser creation
               screenshot.py: full-page screenshot (Chrome and Edge via DevTools, Firefox natively)
reports/       Generated output (HTML report, screenshots). Not source.
pytest.ini     Test discovery and report options
```

## Policy

**Layering.** Tests contain steps and assertions only. Locators and page interactions live in page
objects. Test values live in `data/`. A test should not contain a locator.

**Test data.** Use dummy data only (for example `test.candidate@example.com`). Never put real
candidate details, real resumes or credentials in the repo.

**Never submit a real application.** These tests are negative tests. Each one must leave at least one
mandatory field empty and assert that the form was not accepted: the expected error is shown, the
form is still displayed, the URL is unchanged and no success text appears. Do not add a test that
completes a valid submission against the live site.

**CAPTCHA.** The form has a CAPTCHA. It is not bypassed or automated. It stays empty, so the form
always also reports `CAPTCHA cannot be empty.` Tests allow that one extra message and fail on any
other unexpected error.

**Locators.** Prefer stable attributes (`data-zcqa`, `name`, ids) over text or position. Keep each
locator in one place in the page object. Form-specific ids (for example the Add button of the
Educational Details section) are named constants with a comment, since they change if the form is
edited in Zoho Recruit.

**Waits.** Use explicit waits. No `time.sleep`. Use `_click_when_ready` for elements the page
re-renders (autocomplete and dropdown options).

**Cookie banner.** The Zoho page shows a cookie banner that blocks clicks. Tests decline it with
`JobDetailPage.decline_cookies()` before interacting.

**Screenshots.** Taken automatically after every test, pass or fail, by the hook in
`tests/conftest.py`. They capture the whole page, not just the visible window, and fall back to the
visible area if a full-page capture is not possible. Tests do not take their own. File names are
`<test id>_<passed|failed>_<timestamp>.png`.

**Negative test coverage.** Each test changes one thing from a fully valid form. The missing-Resume
test leaves Resume empty. The invalid-format tests (`INVALID_FORMAT_CASES` in `data/test_data.py`)
put one badly formatted value in an otherwise valid form. Each asserts the exact message for that
field, that no other filled field is flagged, and that the form was not submitted. Add a case by
adding one line to the list, but only after confirming the live form rejects that value.

**Browser sessions.** Each test gets a fresh browser through a fixture and the fixture quits it.
Jobs open in a new tab, so page objects switch to it explicitly.

**Adding a test.** Add the page object method first, add data to `data/test_data.py`, then write the
test in `tests/test_*.py` with a name that states the expected behavior.

## Known gaps

- The live form accepts some values it arguably should reject, so they have no tests: negative numbers
  in Experience in Years and Expected Salary, letters or negative numbers in Notice period, and odd
  text in Zip/Postal Code (typed without choosing a suggestion).
- Each test opens a fresh browser, so the suite is slow (about 5 minutes for 7 tests).
- There is no keyword search test. The earlier placeholder was removed because `CareersPage.search_jobs`
  does not exist.
- The target job is matched by its exact listing title. When the listing is renamed or removed,
  update `QA_LEAD_JOB_TITLE` in `data/test_data.py`.
