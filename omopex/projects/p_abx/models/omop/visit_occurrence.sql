MODEL (
  name @dest_schema.visit_occurrence,
  kind VIEW,
  cron '@daily'
);

SELECT
  vo.visit_occurrence_id,
  vo.person_id,
  vo.visit_concept_id,
  vo.visit_start_date,
  vo.visit_start_datetime,
  vo.visit_end_date,
  vo.visit_end_datetime,
  vo.visit_type_concept_id,
  vo.provider_id,
  vo.care_site_id,
  vo.visit_source_value,
  vo.visit_source_concept_id,
  vo.admitted_from_concept_id,
  vo.admitted_from_source_value,
  vo.discharged_to_concept_id,
  vo.preceding_visit_occurrence_id,
  @project AS project
FROM @src_catalog.@src_schema.visit_occurrence AS vo
WHERE
  vo.visit_start_datetime BETWEEN @study_start_date AND CURRENT_DATE
  AND @person_exists_in_cohort('vo')
