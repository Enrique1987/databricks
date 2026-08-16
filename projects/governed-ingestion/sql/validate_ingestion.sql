-- Databricks SQL validation queries for the governed ingestion project.
-- Bind the named parameter `target_table` to a three-part table name, for example:
-- main.governed_ingestion_dev.orders_raw

-- Gate 1: required metadata must be populated and rescued records must be visible.
SELECT
  COUNT(*) AS row_count,
  COUNT_IF(_ingestion_source_file IS NULL) AS missing_source_file_count,
  COUNT_IF(_ingestion_source_modified_at IS NULL) AS missing_source_time_count,
  COUNT_IF(_ingestion_recorded_at IS NULL) AS missing_ingestion_time_count,
  COUNT_IF(_rescued_data IS NOT NULL) AS rescued_record_count,
  CASE
    WHEN COUNT_IF(
      _ingestion_source_file IS NULL
      OR _ingestion_source_modified_at IS NULL
      OR _ingestion_recorded_at IS NULL
    ) = 0 THEN 'PASS'
    ELSE 'FAIL'
  END AS metadata_gate
FROM IDENTIFIER(:target_table);

-- Gate 2: source-level lineage supports reconciliation and replay decisions.
SELECT
  _ingestion_source_file,
  COUNT(*) AS record_count,
  MIN(_ingestion_source_modified_at) AS source_modified_at,
  MIN(_ingestion_recorded_at) AS first_recorded_at,
  MAX(_ingestion_recorded_at) AS last_recorded_at,
  COUNT_IF(_rescued_data IS NOT NULL) AS rescued_record_count
FROM IDENTIFIER(:target_table)
GROUP BY _ingestion_source_file
ORDER BY last_recorded_at DESC, _ingestion_source_file;

-- Investigation view: this is intentionally a diagnostic result, not a silent filter.
SELECT
  _ingestion_source_file,
  _ingestion_recorded_at,
  _rescued_data
FROM IDENTIFIER(:target_table)
WHERE _rescued_data IS NOT NULL
ORDER BY _ingestion_recorded_at DESC
LIMIT 100;
