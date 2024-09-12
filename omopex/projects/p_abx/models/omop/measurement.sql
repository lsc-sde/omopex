MODEL (
  name @dest_schema.measurement,
  kind VIEW,
  cron '@daily'
);

SELECT
  m.measurement_id::INT,
  m.person_id::INT,
  m.measurement_concept_id::INT,
  m.measurement_date::DATE,
  m.measurement_datetime::DATETIME,
  m.measurement_time::TIME,
  m.measurement_type_concept_id::INT,
  m.operator_concept_id::INT,
  m.value_as_number::REAL,
  m.value_as_concept_id::INT,
  m.unit_concept_id::INT,
  m.range_low::REAL,
  m.range_high::REAL,
  m.provider_id::INT,
  m.visit_occurrence_id::BIGINT,
  m.visit_detail_id::BIGINT,
  m.measurement_source_value::TEXT,
  m.measurement_source_concept_id::INT,
  m.unit_source_value::TEXT,
  m.unit_source_concept_id::INT,
  m.value_source_value::TEXT,
  m.meas_event_field_concept_id::INT,
  m.measurement_event_id::TEXT
/* m.unique_key::TEXT, */ /* m.datasource::TEXT, */ /* m.updated_at::DATETIME */
FROM @src_catalog.@src_schema.measurement AS m /* WHERE */ /*   m.measurement_datetime BETWEEN @start_ds AND @end_ds */
