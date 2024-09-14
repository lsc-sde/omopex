MODEL (
  name @dest_schema.specimen,
  kind VIEW,
  cron '@daily'
);

SELECT
  s.specimen_id,
  s.person_id,
  s.specimen_concept_id,
  s.specimen_type_concept_id,
  s.specimen_date,
  s.specimen_datetime,
  s.quantity,
  s.unit_concept_id,
  s.anatomic_site_concept_id,
  s.disease_status_concept_id,
  s.specimen_source_id,
  s.specimen_source_value,
  s.unit_source_value,
  s.anatomic_site_source_value,
  s.disease_status_source_value
FROM @src_catalog.@src_schema.specimen AS s
WHERE
  s.specimen_datetime BETWEEN @study_start_date AND CURRENT_DATE /* this doesn' t work yet.Hard code instead. */
  AND @person_exists_in_cohort('s')
