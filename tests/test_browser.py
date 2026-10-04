import os
import pytest
from playwright.sync_api import sync_playwright

from scrapers.asos import get_product_info


def test_asos_scraper_with_local_html():
    current_dir = os.path.dirname(os.path.abspath(__file__))

    html_file_path = os.path.join(current_dir, "asos_dummy.html")

    file_uri = f"file:///{html_file_path.replace(chr(92), '/')}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        page.goto(file_uri)

        product_info = get_product_info(page)

        browser.close()

    assert product_info is not None

    assert product_info["currency"] == "ILS"

    assert isinstance(product_info["current_price"], float)

