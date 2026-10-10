import base64
import re
from datetime import datetime
from pathlib import Path

import pytest
import pytest_html
from utils.driver_factory import get_driver
from utils.screenshot import full_page_png
from config.config import BASE_URL

SCREENSHOT_DIR = Path(__file__).resolve().parent.parent / "reports" / "screenshots"


@pytest.fixture(scope="function")
def driver():
    drv = get_driver()
    drv.get(BASE_URL)
    yield drv
    drv.quit()


@pytest.fixture(scope="function")
def careers_driver():
    """Driver fixture that opens the careers page directly."""
    drv = get_driver()
    drv.get(BASE_URL)
    yield drv
    drv.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Take a screenshot at the end of every test (pass or fail) and attach it to the HTML report."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call":
        return

    drv = item.funcargs.get("careers_driver") or item.funcargs.get("driver")
    if drv is None:
        return

    SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    name = re.sub(r"[^\w\-]+", "_", item.nodeid)
    path = SCREENSHOT_DIR / f"{name}_{report.outcome}_{stamp}.png"
    try:
        # The test may have switched tabs; the current window is the one that matters
        try:
            png = full_page_png(drv)
        except Exception:
            png = drv.get_screenshot_as_png()  # fall back to the visible area
        path.write_bytes(png)
    except Exception:
        return

    extras = getattr(report, "extras", [])
    extras.append(pytest_html.extras.image(base64.b64encode(png).decode()))
    report.extras = extras
