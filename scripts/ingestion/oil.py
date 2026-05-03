import os
import yfinance as yf
import pandas as pd


RAW_DIR = "/opt/airflow/data/raw"
OUTPUT_PATH = os.path.join(RAW_DIR, "oil.csv")


def fetch_oil_price():
    print("Mengambil data harga minyak WTI...")

    df = yf.download("CL=F", start="2025-01-01", progress=False)

    if df.empty:
        raise ValueError("Data harga minyak kosong.")

    df = df[["Close"]].reset_index()
    df.columns = ["date", "oil_price"]

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date")

    os.makedirs(RAW_DIR, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Data disimpan ke: {OUTPUT_PATH}")
    print(f"Total data: {len(df)} baris")


def main():
    fetch_oil_price()


if __name__ == "__main__":
    main()