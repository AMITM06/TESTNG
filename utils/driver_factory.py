from selenium import webdriver
from config.config import BROWSER, IMPLICIT_WAIT, PAGE_LOAD_TIMEOUT


def get_driver():
    """Create a driver. Selenium Manager (built into Selenium 4.6+) resolves the matching driver binary."""
    browser = BROWSER.lower()

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Chrome(options=options)

    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        driver = webdriver.Firefox(options=options)

    elif browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--start-maximized")
        driver = webdriver.Edge(options=options)

    else:
        raise ValueError(f"Unsupported browser: '{browser}'. Use chrome, firefox, or edge.")

    driver.implicitly_wait(IMPLICIT_WAIT)
    driver.set_page_load_timeout(PAGE_LOAD_TIMEOUT)
    return driver
