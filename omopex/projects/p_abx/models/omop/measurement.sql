MODEL (
  name @dest_schema.measurement,
  kind VIEW,
  cron '@daily'
);

SELECT
  m.measurement_id::BIGINT,
  m.person_id::BIGINT,
  m.measurement_concept_id::BIGINT,
  m.measurement_date::DATE,
  m.measurement_datetime::DATETIME,
  m.measurement_time::TIME,
  m.measurement_type_concept_id::BIGINT,
  m.operator_concept_id::BIGINT,
  m.value_as_number::REAL,
  m.value_as_concept_id::BIGINT,
  m.unit_concept_id::BIGINT,
  m.range_low::REAL,
  m.range_high::REAL,
  m.provider_id::BIGINT,
  m.visit_occurrence_id::BIGINT,
  m.visit_detail_id::BIGINT,
  m.measurement_source_value::TEXT,
  m.measurement_source_concept_id::BIGINT,
  m.unit_source_value::TEXT,
  m.unit_source_concept_id::BIGINT,
  m.value_source_value::TEXT,
  m.meas_event_field_concept_id::BIGINT,
  m.measurement_event_id::TEXT
/* m.unique_key::TEXT, */ /* m.datasource::TEXT, */ /* m.updated_at::DATETIME */
FROM @src_catalog.@src_schema.measurement AS m
WHERE
  m.measurement_datetime BETWEEN @study_start_date AND CURRENT_DATE /* this doesn' t work yet.Hard code instead. */
  AND @person_exists_in_cohort('m')
