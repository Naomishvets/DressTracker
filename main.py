from playwright.sync_api import sync_playwright
import smtplib
from email.message import EmailMessage
import json
import importlib

import os
from dotenv import load_dotenv

load_dotenv()

def send_email_alert(subject, body):
    sender_email = os.getenv("EMAIL_USER")
    sender_password = os.getenv("EMAIL_PASS")
    recipient_email = os.getenv("EMAIL_USER")

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"Email alert sent successfully! Subject: {subject}")
    except Exception as e:
        print(f"Failed to send email. Error: {e}")

def load_config():
    with open("config.json", "r", encoding="utf-8") as file:
        return json.load(file)


def check_product(dress):
    site = dress["site"]
    url = dress["url"]
    target_price = dress["target_price"]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        print(f"Opening {site.upper()}...")
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        try:
            scraper_module = importlib.import_module(f"scrapers.{site}")
            product_info = scraper_module.get_product_info(page)
        except ModuleNotFoundError:
            print(f"Scraper for {site} not found in scrapers folder.")
            browser.close()
            return
        except Exception as e:
            print(f"Error scraping {site}: {e}")
            browser.close()
            return

        browser.close()

        print(f"Scraped data: {product_info}")

        if product_info and product_info.get("current_price"):
            if product_info["current_price"] <= target_price:
                subject = f"Price Drop Alert! {product_info['name']}"
                body = f"Good news! The dress price dropped to {product_info['current_price']} ILS.\n\nTarget Price was: {target_price} ILS\nLink: {url}"
                send_email_alert(subject, body)
            else:
                print(f"Price ({product_info['current_price']}) is still higher than target ({target_price}).")


if __name__ == "__main__":
    send_email_alert("Test Subject", "This is a test email from my Python script!")
    config = load_config()

    for dress in config["dresses"]:
        check_product(dress)