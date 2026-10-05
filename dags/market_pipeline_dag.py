import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator

from src.run_pipeline import run_pipe

default_args = {
    "owner": "somers",
    "retries": 0,
}

with DAG(
    dag_id="market_pipeline_dag",
    default_args=default_args,
    description="Runs the market prices + rainfall pipeline",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["dsc3103"],
) as dag:

    run_pipeline_task = PythonOperator(
        task_id="run_pipeline",
        python_callable=run_pipe,
    )