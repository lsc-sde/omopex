MODEL (
  name @dest_schema.observation,
  kind VIEW,
  cron '@daily',
    );

SELECT
  o.observation_id,
  o.person_id,
  o.observation_concept_id,
  o.observation_date,
  o.observation_datetime,
  o.observation_type_concept_id,
  o.value_as_number,
  o.value_as_string,
  o.value_as_concept_id,
  o.qualifier_concept_id,
  o.unit_concept_id,
  o.provider_id,
  o.visit_occurrence_id,
  o.visit_detail_id,
  o.observation_source_value,
  o.observation_source_concept_id,
  o.unit_source_value,
  o.qualifier_source_value,
  o.value_source_value,
  o.observation_event_id,
  o.obs_event_field_concept_id,
  -- o.unique_key,
  -- o.datasource,
  -- o.updated_at
FROM @src_catalog.@src_schema.observation AS o
