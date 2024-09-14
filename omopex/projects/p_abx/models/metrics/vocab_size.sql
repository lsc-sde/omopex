MODEL (
  name @stg_schema.metrics__vocab_size,
  kind FULL,
  cron '@yearly'
);

SELECT
  catalog_schema::TEXT,
  table_name::TEXT,
  n::INT
FROM (
  @calculate_vocab_size()
) AS t
