MODEL (
  name @dest_schema.drug_exposure,
  kind VIEW,
  cron '@daily'
);

SELECT
  de.drug_exposure_id,
  de.person_id,
  de.drug_concept_id,
  de.drug_exposure_start_date,
  de.drug_exposure_start_datetime,
  de.drug_exposure_end_date,
  de.drug_exposure_end_datetime,
  de.verbatim_end_date,
  de.drug_type_concept_id,
  de.stop_reason,
  de.refills,
  de.quantity,
  de.days_supply,
  de.sig,
  de.route_concept_id,
  de.lot_number,
  de.provider_id,
  de.visit_occurrence_id,
  de.visit_detail_id,
  de.drug_source_value,
  de.drug_source_concept_id,
  de.route_source_value,
  de.dose_unit_source_value
FROM @src_catalog.@src_schema.drug_exposure AS de
WHERE
  @person_exists_in_cohort('de')
