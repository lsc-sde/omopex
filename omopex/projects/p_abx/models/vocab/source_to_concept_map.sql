MODEL (
  name @dest_schema.source_to_concept_map,
  kind VIEW,
  cron '@yearly'
);

SELECT
  stcm.source_code,
  stcm.source_concept_id,
  stcm.source_vocabulary_id,
  stcm.source_code_description,
  stcm.target_concept_id,
  stcm.target_vocabulary_id,
  stcm.valid_start_date,
  stcm.valid_end_date,
  stcm.invalid_reason
FROM @src_catalog.@src_schema.source_to_concept_map AS stcm
