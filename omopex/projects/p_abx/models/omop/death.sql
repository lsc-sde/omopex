MODEL (
  name @dest_schema.death,
  kind VIEW,
  cron '@monthly',
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
  EXISTS(
    SELECT
      1
    FROM @stg_schema.z__cohort AS c
    WHERE
      c.person_id = d.person_id
  )
