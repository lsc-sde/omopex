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
)
from sqlmesh.core.config.format import FormatConfig
from pydantic import BaseModel


# Local duckdb

dkdb = DuckDBConnectionConfig(database="../data/idril.duckdb")
dkdb_state = DuckDBConnectionConfig(database="../data/sqlmesh_state.duckdb")

gateway_local = GatewayConfig(
    connection=dkdb,
    state_connection=dkdb_state,
    state_schema="omopex",
    variables={"catalog_source": "idril"},
)

# Databricks
dbrks = DatabricksConnectionConfig(
    server_hostname=os.getenv("DATABRICKS_SERVER_HOSTNAME"),
    http_path=os.getenv("DATABRICKS_HTTP_PATH"),
    catalog=os.getenv("DATABRICKS_CATALOG"),
    concurrent_tasks=os.getenv("DATABRICKS_CONCURRENT_TASKS"),
    access_token=os.getenv("DATABRICKS_ACCESS_TOKEN"),
)

dbrks_state = PostgresConnectionConfig(
    host=os.getenv("STATE_DB_HOST"),
    port=os.getenv("STATE_DB_PORT"),
    user=os.getenv("STATE_DB_USER"),
    password=os.getenv("STATE_DB_PASSWORD"),
    database=os.getenv("STATE_DB_DATABASE"),
)

gateway_dbrks = GatewayConfig(
    connection=dbrks, state_connection=dbrks_state, state_schema="omopex"
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
        "local": gateway_local,
    }
    default_gateway: str = "dbrks"
    variables: dict
    format: FormatConfig = format_config
