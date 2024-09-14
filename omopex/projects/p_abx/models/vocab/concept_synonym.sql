MODEL (
  name @dest_schema.concept_synonym,
  kind VIEW,
  cron '@yearly'
);

SELECT
  cs.concept_id,
  cs.concept_synonym_name,
  cs.language_concept_id
FROM @src_catalog.@src_schema.concept_synonym AS cs
WHERE
  @concept_exists_in_shard('cs', 'concept_id')
