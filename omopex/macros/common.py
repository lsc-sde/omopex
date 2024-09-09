from sqlmesh import macro, SQL, ExecutionContext
from sqlmesh.core.macros import MacroEvaluator, RuntimeStage
import sqlglot.expressions as exp
from typing import Any


@macro()
def some_macro_common_for_all_projects(evaluator: MacroEvaluator, key: str) -> Any:

    return "'this is a common macro'"
