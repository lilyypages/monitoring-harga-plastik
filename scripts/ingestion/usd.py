import yfinance as yf
import pandas as pd
import os
import requests


# =========================
# 1. YAHOO FINANCE
# =========================
def get_usd_yahoo():
    print("📥 Ambil USD/IDR dari Yahoo Finance...")

    df = yf.download("USDIDR=X", start="2025-01-01", progress=False)

    if df.empty:
        print("❌ Yahoo gagal")
        return None

    df = df[['Close']].reset_index()
    df.columns = ['date', 'usd_idr']

    return df


# =========================
# 2. BANK INDONESIA (fallback sederhana)
# =========================
def get_usd_bi():
    print("📥 Ambil USD/IDR dari Bank Indonesia (fallback)...")

    try:
        url = "https://api.exchangerate.host/timeseries?start_date=2025-01-01&end_date=2026-05-01&base=USD&symbols=IDR"
        res = requests.get(url).json()

        data = []
        for date, val in res['rates'].items():
            data.append({
                "date": date,
                "usd_idr": val['IDR']
            })

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])

        return df

    except Exception as e:
        print("❌ BI fallback gagal:", e)
        return None


# =========================
# MAIN PIPELINE
# =========================
def main():
    df = get_usd_yahoo()

    if df is None:
        df = get_usd_bi()

    if df is None:
        print("❌ Semua sumber gagal")
        return

    df = df.sort_values("date")

    output_path = "data/raw/usd_idr.csv"
    df.to_csv(output_path, index=False)

    print(f"\n💾 Data disimpan: {output_path}")
    print(f"📊 Total data: {len(df)} baris")
    print(df.head())


if __name__ == "__main__":
    main()