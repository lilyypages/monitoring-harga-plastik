import pandas as pd
from sqlalchemy import create_engine

def main():
    df = pd.read_csv("data/processed/feature_dataset.csv")

    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5434/plastic_db"
    )

    df.to_sql("plastic_prices", engine, if_exists="replace", index=False)

    print("✅ Data berhasil masuk ke PostgreSQL")

if __name__ == "__main__":
    main()