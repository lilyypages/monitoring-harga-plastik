import yfinance as yf
import pandas as pd
import os

# =========================
# FETCH DATA
# =========================
def fetch_oil_price():
    print("📥 Mengambil data harga minyak (WTI)...")

    # CL=F = Crude Oil (WTI Futures)
    df = yf.download("CL=F", start="2025-01-01", progress=False)

    if df.empty:
        print("❌ Data kosong!")
        return

    # ambil kolom close
    df = df[['Close']].reset_index()
    df.columns = ['date', 'oil_price']

    # bersihin
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values('date')

    print(df.head())

    # save
    output_path = "data/raw/oil.csv"
    df.to_csv(output_path, index=False)

    print(f"\n💾 Data disimpan ke: {output_path}")
    print(f"📊 Total data: {len(df)} baris")


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    fetch_oil_price()