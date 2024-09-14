MODEL (
  name @dest_schema.concept_relationship,
  kind VIEW,
  cron '@yearly'
);

SELECT
  cr.concept_id_1,
  cr.concept_id_2,
  cr.relationship_id,
  cr.valid_start_date,
  cr.valid_end_date,
  cr.invalid_reason
FROM @src_catalog.@src_schema.concept_relationship AS cr
WHERE
  @concept_exists_in_shard('cr', 'concept_id_1')
  OR @concept_exists_in_shard('cr', 'concept_id_2')
