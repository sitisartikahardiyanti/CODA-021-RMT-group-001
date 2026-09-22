import os
import pandas as pd
from sqlalchemy import create_engine
 
# Path hasil dari transform yang akan digunakan untuk load ke NeonDB
transform_result = "/opt/airflow/data/transform_result"

# Isi NEONDB_CONNECTION di file .env dengan connection string yang didapat dari NeonDB
CONNECTION_STRING = os.environ.get("NEON_CONNECTION_STRING")

print("DEBUG - NEON_CONNECTION_STRING:", repr(CONNECTION_STRING))
print("DEBUG - Semua env var yang mengandung 'NEON':",
      {k: repr(v) for k, v in os.environ.items() if "NEON" in k.upper()})
print("DEBUG - Semua env var yang mengandung 'KAGGLE':",
      {k: repr(v) for k, v in os.environ.items() if "KAGGLE" in k.upper()})
 
if not CONNECTION_STRING:
    raise ValueError("NEON_CONNECTION_STRING tidak ditemukan. Pastikan sudah diisi di file .env")
 

engine = create_engine(CONNECTION_STRING)

# Insert data ke NeonDB
## Urutannya harus dari dimensi dulu baru fact, karena fact membutuhkan ID dari masing-masing dimension

## dim_pekerjaan
df = pd.read_csv(f"{transform_result}/dim_pekerjaan.csv")
df.to_sql("dim_pekerjaan", con=engine, if_exists="replace", index=False)
print(f"Load selesai: dim_pekerjaan ({len(df)} baris)")
 
## dim_perusahaan
df = pd.read_csv(f"{transform_result}/dim_perusahaan.csv")
df.to_sql("dim_perusahaan", con=engine, if_exists="replace", index=False)
print(f"Load selesai: dim_perusahaan ({len(df)} baris)")
 
## dim_lokasi
df = pd.read_csv(f"{transform_result}/dim_lokasi.csv")
df.to_sql("dim_lokasi", con=engine, if_exists="replace", index=False)
print(f"Load selesai: dim_lokasi ({len(df)} baris)")
 
## fact_gaji_pekerjaan
df = pd.read_csv(f"{transform_result}/fact_gaji_pekerjaan.csv")
df.to_sql("fact_gaji_pekerjaan", con=engine, if_exists="replace", index=False)
print(f"Load selesai: fact_gaji_pekerjaan ({len(df)} baris)")
 
print("\nSemua tabel berhasil di-load ke NeonDB")