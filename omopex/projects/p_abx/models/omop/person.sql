MODEL (
  name @dest_schema.person,
  kind VIEW,
  cron '@yearly'
);

/* This is the patient table. */
SELECT
  p.person_id,
  p.gender_concept_id,
  p.year_of_birth::INT,
  p.month_of_birth::INT,
  1 AS day_of_birth,
  p.race_concept_id,
  p.ethnicity_concept_id,
  p.location_id,
  p.provider_id,
  p.care_site_id,
  NULL AS person_source_value,
  NULL AS gender_source_value,
  NULL AS gender_source_concept_id,
  NULL AS race_source_value,
  NULL AS race_source_concept_id,
  NULL AS ethnicity_source_value,
  NULL AS ethnicity_source_concept_id
FROM @src_catalog.@src_schema.person AS p
WHERE
  @person_exists_in_cohort('p')
