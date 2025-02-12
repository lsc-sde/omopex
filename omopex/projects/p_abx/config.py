import logging
import os
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import find_dotenv, load_dotenv
from pydantic import BaseModel, ConfigDict, Field, computed_field
from sqlmesh.core.config import (
    Config,
    DatabricksConnectionConfig,
    DuckDBConnectionConfig,
    GatewayConfig,
    ModelDefaultsConfig,
    MSSQLConnectionConfig,
    PostgresConnectionConfig,
)
from sqlmesh.core.config.format import FormatConfig
from sqlmesh.core.config.ui import UIConfig
from sqlmesh.core.model import ModelKindName

load_dotenv(find_dotenv(), override=True)

###############################################################################
# SQLMESH CONFIGURATION
###############################################################################

project = Path(__file__).parent.stem


class EnumGateway(str, Enum):
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


class EnumMedallionLayer(str, Enum):
    BASE = os.getenv(
        f"{os.getenv('DEFAULT_GATEWAY', default='duckdb').upper()}_SCHEMA_BASE", "base"
    )
    BRONZE = "bronze"
    SILVER = "silver"
    GOLD = "gold"


state_schema: str = os.getenv("STATE_SCHEMA", "stroma")
default_gateway: str = os.getenv("DEFAULT_GATEWAY", EnumGateway.DUCKDB)

gateways = {}

# Setup gateways
# For each gateway, first check if it is enabled.
# This avoids reading in env variables that may not exist or looking for libraries that are not installed

enabled_gateways = [
    i.strip().lower() for i in os.getenv("ENABLED_GATEWAYS", "duckdb").split(",")
]

# Make sure default gateway is in enabled
assert default_gateway in enabled_gateways, AssertionError(
    f"Default gateway set to {default_gateway} but not in enabled in {enabled_gateways}. Check your environment variables."
)

# Local duckdb
if EnumGateway.DUCKDB in enabled_gateways:
    try:
        database = str(Path(os.environ["DUCKDB_DATABASE"]).resolve())
        state_database = str(Path(os.environ["DUCKDB_STATE_DATABASE"]).resolve())

        gateway_duckdb = GatewayConfig(
            connection=DuckDBConnectionConfig(database=database),
            state_connection=DuckDBConnectionConfig(database=state_database),
            state_schema=state_schema,
        )

        gateways["duckdb"] = gateway_duckdb

    except Exception as e:
        logging.error(
            f"Error setting up DuckDb gateway.  Ensure all environment variables are set correctly. {e}"
        )

# Databricks
if EnumGateway.DATABRICKS in enabled_gateways:
    try:
        gateway_databricks = GatewayConfig(
            connection=DatabricksConnectionConfig(
                server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],
                http_path=os.environ["DATABRICKS_HTTP_PATH"],
                catalog=os.environ["DATABRICKS_CATALOG"],
                concurrent_tasks=os.getenv("DATABRICKS_CONCURRENT_TASKS", default=4),
                access_token=os.environ["DATABRICKS_ACCESS_TOKEN"],
            ),
            state_connection=PostgresConnectionConfig(
                host=os.environ["DATABRICKS_STATE_DB_HOST"],
                port=os.environ["DATABRICKS_STATE_DB_PORT"],
                user=os.environ["DATABRICKS_STATE_DB_USER"],
                password=os.environ["DATABRICKS_STATE_DB_PASSWORD"],
                database=os.environ["DATABRICKS_STATE_DB_DATABASE"],
            ),
            state_schema=state_schema,
        )

        gateways["databricks"] = gateway_databricks

    except Exception as e:
        logging.error(
            f"Error setting up Databricks gateway. Ensure all environment variables are set correctly. {e}"
        )


# MSSQL
if EnumGateway.MSSQL in enabled_gateways:
    try:
        gateway_mssql = GatewayConfig(
            connection=MSSQLConnectionConfig(
                host=os.environ["MSSQL_HOST"],
                database=os.environ["MSSQL_DATABASE"],
                concurrent_tasks=os.getenv("MSSQL_CONCURRENT_TASKS", default=4),
            ),
            state_connection=MSSQLConnectionConfig(
                host=os.environ["MSSQL_STATE_DB_HOST"],
                database=os.environ["MSSQL_STATE_DB_DATABASE"],
            ),
            state_schema=state_schema,
        )

        gateways["mssql"] = gateway_mssql
    except Exception as e:
        logging.error(
            f"Error setting up MS SQL Server gateway. Ensure all environment variables are set correctly. {e}"
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

    model_config = ConfigDict(protected_namespaces=())

    project: str
    model_defaults: ModelDefaultsConfig = ModelDefaultsConfig(
        kind=ModelKindName.VIEW,
        dialect="duckdb",
        cron="@daily",
        owner="LTH DST",
        start="2024-01-01",
    )
    gateways: Dict[str, GatewayConfig] = gateways
    default_gateway: str = default_gateway
    variables: Dict[str, Any]
    format: FormatConfig = FormatConfig(
        append_newline=True,
        normalize=True,
        indent=2,
        normalize_functions="lower",
        leading_comma=False,
        max_text_width=80,
        no_rewrite_casts=False,
    )
    ui: UIConfig = UIConfig(format_on_save=True)


###############################################################################
# OMOP SETTINGS
###############################################################################


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

    vocab_schema: Optional[str] = "vocab"

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
        if default_gateway == EnumGateway.DATABRICKS:
            return os.getenv("DATABRICKS_CATALOG_SOURCE")
        elif default_gateway == EnumGateway.MSSQL:
            return os.getenv("MSSQL_DATABASE_SOURCE")
        elif default_gateway == EnumGateway.DUCKDB:
            return os.getenv("DUCKDB_DATABASE")

    @computed_field
    @property
    def src_schema(self) -> str:
        if default_gateway == EnumGateway.DATABRICKS:
            return os.getenv("DATABRICKS_SCHEMA_BASE")
        elif default_gateway == EnumGateway.MSSQL:
            return os.getenv("MSSQL_SCHEMA_BASE")
        elif default_gateway == EnumGateway.DUCKDB:
            return os.getenv("DUCKDB_SCHEMA_BASE")


variables = OMOPSettings(
    project=project,
    vocab_schema="lth_omop",
    settings={},
).model_dump(mode="json")


variables.update({"study_start_date": "2019-01-01"})
config = Config(**dict(SQLMeshSettings(project=project, variables=variables)))
