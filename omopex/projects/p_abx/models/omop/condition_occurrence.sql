MODEL (
  name @dest_schema.condition_occurrence,
  kind VIEW,
  cron '@daily',
  );

SELECT
  co.condition_occurrence_id,
  co.person_id,
  co.condition_concept_id,
  co.condition_start_date,
  co.condition_start_datetime,
  co.condition_end_date,
  co.condition_end_datetime,
  co.condition_type_concept_id,
  co.condition_status_concept_id,
  co.stop_reason,
  co.provider_id,
  co.visit_occurrence_id,
  co.visit_detail_id,
  co.condition_source_value,
  co.condition_source_concept_id,
  co.condition_status_source_value
FROM @src_catalog.@src_schema.condition_occurrence AS co
WHERE
  EXISTS(
    SELECT
      1
    FROM @stg_schema.stg_cohort AS c
    WHERE
      c.person_id = co.person_id
  )
