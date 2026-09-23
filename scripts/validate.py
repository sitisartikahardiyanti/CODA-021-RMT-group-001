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


def validate_data(df):
    """Validate the transformed job salary DataFrame with Great Expectations.

    Raises:
        ValueError: If one or more expectations fail. This makes the
        validation task fail when called from an Airflow DAG.

    Returns:
        list: Great Expectations validation results when all checks pass.
    """

    # GX context
    context = gx.get_context()

    # Connect Pandas DataFrame to GX
    data_source = context.data_sources.add_pandas(
        name="job_salary_source"
    )
    data_asset = data_source.add_dataframe_asset(
        name="job_salary_asset"
    )
    batch_definition = data_asset.add_batch_definition_whole_dataframe(
        name="job_salary_batch"
    )
    batch = batch_definition.get_batch(
        batch_parameters={"dataframe": df}
    )

    # Define expectations
    expectations = [
        # A. Required columns must exist
        gx.expectations.ExpectTableColumnsToMatchSet(
            column_set=[
                "ID Pekerjaan",
                "Judul Pekerjaan",
                "Perusahaan",
                "Lokasi",
                "Gaji_Rata2",
                "Kategori Pekerjaan",
            ]
        ),

        # B. Important columns must not contain null values
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="Judul Pekerjaan"
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="Perusahaan"
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="Lokasi"
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="Gaji_Rata2"
        ),
        gx.expectations.ExpectColumnValuesToNotBeNull(
            column="Kategori Pekerjaan"
        ),

        # C. Salary must be positive and within reasonable range
        gx.expectations.ExpectColumnValuesToBeBetween(
            column="Gaji_Rata2",
            min_value=0,
            max_value=100_000_000,
        ),

        # D. Job category must follow predefined taxonomy
        gx.expectations.ExpectColumnValuesToBeInSet(
            column="Kategori Pekerjaan",
            value_set=ALLOWED_JOB_CATEGORIES,
        ),

        # E. Row count sanity check
        gx.expectations.ExpectTableRowCountToBeBetween(
            min_value=10_000,
            max_value=35_000,
        ),
    ]

    # Run validation
    validation_results = []

    for expectation in expectations:
        result = batch.validate(expectation)
        validation_results.append(result)

    # Print validation summary
    print("=" * 70)
    print("GREAT EXPECTATIONS - DATA VALIDATION RESULT")
    print("=" * 70)

    passed = 0
    failed = 0

    for i, result in enumerate(validation_results, start=1):
        expectation_name = result.expectation_config.type
        status = "PASSED" if result.success else "FAILED"

        if result.success:
            passed += 1
        else:
            failed += 1

        print(f"{i}. {expectation_name}")
        print(f"   Status: {status}")

        if hasattr(result, "result") and result.result:
            unexpected_count = result.result.get(
                "unexpected_count", None
            )
            unexpected_percent = result.result.get(
                "unexpected_percent", None
            )

            if unexpected_count is not None:
                print(
                    f"   Unexpected Count: {unexpected_count}"
                )

            if unexpected_percent is not None:
                print(
                    f"   Unexpected Percent: "
                    f"{unexpected_percent:.2f}%"
                )

        print("-" * 70)

    print("\nVALIDATION SUMMARY")
    print("=" * 70)
    print(f"Total Expectations : {len(validation_results)}")
    print(f"Passed             : {passed}")
    print(f"Failed             : {failed}")

    if failed == 0:
        print("\nAll data validation checks PASSED.")
    else:
        raise ValueError(
            f"Data validation failed: {failed} of "
            f"{len(validation_results)} expectations failed."
        )

    return validation_results
