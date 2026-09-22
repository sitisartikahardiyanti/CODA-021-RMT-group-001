import datetime as dt
from datetime import timedelta
 
from airflow import DAG
from airflow.operators.bash import BashOperator
 
# Konfigurasi default untuk DAG ini
default_args = {
    'owner': 'coda021_group1',  # siapa yang punya pipeline ini
    'start_date': dt.datetime(2025, 1, 1),  # tanggal mulai pipeline ini dijalankan
    'retries': 1,  # berapa kali jika gagal akan dicoba lagi
    'retry_delay': dt.timedelta(minutes=5),  # berapa lama menunggu sebelum mencoba lagi
}
 
 
with DAG('finalproject_coda021_group1_DAG',  # nama DAG
         default_args=default_args,
         schedule_interval='0,10,20,30 4 * * 1',  # tiap Senin jam 04:00
         catchup=False,  # supaya tidak terpengaruh start_date, dimulai dari sekarang
         ) as dag:
 
     # Extract (run extract.py) - Load Data dari Kaggle via KaggleHub API
    python_extract = BashOperator(
        task_id='extract',
        bash_command='sudo -u airflow python /opt/airflow/scripts/extract.py'
    )
 
    # Transform (run transform.py) - Data Cleaning + bangun Schema Data Warehouse
    python_transform = BashOperator(
        task_id='transform',
        bash_command='sudo -u airflow python /opt/airflow/scripts/transform.py'
    )
 
    # Load (run load.py) - masukkan Star Schema ke NeonDB
    python_load = BashOperator(
        task_id='load',
        bash_command='sudo -E -u airflow HOME=/home/airflow python /opt/airflow/scripts/load.py'
    )
 
# Urutan running (Extract -> Transform -> Load)
python_extract >> python_transform >> python_load