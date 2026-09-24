# Analisis Pasar Kerja Di Indonesia

## Latar Belakang
Perusahaan, job seeker, dan Human Resources (HR) membutuhkan informasi yang akurat mengenai variasi gaji pekerjaan di Indonesia berdasarkan posisi, perusahaan, dan lokasi. Informasi mengenai tingkat gaji dapat menjadi salah satu pertimbangan penting dalam proses rekrutmen, penentuan kompensasi, maupun pengambilan keputusan bagi pencari kerja dalam memilih peluang pekerjaan yang sesuai dengan kompetensi dan ekspektasi mereka.

Namun, banyaknya lowongan pekerjaan yang tersedia dengan posisi, perusahaan, lokasi, serta rentang kompensasi yang berbeda membuat pola dan perbedaan tingkat gaji di pasar kerja menjadi sulit untuk dipahami secara menyeluruh. Perbedaan gaji dapat terjadi antar posisi pekerjaan maupun antarwilayah, sehingga diperlukan analisis terhadap data lowongan pekerjaan untuk melihat bagaimana distribusi dan variasi gaji tersebut.

Selain itu, informasi mengenai perusahaan dan lokasi pekerjaan juga dapat memberikan gambaran mengenai karakteristik pasar kerja di Indonesia. Dengan menganalisis jumlah lowongan, posisi pekerjaan, perusahaan, lokasi, serta tingkat gaji, dapat diketahui pola tertentu yang terdapat dalam data, seperti posisi dengan jumlah lowongan terbanyak, posisi dengan rata-rata gaji tertinggi, wilayah dengan sebaran pekerjaan yang lebih besar, dan perbedaan tingkat gaji antarwilayah maupun perusahaan.

Oleh karena itu, analisis data lowongan pekerjaan diperlukan untuk memberikan gambaran yang lebih terstruktur mengenai kondisi gaji di pasar kerja Indonesia. Hasil analisis ini diharapkan dapat membantu perusahaan dan HR dalam memahami kondisi kompensasi serta membantu job seeker memperoleh informasi sebagai bahan pertimbangan dalam menentukan peluang pekerjaan yang sesuai.

## Problem Statement
Menganalisis data 32.976 job postings di Indonesia yang dikumpulkan pada tahun 2024 untuk mengidentifikasi pola dan variasi rata-rata gaji berdasarkan posisi pekerjaan, perusahaan, dan lokasi, serta menghasilkan dashboard yang dapat digunakan untuk memahami kondisi pasar gaji di Indonesia.

Analisa ini dapat digunakan untuk :
Prediksi gaji berdasarkan karakteristik pekerjaan.
Analisis pasar tenaga kerja di Indonesia.
Sistem rekomendasi karier bagi pencari kerja.
Analisis kompensasi dan HR berbasis data.
Analisis perbedaan gaji berdasarkan posisi, perusahaan, dan lokasi.

Secara keseluruhan dapat memberikan gambaran mengenai pola dan variasi gaji pekerjaan di Indonesia serta mendukung pengambilan keputusan yang berbasis data dalam bidang karier dan sumber daya manusia.

## Dataset Source
job_salary_mean :https://www.kaggle.com/datasets/husnind/indonesia-average-job-salary/data

## Data Pipeline
Membentuk data modeling dari dataset dengan menentukan dim dan fact table, kemudian  melakukakan extract dari sumber dataset, data cleaning dan transform, melakukan validasi dan melakukan load ke database NeonDB PostgreSQL. Proses ETL akan diautomasi menggunakan Airflow. Selanjutnya membuat data warehouse untuk kebutuhan analisa.

## Tools
* NeonDB PostgreSQL
* Airflow
* Docker
* Python
* Tableau

## Final Project RMT-021-Group-001
- Felix Ferdinand Laureng
- Anton Sujono
- Nur Nubli Muhamad
- Rolando Krisnanto
- Siti Sartika Hardiyanti

# Link Dashboard
https://public.tableau.com/app/profile/anton.sujono/viz/IndonesiaJobSalaryExplorer/IndonesiaJobSalaryExplorer?publish=yes

# Link Presentasi
https://docs.google.com/presentation/d/1-ZU-hGHbjaDS3wAiDeY7uHt7PFouNTjzRJFl6tIXo6o/edit?usp=sharing

