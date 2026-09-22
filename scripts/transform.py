import os
import re
import pandas as pd

# Hasil extract yang akan diread untuk di transform
extract_result = "/opt/airflow/data/extract_result/job_salary_raw.csv"

# Path lokasi penyimpanan hasil transform (Star Schema)
transform_result = "/opt/airflow/data/transform_result"

#########################################################################################################################################

# Function untuk mengelompokkan pekerjaan ke dalam kategori yang lebih umum
def kategorikan_pekerjaan(judul):
    judul = judul.lower()  # ubah ke huruf kecil supaya mudah dicocokkan

    # re.search(pola, judul) akan cari apakah "pola" ada di dalam judul
    if re.search(r'\b(manager|manajer\w*|supervisor|spv|kepala|direktur|director|leader|chief|head|ceo|cfo|coo|cto|vp)\b', judul):
        return 'Manajerial/Eksekutif'
    elif re.search(r'\b(personal assistant|executive assistant|secretary|sekretaris)\b|\badmin\w*\b', judul):
        return 'Administrasi/Sekretaris'
    elif re.search(r'\b(dosen|guru|teacher\w*|pengajar)\b', judul):
        return 'Pendidikan/Pengajaran'
    elif re.search(r'\b(sales\w*|telesales|telemarketing|marketing|business development|salesman|spg|spb|partnership)\b', judul):
        return 'Sales/Marketing'
    elif re.search(r'\b(software\w*|backend|front ?end|full ?stack|devops|programmer|cyber\w*|cloud|'
                    r'security analyst|security tester|security operation|presales security|system integrator|'
                    r'solution\w* architect\w*|enterprise architect\w*|it architecture|system architecture|laravel)\b', judul):
        return 'IT/Digital'
    elif re.search(r'\b(customer service|customer care|frontliner|front office)\b', judul):
        return 'Customer Service'
    elif re.search(r'\b(hrd|hrga|hr|recruitment|talent acquisition|general affair|human resource)\b', judul):
        return 'HR/Personalia'
    elif re.search(r'\b(bank\w*|asuransi|insurance|bancassurance|teller|financial advisor|relationship officer|relationship executive|relationship associate|financial consultant|agency relation\w*|verifikator|verificator|asset recovery)\b', judul):
        return 'Perbankan/Asuransi'
    elif re.search(r'\b(account\w*|akunting|finance|tax|pajak|audit\w*|controller|cost control)\b', judul):
        return 'Keuangan/Akuntansi'
    elif re.search(r'\b(warehouse\w*|gudang|logistik|logistic|driver|supir|pengemudi|kurir|inventory control|distribution|import staff|export staff|ppjk)\b', judul):
        return 'Logistik/Warehouse'
    elif re.search(r'\b(it|developer|digital|data analyst|system analyst|technical support|ai engineer|data engineer|network engineer|system engineer|server engineer|qa engineer)\b', judul):
        return 'IT/Digital'
    elif re.search(r'\bstreaming\b', judul):
        return 'Live Streaming/Kreator Konten'
    elif re.search(r'\b(produksi|production|quality control|quality assurance|qc inspector|operator|teknisi|technician|ppic)\b', judul):
        return 'Produksi/QC/Manufaktur'
    elif re.search(r'\b(dokter|perawat|farmasi|apoteker|kesehatan|hse|terapis wicara)\b', judul):
        return 'Kesehatan/K3'
    elif re.search(r'\b(store|toko|kasir|cashier|merchandiser|beauty advisor|beauty consultant)\b', judul):
        return 'Retail/Store'
    elif re.search(r'\b(purchasing|procurement)\b', judul):
        return 'Purchasing/Procurement'
    elif re.search(r'\b(legal|hukum|regulatory affair)\b', judul):
        return 'Legal'
    elif re.search(r'\b(designer|graphic|architect|arsitek|interior|creative)\b', judul):
        return 'Desain/Kreatif'
    elif re.search(r'\b(engineer\w*|drafter|maintenance|geologist|urban planner)\b', judul):
        return 'Engineering'
    elif re.search(r'\b(education counsellor|trainer|instructor|tutor)\b', judul):
        return 'Pendidikan/Pengajaran'
    elif re.search(r'\b(host|live streaming|kol|streamer|content creator|konten kreator|social media|video editor|videographer|vidiographer|copywriter|seo)\b', judul):
        return 'Live Streaming/Kreator Konten'
    elif re.search(r'\b(surveyor|estimator)\b', judul):
        return 'Survey/Estimasi'
    elif re.search(r'\b(collection|collector|penagihan)\b', judul):
        return 'Penagihan/Collection'
    elif re.search(r'\b(e-commerce|ecommerce|marketplace)\b', judul):
        return 'E-Commerce'
    elif re.search(r'\b(chef|barista|cook|waiter|waitress|chatime)\b', judul):
        return 'Kuliner/FnB'
    elif re.search(r'\b(mechanic|mekanik|otomotif|car inspector|foreman otomotif)\b', judul):
        return 'Otomotif/Bengkel'
    elif re.search(r'\b(security|satpam|komandan regu)\b', judul):
        return 'Keamanan/Security'
    elif re.search(r'\b(translator|interpreter|penerjemah)\b', judul):
        return 'Bahasa/Penerjemah'
    else:
        return 'Lainnya'

# Function untuk membersihkan nama perusahaan agar lebih konsisten
def bersihkan_nama_perusahaan(nama):
    nama = str(nama).strip()  # hilangkan spasi di awal dan akhir
    nama = re.sub(r'\s+', ' ', nama)  # rapikan spasi ganda
    nama = re.sub(r'^pt\.?\s*', 'PT ', nama, flags=re.IGNORECASE)  # PT/Pt/pt/PT./PT.X -> "PT "
    nama = re.sub(r'^cv\.?\s*', 'CV ', nama, flags=re.IGNORECASE)  # CV/Cv/cv/CV. -> "CV "
    nama = re.sub(r'\s*,\s*', ', ', nama)  # rapikan spasi sekitar koma
    nama = re.sub(r',?\s*Tbk\.?$', ', Tbk', nama, flags=re.IGNORECASE)  # standarkan penamaan Tbk
    return nama.strip(', ')

# Mulai Tahap Transform
def transform(df):

    # Drop Data Duplikat
    df.drop_duplicates(inplace=True)

    # Buat kolom bantu ID Pekerjaan & Pindahkan ke paling depan
    df['id_gaji_pekerjaan'] = range(1, len(df) + 1)
    kolom = list(df.columns)
    kolom.remove('id_gaji_pekerjaan')   
    kolom.insert(0, 'id_gaji_pekerjaan')
    df = df[kolom]

    # Rename semua kolom supaya lebih konsisten
    df.rename(columns={
        'Judul Pekerjaan' : 'judul_pekerjaan',
        'Perusahaan' : 'perusahaan',
        'Lokasi' : 'lokasi',
        'Gaji_Rata2' : 'gaji_rata2'
    }, inplace=True)

    # Membuat kolom baru "kategori_Pekerjaan" berdasarkan "judul_pekerjaan"
    df['kategori_pekerjaan'] = df['judul_pekerjaan'].apply(kategorikan_pekerjaan)

    # Memindahkan kolom "Kategori Pekerjaan" ke sebelah kolom "Judul Pekerjaan"
    kolom = list(df.columns)
    kolom.remove('kategori_pekerjaan')
    posisi = kolom.index('judul_pekerjaan') + 1
    kolom.insert(posisi, 'kategori_pekerjaan')
    df = df[kolom]

    # Merubah format penamaan Setiap Perusahaan
    df['perusahaan'] = df['perusahaan'].apply(bersihkan_nama_perusahaan)

    # Pembuatan Data Warehouse Schema - Star Schema

    ## dim_pekerjaan
    ### Ambil judul pekerjaan unik, buat id_pekerjaan sebagai identifier untuk setiap barisnya
    dim_pekerjaan = df[['judul_pekerjaan', 'kategori_pekerjaan']].drop_duplicates().reset_index(drop=True)
    dim_pekerjaan.insert(0, 'id_pekerjaan', range(1, len(dim_pekerjaan) + 1))

    ## dim_perusahaan
    ### Ambil nama perusahaan yang unik, buat id_perusahaan sebagai identifier untuk setiap barisnya
    dim_perusahaan = df[['perusahaan']].drop_duplicates().reset_index(drop=True)
    dim_perusahaan.insert(0, 'id_perusahaan', range(1, len(dim_perusahaan) + 1))

    ## dim_lokasi
    ### Ambil nama lokasi unik, buat id_lokasi sebagai identifier untuk setiap barisnya
    dim_lokasi = df[['lokasi']].drop_duplicates().reset_index(drop=True)
    dim_lokasi.insert(0, 'id_lokasi', range(1, len(dim_lokasi) + 1))

    ## fact_gaji_pekerjaan
    ### Join balik ke df menggunakan left join agar tidak hilang datanya dan fact punya ID dari masing-masing dimension
    fact_gaji_pekerjaan = df.merge(dim_pekerjaan, on='judul_pekerjaan', how='left')
    fact_gaji_pekerjaan = fact_gaji_pekerjaan.merge(dim_perusahaan, on='perusahaan', how='left')
    fact_gaji_pekerjaan = fact_gaji_pekerjaan.merge(dim_lokasi, on='lokasi', how='left')

    # Buang kolom teks yang sudah tergantikan oleh ID dimension-nya,
    fact_gaji_pekerjaan = fact_gaji_pekerjaan[
        ['id_gaji_pekerjaan', 'id_pekerjaan', 'id_perusahaan', 'id_lokasi', 'gaji_rata2']
    ]

    return {
        "dim_pekerjaan": dim_pekerjaan,
        "dim_perusahaan": dim_perusahaan,
        "dim_lokasi": dim_lokasi,
        "fact_gaji_pekerjaan": fact_gaji_pekerjaan,
    }


# Baca hasil extract
df = pd.read_csv(extract_result)

# Bersihkan data dan bangun star schema
tables = transform(df)

# Otomatis buat folder tujuan dulu kalau belum ada
os.makedirs(transform_result, exist_ok=True)

# Simpan keempat tabel ke folder transform_result
tables["dim_pekerjaan"].to_csv(f"{transform_result}/dim_pekerjaan.csv", index=False)
tables["dim_perusahaan"].to_csv(f"{transform_result}/dim_perusahaan.csv", index=False)
tables["dim_lokasi"].to_csv(f"{transform_result}/dim_lokasi.csv", index=False)
tables["fact_gaji_pekerjaan"].to_csv(f"{transform_result}/fact_gaji_pekerjaan.csv", index=False)

print("\nTransform selesai. Tabel Star Schema tersimpan di:", transform_result)
for nama, tabel in tables.items():
    print(f"- {nama}: {tabel.shape[0]} baris, {tabel.shape[1]} kolom")