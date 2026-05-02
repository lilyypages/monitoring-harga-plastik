
"""
================================================================
  Scraper Harga Plastik (Polyethylene) — CLEAN VERSION
================================================================
"""

import os
import time
import json
import logging
import requests
import pandas as pd

from datetime import datetime
from bs4 import BeautifulSoup

# ── CONFIG ─────────────────────────────────────────────────────
SAVE_DIR = r"D:\IPBD\Project-Pipeline-EndToEnd\data\raw"
URL = "https://tradingeconomics.com/commodity/polyethylene"

os.makedirs(SAVE_DIR, exist_ok=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


# ================================================================
# UTIL
# ================================================================
def ts_to_date(ts):
    return datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d")


def setup_driver(headless=True):
    from selenium import webdriver
    from selenium.webdriver.firefox.options import Options
    from selenium.webdriver.firefox.service import Service
    from webdriver_manager.firefox import GeckoDriverManager

    opts = Options()
    if headless:
        opts.add_argument("--headless")

    opts.set_preference("dom.webnotifications.enabled", False)

    service = Service(GeckoDriverManager().install())
    return webdriver.Firefox(service=service, options=opts)


# ================================================================
# METHOD 1 — Highcharts (BEST)
# ================================================================
def scrape_highcharts():
    from selenium.webdriver.support.ui import WebDriverWait

    logging.info("[Highcharts] Start scraping...")

    driver = setup_driver()

    try:
        driver.get(URL)

        # tunggu Highcharts muncul
        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return typeof Highcharts !== 'undefined'")
        )

        js = """
        var chart = Highcharts.charts[0];
        if (!chart) return null;

        var s = chart.series[0];

        return JSON.stringify({
            data: s.options.data || [],
            x: s.processedXData || [],
            y: s.processedYData || [],
            name: s.name
        });
        """

        result = driver.execute_script(js)

        if not result:
            return None

        obj = json.loads(result)

        records = []

        # format 1
        if obj["data"] and isinstance(obj["data"][0], list):
            for pt in obj["data"]:
                records.append({
                    "date": ts_to_date(pt[0]),
                    "plastic_price": pt[1],
                })

        # format 2
        elif obj["x"] and obj["y"]:
            for x, y in zip(obj["x"], obj["y"]):
                records.append({
                    "date": ts_to_date(x),
                    "plastic_price": y,
                })

        if records:
            df = pd.DataFrame(records)
            df["satuan"] = "CNY/T"
            df["sumber"] = "TradingEconomics"
            df["metode"] = "highcharts"
            logging.info(f"[Highcharts] SUCCESS {len(df)} rows")
            return df

    except Exception as e:
        logging.error(f"[Highcharts] Error: {e}")

    finally:
        driver.quit()

    return None


# ================================================================
# METHOD 2 — XHR REQUEST
# ================================================================
def scrape_xhr():
    logging.info("[XHR] Start scraping...")

    driver = setup_driver()

    try:
        driver.get(URL)
        time.sleep(5)

        js = """
        return performance.getEntries().map(e => e.name)
        """

        urls = driver.execute_script(js)
        cookies = {c['name']: c['value'] for c in driver.get_cookies()}

        driver.quit()

        for u in urls:
            if "chart" in u.lower():
                try:
                    r = requests.get(u, cookies=cookies, timeout=10)
                    data = r.json()

                    if isinstance(data, list):
                        records = []
                        for pt in data:
                            records.append({
                                "date": ts_to_date(pt[0]),
                                "plastic_price": pt[1],
                                "satuan": "CNY/T",
                                "sumber": "TradingEconomics",
                                "metode": "xhr"
                            })

                        if records:
                            logging.info(f"[XHR] SUCCESS {len(records)} rows")
                            return pd.DataFrame(records)

                except Exception as e:
                    logging.warning(f"[XHR] Skip URL: {e}")

    except Exception as e:
        logging.error(f"[XHR] Error: {e}")

    return None


# ================================================================
# METHOD 3 — HTML (LAST RESORT)
# ================================================================
def scrape_html():
    logging.info("[HTML] Fallback scraping...")

    try:
        r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(r.text, "html.parser")

        h2 = soup.find("h2")
        if not h2:
            return None

        text = h2.get_text()

        import re
        num = re.findall(r'\d+\.?\d*', text)

        if num:
            df = pd.DataFrame([{
                "date": datetime.now().strftime("%Y-%m-%d"),
                "plastic_price": float(num[0]),
                "satuan": "CNY/T",
                "sumber": "TradingEconomics",
                "metode": "html"
            }])
            logging.info("[HTML] SUCCESS")
            return df

    except Exception as e:
        logging.error(f"[HTML] Error: {e}")

    return None


# ================================================================
# SAVE
# ================================================================
def save_data(df):

    f_csv = os.path.join(SAVE_DIR, f"polyethylene.csv")
    f_json = os.path.join(SAVE_DIR, f"polyethylene.json")

    df.to_csv(f_csv, index=False, encoding="utf-8-sig")
    df.to_json(f_json, orient="records", indent=2)

    logging.info("======================================")
    logging.info(f"SAVED CSV  : {f_csv}")
    logging.info(f"SAVED JSON : {f_json}")
    logging.info(f"ROWS       : {len(df)}")
    logging.info("======================================")


# ================================================================
# MAIN
# ================================================================
def main():
    logging.info("START SCRAPING...")

    df = scrape_highcharts()

    if df is None:
        df = scrape_xhr()

    if df is None:
        df = scrape_html()

    if df is None:
        logging.warning("All methods failed. Using dummy data.")
        df = pd.DataFrame([{
            "date": datetime.now().strftime("%Y-%m-%d"),
            "plastic_price": 8887,
            "satuan": "CNY/T",
            "sumber": "dummy",
            "metode": "manual"
        }])

    save_data(df)


if __name__ == "__main__":
    main()
