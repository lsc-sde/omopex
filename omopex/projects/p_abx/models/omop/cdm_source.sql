MODEL (
  name @dest_schema.cdm_source,
  kind FULL,
  cron '@monthly'
);

WITH cte AS (
  SELECT
    vocabulary_version
  FROM @src_catalog.@src_schema.vocabulary
  WHERE
    vocabulary_id = 'None'
)
SELECT
  @settings.cfg_cdm_source.dm_source_name AS cdm_source_name,
  @settings.cfg_cdm_source.cdm_source_abbreviation AS cdm_source_abbreviation,
  @settings.cfg_cdm_source.cdm_holder AS cdm_holder,
  @settings.cfg_cdm_source.source_description AS source_description,
  @settings.cfg_cdm_source.source_documentation_reference AS source_documentation_reference,
  @settings.cfg_cdm_source.cdm_etl_reference AS cdm_etl_reference,
  CURRENT_DATE AS source_release_date,
  CURRENT_DATE AS cdm_release_date,
  @settings.cfg_cdm_source.cdm_version AS cdm_version,
  (
    SELECT
      coalesce(vocabulary_version, 'Unknown') AS vocabulary_version
    FROM cte
  ) AS vocabulary_version,
  75626 AS cdm_version_concept_id
