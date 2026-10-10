# Test data for CCTech Careers page

CAREERS_URL = "https://www.cctech.co.in/careers"

# Example: job search keywords for data-driven tests
SEARCH_KEYWORDS = [
    "Python",
    "Selenium",
    "QA",
    "Developer",
]

# Example: expected job titles (update after inspecting live page)
EXPECTED_JOB_TITLES = [
    # "Software Engineer",
    # "QA Automation Engineer",
]

# Example: filter options to validate
FILTER_OPTIONS = [
    # "Full Time",
    # "Remote",
]

# Job used by the application form tests (exact listing title on the careers page)
QA_LEAD_JOB_TITLE = "QA Lead Drive 9th Oct 2026"

# Valid values for every mandatory field except Resume and CAPTCHA.
# Keys are the form labels as shown on the application form.
VALID_APPLICANT = {
    "First Name": "Test",
    "Last Name": "Candidate",
    "Email": "test.candidate@example.com",
    "LinkedIn Profile URL": "https://www.linkedin.com/in/test-candidate",
    "City": "Pune",
    "Zip/Postal Code": "411001",
    "Job Title": "QA Lead",
    "Skill Set": "Selenium",
    "Experience in Years": "8",
    "Expected Salary": "2000000",
    "Current Salary": "1800000",
    "Notice period": "30",
    "Institute / School": "Test Institute of Technology",
    "Major / Department": "Computer Science",
    "Degree": "B.E.",
    "Graduation College Name": "Test Institute of Technology",
}

EDUCATION_DURATION = {
    "from_month": "Jun",
    "from_year": "2010",
    "to_month": "May",
    "to_year": "2014",
}

# Zoho Recruit shows "<Label> cannot be empty." under a mandatory field left blank
EMPTY_FIELD_ERROR = "{label} cannot be empty."

# ...and "Please enter a valid <Label>." for a value in the wrong format
INVALID_FIELD_ERROR = "Please enter a valid {label}."

# (field label, invalid value) pairs the form is known to reject
INVALID_FORMAT_CASES = [
    ("Email", "invalid-email"),
    ("Email", "test@example"),
    ("LinkedIn Profile URL", "not a url"),
    ("Experience in Years", "abc"),
    ("Expected Salary", "abc"),
    ("Current Salary", "abc"),
]
