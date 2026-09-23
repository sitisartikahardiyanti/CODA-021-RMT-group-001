import os
import json
import datetime as dt
import pandas as pd
import great_expectations as gx

ALLOWED_JOB_CATEGORIES = [
    "Manajerial/Eksekutif",
    "Sales/Marketing",
    "Lainnya",
    "Keuangan/Akuntansi",
    "Engineering",
    "Administrasi/Sekretaris",
    "IT/Digital",
    "Live Streaming/Kreator Konten",
    "Perbankan/Asuransi",
    "Produksi/QC/Manufaktur",
    "Pendidikan/Pengajaran",
    "Desain/Kreatif",
    "Logistik/Warehouse",
    "HR/Personalia",
    "Kesehatan/K3",
    "Bahasa/Penerjemah",
    "Retail/Store",
    "Purchasing/Procurement",
    "Customer Service",
    "Survey/Estimasi",
    "Penagihan/Collection",
    "Kuliner/FnB",
    "E-Commerce",
    "Legal",
    "Otomotif/Bengkel",
    "Keamanan/Security",
]

# Macam-macam Great Expectations validasi per tabel
EXPECTATION_PLAN = {
    "dim_pekerjaan": [
        # 1. Kolom yang wajib ada di dim_pekerjaan
        gx.expectations.ExpectTableColumnsToMatchSet(
            column_set=["id_pekerjaan", "judul_pekerjaan", "kategori_pekerjaan"]
        ),
        # 2. judul_pekerjaan tidak boleh kosong
        gx.expectations.ExpectColumnValuesToNotBeNull(column="judul_pekerjaan"),
        # 3. kategori_pekerjaan harus sesuai daftar kategori yang valid
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="kategori_pekerjaan", value_set=ALLOWED_JOB_CATEGORIES
        ),
        # 4. id_pekerjaan harus unik (primary key check)
        gx.expectations.ExpectColumnValuesToBeUnique(column="id_pekerjaan"),
    ],
    "dim_perusahaan": [
        # 5. Kolom yang wajib ada di dim_perusahaan
        gx.expectations.ExpectTableColumnsToMatchSet(
            column_set=["id_perusahaan", "perusahaan"]
        ),
        # 6. perusahaan tidak boleh kosong
        gx.expectations.ExpectColumnValuesToNotBeNull(column="perusahaan"),
        # 7. id_perusahaan harus unik (primary key check)
        gx.expectations.ExpectColumnValuesToBeUnique(column="id_perusahaan"),
    ],
    "dim_lokasi": [
        # 8. Kolom yang wajib ada di dim_lokasi
        gx.expectations.ExpectTableColumnsToMatchSet(
            column_set=["id_lokasi", "lokasi"]
        ),
        # 9. lokasi tidak boleh kosong
        gx.expectations.ExpectColumnValuesToNotBeNull(column="lokasi"),
        # 10. id_lokasi harus unik (primary key check)
        gx.expectations.ExpectColumnValuesToBeUnique(column="id_lokasi"),
    ],
    "fact_gaji_pekerjaan": [
        # 11. Kolom yang wajib ada di fact_gaji_pekerjaan
        gx.expectations.ExpectTableColumnsToMatchSet(
            column_set=["id_gaji_pekerjaan", "id_pekerjaan", "id_perusahaan", "id_lokasi", "gaji_rata2"]
        ),
        # 12. gaji_rata2 tidak boleh kosong
        gx.expectations.ExpectColumnValuesToNotBeNull(column="gaji_rata2"),
        # 13. gaji_rata2 harus positif dan dalam rentang wajar
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="gaji_rata2", min_value=0, max_value=100_000_000
        ),
        # 14. id_gaji_pekerjaan harus unik (primary key check)
        gx.expectations.ExpectColumnValuesToBeUnique(column="id_gaji_pekerjaan"),
        # 15. Jumlah baris harus dalam rentang wajar (sanity check)
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=10_000, max_value=35_000
        ),
    ],
}


def validate_data(tables):
    
    # Proses Validasi
    context = gx.get_context(mode="ephemeral") # GX kerja hanya di memori, tidak nulis folder config ke disk
    data_source = context.data_sources.add_pandas(name="job_salary_source")

    validation_results = []

    for nama_tabel, expectations in EXPECTATION_PLAN.items():
        df = tables[nama_tabel]

        data_asset = data_source.add_dataframe_asset(name=f"{nama_tabel}_asset")
        batch_definition = data_asset.add_batch_definition_whole_dataframe(
            name=f"{nama_tabel}_batch"
        )
        batch = batch_definition.get_batch(batch_parameters={"dataframe": df})

        for expectation in expectations:
            result = batch.validate(expectation)
            validation_results.append((nama_tabel, result))

    # Print keseluruhan hasil validasi ke console supaya bisa dibaca di log Airflow
    print("=" * 70)
    print("GREAT EXPECTATIONS - DATA VALIDATION RESULT")
    print("=" * 70)

    passed = 0
    failed = 0

    for i, (nama_tabel, result) in enumerate(validation_results, start=1):
        expectation_name = result.expectation_config.type
        status = "PASSED" if result.success else "FAILED"

        if result.success:
            passed += 1
        else:
            failed += 1

        print(f"{i}. [{nama_tabel}] {expectation_name}")
        print(f"   Status: {status}")

        if hasattr(result, "result") and result.result:
            unexpected_count = result.result.get("unexpected_count", None)
            unexpected_percent = result.result.get("unexpected_percent", None)

            if unexpected_count is not None:
                print(f"   Unexpected Count: {unexpected_count}")

            if unexpected_percent is not None:
                print(f"   Unexpected Percent: {unexpected_percent:.2f}%")

        print("-" * 70)

    print("\nVALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total Expectations : {len(validation_results)}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")

    # Proses simpan hasil ke .json
    if failed == 0:
        print("\nAll data validation checks PASSED.")
    validation_result_path = "/opt/airflow/data/validation_result"
    os.makedirs(validation_result_path, exist_ok=True)

    ringkasan = {
        "timestamp": dt.datetime.now().isoformat(),
        "total_expectations": len(validation_results),
        "passed": passed,
        "failed": failed,
        "detail": [
            {
                "nomor": i,
                "tabel": nama_tabel,
                "expectation": result.expectation_config.type,
                "status": "PASSED" if result.success else "FAILED",
                "hasil": result.to_json_dict().get("result", {}),
            }
            for i, (nama_tabel, result) in enumerate(validation_results, start=1)
        ],
    }

    with open(f"{validation_result_path}/validation_result.json", "w") as f:
        json.dump(ringkasan, f, indent=2, default=str)

    print(f"Hasil validasi tersimpan di: {validation_result_path}/validation_result.json")

    if failed > 0:
        raise ValueError(
            f"Data validation failed: {failed} of "
            f"{len(validation_results)} expectations failed."
        )

    return validation_results


# Load Data hasil Transform.py untuk divalidasi
transform_result = "/opt/airflow/data/transform_result"

tables = {
    "dim_pekerjaan": pd.read_csv(f"{transform_result}/dim_pekerjaan.csv"),
    "dim_perusahaan": pd.read_csv(f"{transform_result}/dim_perusahaan.csv"),
    "dim_lokasi": pd.read_csv(f"{transform_result}/dim_lokasi.csv"),
    "fact_gaji_pekerjaan": pd.read_csv(f"{transform_result}/fact_gaji_pekerjaan.csv"),
}

validate_data(tables)