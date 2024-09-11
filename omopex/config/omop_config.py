from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, computed_field
from typing import Optional
from datetime import date
from omopex.config.sqlmesh_config import default_gateway, DefaultGateway
import os

from enum import Enum


class TableSettings(BaseModel):
    include: Optional[bool] = True
    include_source_concepts: Optional[bool] = False
    concept_ids: Optional[int] = None


class EventSettings(TableSettings):
    start_date: Optional[str] = "2010-01-01"
    end_date: Optional[date] = None


class CareSiteSettings(TableSettings):
    pass


class CdmSourceSettings(BaseModel):
    cdm_source_name: Optional[str] = "IDRIL - Project Description"
    cdm_source_abbreviation: Optional[str] = "IDRIL-P_DESC"
    cdm_holder: Optional[str] = "LSC SDE"
    source_description: Optional[str] = "OMOP 5.4 CDM Gold"
    cdm_version: Optional[str] = "5.4"
    source_documentation_reference: Optional[str] = "https://omop-lsc.surge.sh/"
    cdm_etl_reference: Optional[str] = "https://omop-lsc.surge.sh/"


class ConditionEraSettings(EventSettings):
    pass


class ConditionOccurrenceSettings(EventSettings):
    pass


class CostSettings(EventSettings):
    pass


class DeathSettings(EventSettings):
    pass


class DeviceExposureSettings(EventSettings):
    pass


class DoseEraSettings(EventSettings):
    pass


class DrugEraSettings(EventSettings):
    pass


class DrugExposureSettings(EventSettings):
    pass


class DrugStrengthSettings(EventSettings):
    pass


class EpisodeEventSettings(EventSettings):
    pass


class EpisodeSettings(EventSettings):
    pass


class FactRelationshipSettings(EventSettings):
    pass


class LocationSettings(EventSettings):
    pass


class MeasurementSettings(EventSettings):
    pass


class NoteNlpSettings(EventSettings):
    include: bool = False


class NoteSettings(EventSettings):
    include: bool = False


class ObservationPeriodSettings(EventSettings):
    pass


class ObservationSettings(EventSettings):
    pass


class PayerPlanPeriodSettings(EventSettings):
    pass


class PersonSettings(EventSettings):
    truncate_birth_datetime: bool = True


class ProcedureOccurrenceSettings(EventSettings):
    pass


class ProviderSettings(TableSettings):
    pass


class SpecimenSettings(EventSettings):
    pass


class VisitDetailSettings(EventSettings):
    pass


class VisitOccurrenceSettings(EventSettings):
    pass


class SourceShema(str, Enum):
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


class ModelSettings(BaseModel):
    cfg_caresite: Optional[CareSiteSettings] = CareSiteSettings()
    cfg_cdm_source: Optional[CdmSourceSettings] = CdmSourceSettings()
    cfg_condition_era: Optional[ConditionEraSettings] = ConditionEraSettings()
    cfg_condition_occurrence: Optional[ConditionOccurrenceSettings] = (
        ConditionOccurrenceSettings()
    )
    cfg_cost: Optional[CostSettings] = CostSettings()
    cfg_death: Optional[DeathSettings] = DeathSettings()
    cfg_device_exposure: Optional[DeviceExposureSettings] = DeviceExposureSettings()
    cfg_dose_era: Optional[DoseEraSettings] = DoseEraSettings()
    cfg_drug_era: Optional[DrugEraSettings] = DrugEraSettings()
    cfg_drug_exposure: Optional[DrugExposureSettings] = DrugExposureSettings()
    cfg_drug_strength: Optional[DrugStrengthSettings] = DrugStrengthSettings()
    cfg_episode_event: Optional[EpisodeEventSettings] = EpisodeEventSettings()
    cfg_episode: Optional[EpisodeSettings] = EpisodeSettings()
    cfg_fact_relationship: Optional[FactRelationshipSettings] = (
        FactRelationshipSettings()
    )
    cfg_location: Optional[LocationSettings] = LocationSettings()
    cfg_measurement: Optional[MeasurementSettings] = MeasurementSettings()
    cfg_note_nlp: Optional[NoteNlpSettings] = NoteNlpSettings()
    cfg_note: Optional[NoteSettings] = NoteSettings
    cfg_observation_period: Optional[ObservationPeriodSettings] = (
        ObservationPeriodSettings()
    )
    cfg_observation: Optional[ObservationSettings] = ObservationSettings()
    cfg_payer_plan_period: Optional[PayerPlanPeriodSettings] = PayerPlanPeriodSettings()
    cfg_person: Optional[PersonSettings] = PersonSettings()
    cfg_procedure_occurrence: Optional[ProcedureOccurrenceSettings] = (
        ProcedureOccurrenceSettings()
    )
    cfg_provider: Optional[ProviderSettings] = ProviderSettings()
    cfg_specimen: Optional[SpecimenSettings] = SpecimenSettings()
    cfg_visit_detail: Optional[VisitDetailSettings] = VisitDetailSettings()
    cfg_visit_occurrence: Optional[VisitOccurrenceSettings] = VisitOccurrenceSettings()


class OMOPSettings(BaseSettings):
    project: str
    src_schema: Optional[SourceShema] = "gold"
    # dest_catalog: str
    # model_settings: Optional[ModelSettings] = ModelSettings()

    settings: Optional[dict]

    @computed_field
    @property
    def dest_schema(self) -> str:
        return self.project

    @computed_field
    @property
    def stg_schema(self) -> str:
        return "stg_" + self.dest_schema

    @computed_field
    @property
    def temp_schema(self) -> str:
        return "temp_" + self.dest_schema

    @computed_field
    @property
    def src_catalog(self) -> str:
        if default_gateway == DefaultGateway.DATABRICKS:
            return os.getenv("DATABRICKS_SOURCE_CATALOG")
        elif default_gateway == DefaultGateway.MSSQL:
            return os.getenv("MSSQL_SOURCE_DATABASE")
        elif default_gateway == DefaultGateway.DUCKDB:
            return os.getenv("DUCKDB_DATABASE")
