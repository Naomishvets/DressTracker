from playwright.sync_api import Page


def parse_price(price_text):
    if not price_text:
        return None
    price_text = price_text.replace("Now ", "").replace("Was ", "").replace(" ILS", "").replace(",", "")
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
        product_info["name"] = title.inner_text()

        price = page.locator('[data-testid="current-price"]').first
        product_info["current_price"] = parse_price(price.inner_text())

        previous_price_locator = page.locator('[data-testid="previous-price"]')
        if previous_price_locator.count() > 0:
            product_info["original_price"] = parse_price(previous_price_locator.first.inner_text())

    except Exception as e:
        print(f"Could not extract some details from ASOS: {e}")

    return product_info
