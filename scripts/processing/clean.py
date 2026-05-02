import pandas as pd

def main():
    oil = pd.read_csv("data/raw/oil.csv")
    plastic = pd.read_csv("data/raw/polyethylene.csv")
    usd = pd.read_csv("data/raw/usd_idr.csv")

    # ===== OIL =====
    oil = oil[["date", "oil_price"]]

    # ===== PLASTIC =====
    plastic = plastic[["date", "plastic_price"]]

    # ===== USD =====
    usd = usd[["date", "usd_idr"]]

    # convert tanggal
    oil["date"] = pd.to_datetime(oil["date"])
    plastic["date"] = pd.to_datetime(plastic["date"])
    usd["date"] = pd.to_datetime(usd["date"])

    # sort biar rapi
    oil = oil.sort_values("date")
    plastic = plastic.sort_values("date")
    usd = usd.sort_values("date")

    # simpan
    oil.to_csv("data/processed/oil_clean.csv", index=False)
    plastic.to_csv("data/processed/plastic_clean.csv", index=False)
    usd.to_csv("data/processed/usd_clean.csv", index=False)

if __name__ == "__main__":
    main()