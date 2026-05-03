from datetime import datetime, timedelta
import sys

from airflow import DAG
from airflow.operators.python import PythonOperator

# Folder scripts di-mount ke /opt/airflow/scripts
sys.path.append("/opt/airflow/scripts")

# ingestion
from ingestion.plastic import main as scrape_plastic
from ingestion.oil import main as scrape_oil
from ingestion.usd import main as scrape_usd

# processing
from processing.clean import main as clean_data
from processing.merge import main as merge_data
from processing.feature import main as feature_engineering

# database
from db.load import main as load_to_db


default_args = {
    "owner": "talitha",
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


with DAG(
    dag_id="commodity_pipeline",
    description="Pipeline monitoring harga plastik, minyak, kurs USD, processing data, dan load ke PostgreSQL",
    default_args=default_args,
    start_date=datetime(2025, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["commodity", "plastic", "airflow"],
) as dag:

    scrape_plastic_task = PythonOperator(
        task_id="scrape_plastic",
        python_callable=scrape_plastic,
    )

    scrape_oil_task = PythonOperator(
        task_id="scrape_oil",
        python_callable=scrape_oil,
    )

    scrape_usd_task = PythonOperator(
        task_id="scrape_usd",
        python_callable=scrape_usd,
    )

    clean_data_task = PythonOperator(
        task_id="clean_data",
        python_callable=clean_data,
    )

    merge_data_task = PythonOperator(
        task_id="merge_data",
        python_callable=merge_data,
    )

    feature_engineering_task = PythonOperator(
        task_id="feature_engineering",
        python_callable=feature_engineering,
    )

    load_to_postgres_task = PythonOperator(
        task_id="load_to_postgres",
        python_callable=load_to_db,
    )

    [scrape_plastic_task, scrape_oil_task, scrape_usd_task] >> clean_data_task
    clean_data_task >> merge_data_task >> feature_engineering_task >> load_to_postgres_task