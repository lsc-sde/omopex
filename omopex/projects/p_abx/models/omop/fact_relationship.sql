MODEL (
  name @dest_schema.fact_relationship,
  kind VIEW,
  cron '@monthly',
  );

SELECT
  fr.domain_concept_id_1,
  fr.fact_id_1,
  fr.domain_concept_id_2,
  fr.fact_id_2,
  fr.relationship_concept_id
FROM @src_catalog.@src_schema.fact_relationship AS fr
