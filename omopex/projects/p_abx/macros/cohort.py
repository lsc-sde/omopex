from sqlmesh import macro
from sqlmesh.core.macros import MacroEvaluator
from typing import Any
from omopex.macros.common import QueryGenerator

# Macros seem to only be able to get evaluator if they are within the project/macros folder and not in the root omopex/macros folder
# This needs further investigation


@macro()
def person_exists_in_cohort(evaluator: MacroEvaluator, model: str) -> Any:
    stg_schema = evaluator.var("stg_schema")

    return f"""
EXISTS(
    SELECT
      1
    FROM {stg_schema}.stg_cohort AS c
    WHERE
      c.person_id = {model}.person_id
  )
"""


@macro()
def concept_exists_in_shard(evaluator: MacroEvaluator, model: str, column: str) -> str:
    stg_schema = evaluator.var("stg_schema")

    return f"""
EXISTS(
    SELECT
      1
    FROM {stg_schema}.stg_vocab_shard AS svs
    WHERE
      svs.concept_id = {model}.{column}
  )
"""


@macro()
def calculate_vocab_size(evaluator: MacroEvaluator) -> str:
    vocab_tables = [
        "concept_ancestor",
        "concept_class",
        "concept_relationship",
        "concept_synonym",
        "concept",
        "domain",
        "relationship",
        "source_to_concept_map",
        "vocabulary",
    ]

    q = QueryGenerator(
        src_catalog=evaluator.var("src_catalog"),
        src_schema=evaluator.var("src_schema"),
        dest_schema=evaluator.var("dest_schema"),
    )

    return q.generate_vocab_size_query()
