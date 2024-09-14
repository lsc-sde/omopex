from sqlmesh import macro, SQL, ExecutionContext
from sqlmesh.core.macros import MacroEvaluator, RuntimeStage
import sqlglot.expressions as exp
from typing import Any
from datetime import datetime


# @macro()
# def some_macro_common_for_all_projects(evaluator: MacroEvaluator, key: str) -> Any:

#     return "'this is a common macro'"


# @macro()
# def between_dates(evaluator: MacroEvaluator, model: str, column: str):
#     print(evaluator.runtime_stage)
#     settings = evaluator.var("cfg")

#     model_settings = settings.get("cfg_" + model)
#     if not model_settings:
#         raise KeyError(f"cfg_{model} settings not found in settings variable.")

#     start_date = model_settings.get("start_date")
#     end_date = model_settings.get("end_date")
#     if not start_date:
#         start_date = datetime(2010, 1, 1)
#     if not end_date:
#         end_date = datetime.today()
#     return f"{column} between {start_date} and {end_date}"
