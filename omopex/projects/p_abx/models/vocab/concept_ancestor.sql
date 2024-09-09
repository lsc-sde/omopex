MODEL (
  name @dest_schema.concept_ancestor,
  kind VIEW,
  cron '@yearly'
);

SELECT
  ca.ancestor_concept_id,
  ca.descendant_concept_id,
  ca.min_levels_of_separation,
  ca.max_levels_of_separation
FROM @src_catalog.@src_schema.concept_ancestor AS ca
