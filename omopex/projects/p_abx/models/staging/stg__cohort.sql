MODEL (
  name @stg_schema.stg_cohort,
  kind VIEW,
  cron '@daily'
);

SELECT DISTINCT
  person_id
FROM @src_catalog.@src_schema.drug_exposure AS de
JOIN @stg_schema.cs_drug AS cs_d
  ON cs_d.conceptid = de.drug_concept_id
