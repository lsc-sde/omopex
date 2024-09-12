MODEL (
  name @dest_schema.provider,
  kind VIEW,
  cron '@daily'
);

SELECT
  p.provider_id,
  p.provider_name,
  p.npi,
  p.dea,
  p.specialty_concept_id,
  p.care_site_id,
  p.year_of_birth,
  p.gender_concept_id,
  p.provider_source_value,
  p.specialty_source_value,
  p.specialty_source_concept_id,
  p.gender_source_value,
  p.gender_source_concept_id
FROM @src_catalog.@src_schema.provider AS p
