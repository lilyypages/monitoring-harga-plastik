import pandas as pd

def main():
    oil = pd.read_csv("data/processed/oil_clean.csv")
    plastic = pd.read_csv("data/processed/plastic_clean.csv")
    usd = pd.read_csv("data/processed/usd_clean.csv")

    # pastikan datetime
    oil["date"] = pd.to_datetime(oil["date"])
    plastic["date"] = pd.to_datetime(plastic["date"])
    usd["date"] = pd.to_datetime(usd["date"])

    # merge pakai left join
    df = plastic.merge(oil, on="date", how="left") \
                .merge(usd, on="date", how="left")

    # isi missing value
    df = df.sort_values("date")
    df.fillna(method="ffill", inplace=True)

    df.to_csv("data/processed/final_dataset.csv", index=False)

if __name__ == "__main__":
    main()