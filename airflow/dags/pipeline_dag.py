from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

from scripts.ingestion.plastic import main as scrape_plastic
from scripts.ingestion.oil import main as scrape_oil
from scripts.ingestion.usd import main as scrape_usd

with DAG(
    dag_id="commodity_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="plastic", python_callable=scrape_plastic)
    t2 = PythonOperator(task_id="oil", python_callable=scrape_oil)
    t3 = PythonOperator(task_id="usd", python_callable=scrape_usd)