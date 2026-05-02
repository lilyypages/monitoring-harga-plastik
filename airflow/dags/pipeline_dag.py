from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# ingestion
from scripts.ingestion.plastic import main as scrape_plastic
from scripts.ingestion.oil import main as scrape_oil
from scripts.ingestion.usd import main as scrape_usd

# processing
from scripts.processing.clean import main as clean_data
from scripts.processing.merge import main as merge_data
from scripts.processing.feature import main as feature_engineering

# db
from scripts.db.load import main as load_to_db

# ml
from scripts.ml.train import main as train_model
from scripts.ml.predict import main as predict

with DAG(
    dag_id="commodity_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="plastic", python_callable=scrape_plastic)
    t2 = PythonOperator(task_id="oil", python_callable=scrape_oil)
    t3 = PythonOperator(task_id="usd", python_callable=scrape_usd)

    t4 = PythonOperator(task_id="clean", python_callable=clean_data)
    t5 = PythonOperator(task_id="merge", python_callable=merge_data)
    t6 = PythonOperator(task_id="feature", python_callable=feature_engineering)

    t7 = PythonOperator(task_id="load_db", python_callable=load_to_db)

    t8 = PythonOperator(task_id="train", python_callable=train_model)
    t9 = PythonOperator(task_id="predict", python_callable=predict)

    # FLOW
    [t1, t2, t3] >> t4 >> t5 >> t6 >> t7 >> t8 >> t9