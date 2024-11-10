from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2022, 8, 9),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
        'process_sales',
        default_args=default_args,
        schedule_interval=None,
        catchup=False,
) as dag:
    def task_1_func(**context):
        # Retrieve date and raw_dir from DAG run configuration or use defaults
        date = context['dag_run'].conf.get('date', '2022-08-09')
        raw_dir = context['dag_run'].conf.get('raw_dir', '/app/data/2022-08-09')

        url = 'http://localhost:8081'
        headers = {'Content-Type': 'application/json'}
        data = {
            'date': date,
            'raw_dir': raw_dir
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.text


    def task_2_func(**context):
        # Retrieve raw_dir and stg_dir from DAG run configuration or use defaults
        raw_dir = context['dag_run'].conf.get('raw_dir', '/app/data/2022-08-09')
        stg_dir = context['dag_run'].conf.get('stg_dir', '/app/stage/2022-08-09')

        url = 'http://localhost:8082'
        headers = {'Content-Type': 'application/json'}
        data = {
            'raw_dir': raw_dir,
            'stg_dir': stg_dir
        }

        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return response.text


    task_1 = PythonOperator(
        task_id='task_1',
        python_callable=task_1_func,
        provide_context=True,
    )

    task_2 = PythonOperator(
        task_id='task_2',
        python_callable=task_2_func,
        provide_context=True,
    )

    task_1 >> task_2
