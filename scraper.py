import os
import time
import traceback
from threading import Thread

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def home():
    return "Tryline scraper is running"


def run_test():
    driver = None

    try:
        print("=" * 60, flush=True)
        print("Opening Tryline match page...", flush=True)

        print("Creating Chrome options...", flush=True)

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        print("Launching Chrome...", flush=True)

        driver = webdriver.Chrome(options=options)

        print("Chrome launched!", flush=True)

        driver.get(
            "https://tryline.com.au/match/2683/2026-round-9-dolphins-vs-melbourne-storm"
        )

        time.sleep(5)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(" ", strip=True)

        print(f"Title: {driver.title}", flush=True)

        print("\nFIRST 500 CHARS:", flush=True)
        print(page_text[:500], flush=True)

        print("\nKEYWORD CHECK:", flush=True)
        print(f"Overview: {'Overview' in page_text}", flush=True)
        print(f"Lineup: {'Lineup' in page_text}", flush=True)
        print(f"Team Stats: {'Team Stats' in page_text}", flush=True)
        print(f"Player Stats: {'Player Stats' in page_text}", flush=True)

        print("SUCCESS", flush=True)

    except Exception:
        print("FAILED", flush=True)
        print(traceback.format_exc(), flush=True)

    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


def scraper_loop():
    print("Scraper thread started", flush=True)

    while True:
        run_test()

        print("Sleeping for 120 seconds...", flush=True)
        time.sleep(120)


if __name__ == "__main__":
    Thread(target=scraper_loop, daemon=True).start()

    port = int(os.environ.get("PORT", 10000))

    print(f"Starting Flask on port {port}", flush=True)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )