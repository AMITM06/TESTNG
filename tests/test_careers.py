from pages.careers_page import CareersPage


class TestCareersPage:

    def test_page_loads_successfully(self, careers_driver):
        page = CareersPage(careers_driver)
        assert "cctech" in page.get_current_url().lower()

    def test_page_title_is_present(self, careers_driver):
        page = CareersPage(careers_driver)
        title = page.get_title()
        assert title != ""
