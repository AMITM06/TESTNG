import base64


def full_page_png(driver) -> bytes:
    """Return a PNG of the whole page, not just the visible window."""
    if hasattr(driver, "get_full_page_screenshot_as_png"):  # Firefox
        return driver.get_full_page_screenshot_as_png()

    # Chrome and Edge: capture beyond the viewport through the DevTools protocol
    size = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})["cssContentSize"]
    data = driver.execute_cdp_cmd("Page.captureScreenshot", {
        "format": "png",
        "captureBeyondViewport": True,
        "clip": {"x": 0, "y": 0, "width": size["width"], "height": size["height"], "scale": 1},
    })["data"]
    return base64.b64decode(data)
