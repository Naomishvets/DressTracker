from playwright.sync_api import Page


def parse_price(price_text):
    if not price_text:
        return None
    price_text = price_text.replace("₪", "").replace(",", "").strip()
    try:
        return float(price_text)
    except ValueError:
        return None


def get_product_info(page: Page):
    product_info = {
        "name": None,
        "current_price": None,
        "original_price": None,
        "currency": "ILS",
        "in_stock": True
    }

    try:
        title = page.locator("h1").first
        product_info["name"] = title.inner_text().strip()

        sale_price_locator = page.locator('#markdownPrice').first
        retail_price_locator = page.locator('#retailPrice').first

        if sale_price_locator.is_visible():
            product_info["current_price"] = parse_price(sale_price_locator.inner_text())

            strikethrough_locator = page.locator('#retailPriceStrikethrough').first
            if strikethrough_locator.is_visible():
                product_info["original_price"] = parse_price(strikethrough_locator.inner_text())
        else:
            product_info["current_price"] = parse_price(retail_price_locator.inner_text())

    except Exception as e:
        print(f"Could not extract some details from Revolve: {e}")

    return product_info