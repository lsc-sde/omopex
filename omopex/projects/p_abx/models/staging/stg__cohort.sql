MODEL (
  name @stg_schema.z__cohort,
  kind VIEW,
  cron '@monthly'
);

SELECT DISTINCT
  person_id
FROM @src_catalog.@src_schema.drug_exposure AS de
JOIN @stg_schema.cs_drug AS cs_d
  ON cs_d.conceptid = de.drug_concept_id
