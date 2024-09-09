MODEL (
  name  @dest_schema.relationship,
  kind VIEW,
  cron '@yearly'
);

SELECT
  r.relationship_id,
  r.relationship_name,
  r.is_hierarchical,
  r.defines_ancestry,
  r.reverse_relationship_id,
  r.relationship_concept_id
FROM @src_catalog.@src_schema.relationship AS r
