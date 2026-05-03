import os
import pandas as pd
from sqlalchemy import create_engine


def main():
    input_path = os.getenv(
        "FEATURE_DATASET_PATH",
        "/opt/airflow/data/processed/feature_dataset.csv"
    )

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"File tidak ditemukan: {input_path}")

    df = pd.read_csv(input_path)

    db_host = os.getenv("DB_HOST", "postgres")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "airflow")
    db_password = os.getenv("DB_PASSWORD", "airflow")
    db_name = os.getenv("DB_NAME", "airflow")

    engine = create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )

    df.to_sql(
        "plastic_prices",
        engine,
        if_exists="replace",
        index=False
    )

    print("✅ Data berhasil masuk ke PostgreSQL table: plastic_prices")
    print(f"✅ Jumlah baris: {len(df)}")


if __name__ == "__main__":
    main()