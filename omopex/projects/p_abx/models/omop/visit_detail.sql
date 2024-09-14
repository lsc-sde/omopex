MODEL (
  name @dest_schema.visit_detail,
  kind VIEW,
  cron '@daily'
);

SELECT
  vd.visit_detail_id,
  vd.person_id,
  vd.visit_detail_concept_id,
  vd.visit_detail_start_date,
  vd.visit_detail_start_datetime,
  vd.visit_detail_end_date,
  vd.visit_detail_end_datetime,
  vd.visit_detail_type_concept_id,
  vd.provider_id,
  vd.care_site_id,
  vd.visit_detail_source_value,
  vd.visit_detail_source_concept_id,
  vd.admitted_from_source_value,
  vd.discharged_to_source_value,
  vd.discharged_to_concept_id,
  vd.preceding_visit_detail_id,
  vd.parent_visit_detail_id,
  vd.visit_occurrence_id
FROM @src_catalog.@src_schema.visit_detail AS vd
WHERE
  vd.visit_detail_start_datetime BETWEEN @study_start_date AND CURRENT_DATE /* this doesn' t work yet.Hard code instead. */
  AND @person_exists_in_cohort('vd')
