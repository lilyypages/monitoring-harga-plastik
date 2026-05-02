import pandas as pd

def main():
    df = pd.read_csv("data/processed/final_dataset.csv")

    # pastikan urut
    df = df.sort_values("date")

    # lag (harga kemarin)
    df["plastic_lag_1"] = df["plastic_price"].shift(1)

    # moving average
    df["plastic_ma_3"] = df["plastic_price"].rolling(3).mean()

    # perubahan harga minyak
    df["oil_change"] = df["oil_price"].pct_change()

    # drop NA
    df.dropna(inplace=True)

    df.to_csv("data/processed/feature_dataset.csv", index=False)

if __name__ == "__main__":
    main()