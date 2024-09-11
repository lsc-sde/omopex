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
from pydantic import BaseModel
from enum import Enum


class DefaultGateway(str, Enum):
    DATABRICKS = "dbrks"
    MSSQL = "mssql"
    DUCKDB = "dkdb"


state_schema: str = os.getenv("STATE_SCHEMA", "omopex")
default_gateway: str = os.getenv("DEFAULT_GATEWAY", DefaultGateway.DATABRICKS)
# Local duckdb

dkdb = DuckDBConnectionConfig(database=os.getenv("DUCKDB_DATABASE"))
dkdb_state = DuckDBConnectionConfig(database=os.getenv("DUCKDB_STATE_DATABASE"))

gateway_local = GatewayConfig(
    connection=dkdb,
    state_connection=dkdb_state,
    state_schema="idril",
    variables={"catalog_source": "idril"},
)

# Databricks
dbrks = DatabricksConnectionConfig(
    server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    catalog=os.getenv("DATABRICKS_CATALOG"),
    concurrent_tasks=os.getenv("DATABRICKS_CONCURRENT_TASKS", 4),
    access_token=os.getenv("DATABRICKS_ACCESS_TOKEN"),
)

dbrks_state = PostgresConnectionConfig(
    host=os.getenv("DATABRICKS_STATE_DB_HOST"),
    port=os.getenv("DATABRICKS_STATE_DB_PORT"),
    user=os.getenv("DATABRICKS_STATE_DB_USER"),
    password=os.getenv("DATABRICKS_STATE_DB_PASSWORD"),
    database=os.getenv("DATABRICKS_STATE_DB_DATABASE"),
)

gateway_dbrks = GatewayConfig(
    connection=dbrks, state_connection=dbrks_state, state_schema=state_schema
)

# MSSQL

mssql = MSSQLConnectionConfig(
    host=os.getenv("MSSQL_HOST"),
    database=os.getenv("MSSQL_DATABASE"),
    concurrent_tasks=os.getenv("MSSQL_CONCURRENT_TASKS", 4),
)

mssql_state = MSSQLConnectionConfig(
    host=os.getenv("MSSQL_STATE_DB_HOST"),
    database=os.getenv("MSSQL_STATE_DB_DATABASE"),
)

gateway_mssql = GatewayConfig(
    connection=mssql, state_connection=mssql_state, state_schema=state_schema
)

format_config = FormatConfig(
    append_newline=True,
    normalize=True,
    indent=2,
    normalize_functions="lower",
    leading_comma=False,
    max_text_width=80,
)


class OmopExConfig(BaseModel):
    project: str
    model_defaults: ModelDefaultsConfig = ModelDefaultsConfig(dialect="duckdb")
    gateways: dict = {
        "dbrks": gateway_dbrks,
        "mssql": gateway_mssql,
        "local": gateway_local,
    }
    default_gateway: str = default_gateway
    variables: dict
    format: FormatConfig = format_config
