MODEL (
  name  @dest_schema.vocabulary,
  kind VIEW,
  cron '@yearly'
);

SELECT
  v.vocabulary_id,
  v.vocabulary_name,
  v.vocabulary_reference,
  v.vocabulary_version,
  v.vocabulary_concept_id
FROM @src_catalog.@src_schema.vocabulary AS v
