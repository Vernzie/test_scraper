import time
import traceback
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


MATCH_URL = "https://tryline.com.au/match/2683/2026-round-9-dolphins-vs-melbourne-storm"


def run_test():
    try:
        print("=" * 60)
        print("Opening Tryline match page...")

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        driver = webdriver.Chrome(options=options)

        driver.get(MATCH_URL)

        time.sleep(5)

        print("Title:", driver.title)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Print page text sample
        page_text = soup.get_text(" ", strip=True)

        print("\nFIRST 1000 CHARS:")
        print(page_text[:1000])

        # Check if expected content exists
        keywords = [
            "Overview",
            "Lineup",
            "Team Stats",
            "Player Stats"
        ]

        print("\nKEYWORD CHECK:")
        for keyword in keywords:
            print(f"{keyword}: {keyword in page_text}")

        driver.quit()

        print("SUCCESS")

    except Exception:
        print("FAILED")
        print(traceback.format_exc())


print("Worker started...")

while True:
    run_test()

    print("Sleeping 10 seconds...")
    time.sleep(10)