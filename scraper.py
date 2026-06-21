import os
import time
import shutil
import traceback
from threading import Thread

from flask import Flask, jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup

app = Flask(__name__)


@app.route("/")
def home():
    return "Tryline scraper is running"


@app.route("/debug")
def debug():
    return jsonify({
        "google-chrome": shutil.which("google-chrome"),
        "google-chrome-stable": shutil.which("google-chrome-stable"),
        "chromium": shutil.which("chromium"),
        "chromium-browser": shutil.which("chromium-browser"),
        "chromedriver": shutil.which("chromedriver"),
    })


def run_test():
    driver = None

    try:
        print("\n" + "=" * 80, flush=True)
        print("STARTING DEBUG TEST", flush=True)
        print("=" * 80, flush=True)

        # --------------------------------------------------
        # Check what browser binaries exist
        # --------------------------------------------------

        print("\nChecking installed browser binaries...", flush=True)

        print(
            f"google-chrome: {shutil.which('google-chrome')}",
            flush=True
        )

        print(
            f"google-chrome-stable: {shutil.which('google-chrome-stable')}",
            flush=True
        )

        print(
            f"chromium: {shutil.which('chromium')}",
            flush=True
        )

        print(
            f"chromium-browser: {shutil.which('chromium-browser')}",
            flush=True
        )

        print(
            f"chromedriver: {shutil.which('chromedriver')}",
            flush=True
        )

        # --------------------------------------------------
        # Selenium setup
        # --------------------------------------------------

        print("\nCreating Chrome options...", flush=True)

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--remote-debugging-port=9222")

        print("Creating Chrome service...", flush=True)

        service = Service()

        print("Attempting webdriver.Chrome() ...", flush=True)

        start_time = time.time()

        driver = webdriver.Chrome(
            service=service,
            options=options
        )

        elapsed = time.time() - start_time

        print(
            f"Chrome launched successfully in {elapsed:.2f} seconds",
            flush=True
        )

        # --------------------------------------------------
        # Open page
        # --------------------------------------------------

        url = (
            "https://tryline.com.au/match/"
            "2683/2026-round-9-dolphins-vs-melbourne-storm"
        )

        print(f"\nOpening URL: {url}", flush=True)

        driver.get(url)

        print("Page loaded", flush=True)

        time.sleep(5)

        print("Getting page source...", flush=True)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        page_text = soup.get_text(" ", strip=True)

        print(f"\nTitle: {driver.title}", flush=True)

        print("\nFIRST 500 CHARS:", flush=True)
        print(page_text[:500], flush=True)

        print("\nKEYWORD CHECK:", flush=True)
        print(f"Overview: {'Overview' in page_text}", flush=True)
        print(f"Lineup: {'Lineup' in page_text}", flush=True)
        print(f"Team Stats: {'Team Stats' in page_text}", flush=True)
        print(f"Player Stats: {'Player Stats' in page_text}", flush=True)

        print("\nSUCCESS", flush=True)

    except Exception as e:
        print("\nFAILED", flush=True)

        print(f"\nException Type: {type(e).__name__}", flush=True)
        print(f"Exception Message: {str(e)}", flush=True)

        print("\nTRACEBACK:", flush=True)
        print(traceback.format_exc(), flush=True)

    finally:
        if driver:
            try:
                print("\nClosing browser...", flush=True)
                driver.quit()
            except Exception:
                pass


def scraper_loop():
    print("Scraper thread started", flush=True)

    # Run immediately on startup
    run_test()

    while True:
        print("\nSleeping for 120 seconds...", flush=True)
        time.sleep(120)

        run_test()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    print(f"Starting Flask on port {port}", flush=True)

    Thread(
        target=scraper_loop,
        daemon=True
    ).start()

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )