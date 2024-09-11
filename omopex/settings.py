from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

import os
from sqlmesh.core.config import (
    Config,
    ModelDefaultsConfig,
    GatewayConfig,
    DatabricksConnectionConfig,
    PostgresConnectionConfig,
    DuckDBConnectionConfig,
    MSSQLConnectionConfig,
)
from sqlmesh.core.config.format import FormatConfig
from sqlmesh.core.model import ModelKindName
from pydantic import BaseModel, computed_field, Field
from enum import Enum
from typing import Dict, Any, Optional
from datetime import date

###############################################################################
# SQLMESH CONFIGURATION
###############################################################################


class DefaultGateway(str, Enum):
    """
    Enumeration class representing the default gateway options.

    Attributes:
        DATABRICKS (str): Represents the Databricks gateway.
        MSSQL (str): Represents the MSSQL gateway.
        DUCKDB (str): Represents the DuckDB gateway.
    """

    DATABRICKS = "databricks"
    MSSQL = "mssql"
    DUCKDB = "duckdb"


state_schema: str = os.getenv("STATE_SCHEMA", "omopex")
default_gateway: str = os.getenv("DEFAULT_GATEWAY", DefaultGateway.DATABRICKS)

# Local duckdb

gateway_duckdb = GatewayConfig(
    connection=DuckDBConnectionConfig(database=os.getenv("DUCKDB_DATABASE")),
    state_connection=DuckDBConnectionConfig(
        database=os.getenv("DUCKDB_STATE_DATABASE")
    ),
    state_schema=state_schema,
    variables={"catalog_source": "idril"},
)

# Databricks

gateway_databricks = GatewayConfig(
    connection=DatabricksConnectionConfig(
        server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
        http_path=os.getenv("DATABRICKS_HTTP_PATH"),
        catalog=os.getenv("DATABRICKS_CATALOG"),
        concurrent_tasks=os.getenv("DATABRICKS_CONCURRENT_TASKS", 4),
        access_token=os.getenv("DATABRICKS_ACCESS_TOKEN"),
    ),
    state_connection=PostgresConnectionConfig(
        host=os.getenv("DATABRICKS_STATE_DB_HOST"),
        port=os.getenv("DATABRICKS_STATE_DB_PORT"),
        user=os.getenv("DATABRICKS_STATE_DB_USER"),
        password=os.getenv("DATABRICKS_STATE_DB_PASSWORD"),
        database=os.getenv("DATABRICKS_STATE_DB_DATABASE"),
    ),
    state_schema=state_schema,
)

print(gateway_databricks.model_dump())
# MSSQL

gateway_mssql = GatewayConfig(
    connection=MSSQLConnectionConfig(
        host=os.getenv("MSSQL_HOST"),
        database=os.getenv("MSSQL_DATABASE"),
        concurrent_tasks=os.getenv("MSSQL_CONCURRENT_TASKS", 4),
    ),
    state_connection=MSSQLConnectionConfig(
        host=os.getenv("MSSQL_STATE_DB_HOST"),
        database=os.getenv("MSSQL_STATE_DB_DATABASE"),
    ),
    state_schema=state_schema,
)


class SQLMeshSettings(BaseModel):
    """
    SQLMeshSettings class represents the settings for SQLMesh.

    Attributes:
        project (str): The name of the project.
        model_defaults (ModelDefaultsConfig): The configuration for model defaults.
        gateways (dict): A dictionary of gateways, where the keys are the gateway names and the values are the corresponding gateway functions.
        default_gateway (str): The name of the default gateway.
        variables (dict): A dictionary of variables.
        format (FormatConfig): The configuration for formatting.
    """

    project: str
    model_defaults: ModelDefaultsConfig = ModelDefaultsConfig(
        kind=ModelKindName.VIEW, dialect="duckdb", cron="@daily", owner="LTH DST"
    )
    gateways: Dict[str, GatewayConfig] = {
        "databricks": gateway_databricks,
        "mssql": gateway_mssql,
        "duckdb": gateway_duckdb,
    }
    default_gateway: str = default_gateway
    variables: Dict[str, Any]
    format: FormatConfig = FormatConfig(
        append_newline=True,
        normalize=True,
        indent=2,
        normalize_functions="lower",
        leading_comma=False,
        max_text_width=80,
    )


###############################################################################
# OMOP SETTINGS
###############################################################################


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
    source_release_date: Optional[date] = date.today()
    cdm_release_date: Optional[date] = date.today()
    vocabulary_version: Optional[str] = None


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


class OMOPSettings(BaseModel):
    """
    Represents the settings for OMOP project.

    Attributes:
        project (str): The name of the project.
        src_schema (Optional[SourceShema], optional): The source schema. Defaults to "gold".
        settings (Optional[dict], optional): Additional settings. Defaults to None.

    Computed Properties:
        dest_schema (str): The destination schema, which is the same as the project name.
        stg_schema (str): The staging schema, which is "stg_" + dest_schema.
        temp_schema (str): The temporary schema, which is "temp_" + dest_schema.
        src_catalog (str): The source catalog based on the default gateway.

    Methods:
        dest_schema() -> str: Returns the destination schema.
        stg_schema() -> str: Returns the staging schema.
        temp_schema() -> str: Returns the temporary schema.
        src_catalog() -> str: Returns the source catalog based on the default gateway.
    """

    project: str = Field(
        ...,
        description="The name of the project and should be unique across all projects and will be used as the target schema name. This defaults to the name of the project directory and should match the regex pattern `^p_[a-z0-9_]+$`.",
        examples=["p_abx", "p_copd", "p_diabetes"],
        pattern="^p_[a-z0-9_]+$",
    )
    src_schema: Optional[SourceShema | str] = SourceShema.GOLD
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
