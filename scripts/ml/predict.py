import os
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error


DATA_PATH = os.getenv(
    "FEATURE_DATASET_PATH",
    "/opt/airflow/data/processed/feature_dataset.csv"
)

OUTPUT_PATH = os.getenv(
    "PREDICTION_OUTPUT_PATH",
    "/opt/airflow/data/processed/plastic_price_predictions.csv"
)

FORECAST_DAYS = int(os.getenv("FORECAST_DAYS", "30"))


def get_db_engine():
    db_host = os.getenv("DB_HOST", "postgres")
    db_port = os.getenv("DB_PORT", "5432")
    db_user = os.getenv("DB_USER", "airflow")
    db_password = os.getenv("DB_PASSWORD", "airflow")
    db_name = os.getenv("DB_NAME", "airflow")

    return create_engine(
        f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )


def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"File tidak ditemukan: {DATA_PATH}")

    df = pd.read_csv(DATA_PATH)

    required_cols = ["date", "plastic_price", "oil_price", "usd_idr"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        raise ValueError(f"Kolom wajib tidak ditemukan: {missing_cols}")

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    df["day_index"] = np.arange(len(df))

    if "plastic_lag_1" not in df.columns:
        df["plastic_lag_1"] = df["plastic_price"].shift(1)

    if "plastic_ma_3" not in df.columns:
        df["plastic_ma_3"] = df["plastic_price"].rolling(window=3).mean()

    if "oil_change" not in df.columns:
        df["oil_change"] = df["oil_price"].pct_change()

    if "usd_change" not in df.columns:
        df["usd_change"] = df["usd_idr"].pct_change()

    feature_cols = [
        "day_index",
        "oil_price",
        "usd_idr",
        "plastic_lag_1",
        "plastic_ma_3",
        "oil_change",
        "usd_change",
    ]

    df = df.dropna(subset=feature_cols + ["plastic_price"]).reset_index(drop=True)

    if len(df) < 10:
        raise ValueError(
            f"Data valid terlalu sedikit untuk forecasting. Data valid: {len(df)} baris."
        )

    return df, feature_cols


def train_model(df, feature_cols):
    X = df[feature_cols]
    y = df["plastic_price"]

    split_idx = int(len(df) * 0.8)

    X_train = X.iloc[:split_idx]
    X_test = X.iloc[split_idx:]
    y_train = y.iloc[:split_idx]
    y_test = y.iloc[split_idx:]

    model = LinearRegression()
    model.fit(X_train, y_train)

    mae = None
    rmse = None

    if len(X_test) > 0:
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    return model, mae, rmse


def average_daily_change(series, window=7):
    recent = series.dropna().tail(window + 1)

    if len(recent) < 2:
        return 0

    return float(recent.diff().dropna().mean())


def forecast_future(df, model, feature_cols):
    last_row = df.iloc[-1]
    last_date = pd.to_datetime(last_row["date"])

    last_day_index = int(last_row["day_index"])

    oil_price = float(last_row["oil_price"])
    usd_idr = float(last_row["usd_idr"])

    oil_daily_change = average_daily_change(df["oil_price"], window=7)
    usd_daily_change = average_daily_change(df["usd_idr"], window=7)

    previous_plastic_price = float(last_row["plastic_price"])
    recent_prices = list(df["plastic_price"].tail(3))

    predictions = []

    previous_oil_price = oil_price
    previous_usd_idr = usd_idr

    for day in range(1, FORECAST_DAYS + 1):
        prediction_date = last_date + timedelta(days=day)
        future_day_index = last_day_index + day

        # proyeksi sederhana untuk variabel eksternal
        oil_price = oil_price + oil_daily_change
        usd_idr = usd_idr + usd_daily_change

        oil_change = (
            (oil_price - previous_oil_price) / previous_oil_price
            if previous_oil_price != 0
            else 0
        )

        usd_change = (
            (usd_idr - previous_usd_idr) / previous_usd_idr
            if previous_usd_idr != 0
            else 0
        )

        plastic_lag_1 = previous_plastic_price
        plastic_ma_3 = sum(recent_prices[-3:]) / len(recent_prices[-3:])

        future_input = pd.DataFrame([{
            "day_index": future_day_index,
            "oil_price": oil_price,
            "usd_idr": usd_idr,
            "plastic_lag_1": plastic_lag_1,
            "plastic_ma_3": plastic_ma_3,
            "oil_change": oil_change,
            "usd_change": usd_change,
        }])

        predicted_price = float(model.predict(future_input[feature_cols])[0])

        predictions.append({
            "prediction_date": prediction_date.strftime("%Y-%m-%d"),
            "horizon_day": day,
            "predicted_price": round(predicted_price, 4),
            "forecast_oil_price": round(oil_price, 4),
            "forecast_usd_idr": round(usd_idr, 4),
            "model_name": "LinearRegression_with_trend_features",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        })

        previous_plastic_price = predicted_price
        recent_prices.append(predicted_price)

        previous_oil_price = oil_price
        previous_usd_idr = usd_idr

    return pd.DataFrame(predictions)


def save_predictions(pred_df):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    pred_df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8-sig")
    print(f"✅ File prediksi disimpan ke: {OUTPUT_PATH}")

    engine = get_db_engine()

    pred_df.to_sql(
        "plastic_price_predictions",
        engine,
        if_exists="replace",
        index=False,
    )

    print("✅ Data prediksi masuk ke PostgreSQL table: plastic_price_predictions")


def main():
    print("🚀 Start prediksi harga plastik...")

    df, feature_cols = load_data()
    model, mae, rmse = train_model(df, feature_cols)

    print("✅ Model training selesai")
    print(f"MAE  : {mae}")
    print(f"RMSE : {rmse}")

    pred_df = forecast_future(df, model, feature_cols)
    print(pred_df.head())

    save_predictions(pred_df)

    print("✅ Prediksi selesai.")


if __name__ == "__main__":
    main()