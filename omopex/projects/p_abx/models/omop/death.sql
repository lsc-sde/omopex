MODEL (
  name @dest_schema.death,
  kind VIEW,
  cron '@daily'
);

SELECT
  d.person_id,
  d.death_date,
  d.death_datetime,
  d.death_type_concept_id,
  d.cause_concept_id,
  d.cause_source_value,
  d.cause_source_concept_id
FROM @src_catalog.@src_schema.death AS d
WHERE
  @person_exists_in_cohort('d')
