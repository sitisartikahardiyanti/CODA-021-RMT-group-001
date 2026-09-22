import os
import pandas as pd
import kagglehub
from kagglehub import KaggleDatasetAdapter
 
# Path lokasi hasil extract yang nanti digunakan untuk transform.py
extract_result = "/opt/airflow/data/extract_result/job_salary_raw.csv"
 
# Path file yang ingin diambil dari dataset Kaggle
file_path = "job_salary_mean.csv"
 
 
def load_data():
    # Load dataset terbaru dari Kaggle via KaggleHub API
    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        "husnind/indonesia-average-job-salary",
        file_path,
    )
    return df
 
 
df = load_data()

# Otomatis buat folder tujuan dulu kalau belum ada
os.makedirs(os.path.dirname(extract_result), exist_ok=True)
 
# Simpan hasilnya ke file csv, supaya bisa dibaca oleh transform.py
df.to_csv(extract_result, index=False)
print(f"Data Extract berhasil disimpan di: {extract_result}")