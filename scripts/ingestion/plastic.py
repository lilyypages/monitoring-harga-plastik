"""
=========================================================
Scraper Harga Plastik / Resin Plastik
Source: FRED - Producer Price Index: Plastics Material and Resin Manufacturing
Output: /opt/airflow/data/raw/plastic.csv
=========================================================
"""

import os
import logging
from datetime import datetime

import pandas as pd


# =========================
# CONFIG
# =========================
SAVE_DIR = os.getenv("SAVE_DIR", "/opt/airflow/data/raw")
OUTPUT_FILE = "plastic.csv"
OUTPUT_PATH = os.path.join(SAVE_DIR, OUTPUT_FILE)

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=PCU325211325211"
VALUE_COL = "PCU325211325211"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# =========================
# SCRAPER
# =========================
def fetch_plastic_price():
    logging.info("Mengambil data Plastic Material and Resin Price Index dari FRED...")

    try:
        df = pd.read_csv(FRED_URL)

        if df.empty:
            raise ValueError("Data dari FRED kosong.")

        if VALUE_COL not in df.columns:
            raise ValueError(f"Kolom {VALUE_COL} tidak ditemukan. Kolom tersedia: {df.columns.tolist()}")

        # Bersihkan missing value dari FRED
        df = df[df[VALUE_COL] != "."].copy()
        df[VALUE_COL] = pd.to_numeric(df[VALUE_COL], errors="coerce")
        df = df.dropna(subset=[VALUE_COL])

        if df.empty:
            raise ValueError("Tidak ada data valid setelah cleaning.")

        # Rename agar konsisten untuk pipeline
        df = df.rename(
            columns={
                "observation_date": "date",
                VALUE_COL: "plastic_price"
            }
        )

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date")

        # Metadata
        df["satuan"] = "PPI Index"
        df["sumber"] = "FRED"
        df["metode"] = "csv_api"
        df["scraped_at"] = datetime.now()

        # Simpan ke folder raw
        os.makedirs(SAVE_DIR, exist_ok=True)
        df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")

        logging.info("======================================")
        logging.info(f"SAVED CSV : {OUTPUT_PATH}")
        logging.info(f"ROWS      : {len(df)}")
        logging.info("======================================")

        return df

    except Exception as e:
        logging.error(f"Gagal mengambil data plastik: {e}")
        raise


# =========================
# MAIN
# =========================
def main():
    logging.info("START SCRAPING PLASTIC DATA...")
    fetch_plastic_price()
    logging.info("FINISH SCRAPING PLASTIC DATA.")


if __name__ == "__main__":
    main()