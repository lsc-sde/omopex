from typing import Any
from datetime import datetime

from sqlmesh import ExecutionContext, model
from sqlmesh.core.model import ModelKindName
import pandas as pd


# Importing config creates an obscure error. Import variables instead.
from omopex.projects.p_abx.config import variables


stg_schema = variables.get("stg_schema")
model_name = f"{stg_schema}.stg_vocab_shard"


@model(
    name=model_name,
    kind=ModelKindName.FULL,
    columns={
        "concept_id": "bigint",
    },
)
def execute(
    context: ExecutionContext,
    start: datetime,
    end: datetime,
    execution_time: datetime,
    **kwargs: Any,
) -> pd.DataFrame:

    non_vocab_tables = [
        "condition_occurrence",
        "cdm_source",
        "condition_era",
        "cost",
        "death",
        "device_exposure",
        "drug_era",
        "drug_exposure",
        "measurement",
        "observation_period",
        "observation",
        "payer_plan_period",
        "person",
        "procedure_occurrence",
        "provider",
        "visit_detail",
        "visit_occurrence",
    ]

    tables = ",".join(f"'{t}'" for t in non_vocab_tables)

    src_catalog = variables.get("src_catalog")
    dest_catalog = "vvcb"
    # print(config)
    src_schema = variables.get("src_schema")
    dest_schema = context.var("dest_schema")

    df_concept_columns: pd.DataFrame = context.fetchdf(
        query=f"""
        select
            table_catalog,
            table_schema,
            table_name,
            column_name
        from information_schema.columns as c
        where
            c.table_catalog = '{dest_catalog}'
            and c.table_schema = '{dest_schema}'
            and c.table_name in ({tables})
            and c.column_name like '%_concept_id'
            """
    )

    concept_ids = []
    queries = []
    for row in df_concept_columns.itertuples():
        # print("Getting distinct concept_ids for ", row.column_name)
        query: str = (
            f"select distinct {row.column_name} as concept_id from {row.table_catalog}.{row.table_schema}.{row.table_name}"
        )
        queries.append(query)

    query = " UNION ".join(queries)

    final_query = f"""
    with cte_concept_ids as ({query}),
    distinct_concept_ids as (select distinct concept_id from cte_concept_ids),
    all_concept_ids as (
        select descendant_concept_id as concept_id
        from {src_catalog}.{src_schema}.concept_ancestor ca
        join distinct_concept_ids dci
        on dci.concept_id = ca.ancestor_concept_id
        union
        select ca.ancestor_concept_id as concept_id
        from {src_catalog}.{src_schema}.concept_ancestor ca
        join distinct_concept_ids dci
        on  dci.concept_id = ca.descendant_concept_id
        union
        select concept_id from distinct_concept_ids dci
        )
    select distinct concept_id from all_concept_ids
    """
    df = context.fetchdf(final_query).dropna()
    return df
