from sqlalchemy import create_engine

def get_engine():
    return create_engine(
        "postgresql+psycopg2://airflow:airflow@postgres:5432/airflow"
    )