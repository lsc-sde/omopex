from sqlmesh import macro, SQL, ExecutionContext
from sqlmesh.core.macros import MacroEvaluator, RuntimeStage
import sqlglot.expressions as exp
from typing import Any
from datetime import datetime

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
