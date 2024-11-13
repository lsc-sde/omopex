MODEL (
  name @dest_schema.domain,
  kind VIEW,
  cron '@yearly'
);

SELECT
  d.domain_id,
  d.domain_name,
  d.domain_concept_id
FROM @src_catalog.@vocab_schema.domain AS d
