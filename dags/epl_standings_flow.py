import os
import sys
from datetime import datetime

from airflow import DAG
from airflow.operators.python import PythonOperator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pipelines.epl_standings_pipeline import extract_and_transform_data, save_to_db

dag = DAG(
    dag_id='epl_standings_flow',
    default_args={
        "owner": "Chien Nguyen Nhu",
        "start_date": datetime(2024, 12, 20),
    },
    schedule_interval=None,
    catchup=False
)

extract_and_transform_data = PythonOperator(
    task_id="extract_and_transform",
    python_callable=extract_and_transform_data,
    provide_context=True,
    op_args={"https://onefootball.com/en/competition/premier-league-9/table"},
    dag=dag
)

save_to_db = PythonOperator(
    task_id='save_to_db',
    provide_context=True,
    python_callable=save_to_db,  
    dag=dag
)

extract_and_transform_data >> save_to_db
