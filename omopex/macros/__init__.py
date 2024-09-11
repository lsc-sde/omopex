from sqlmesh import macro, SQL, ExecutionContext
import sqlglot.expressions as exp
from sqlglot import select, condition, case
from omopex.settings import CdmSourceSettings, OMOPSettings


@macro()
def build_cdm_source(evaluator: ExecutionContext) -> str:

    project: str = evaluator.var(var_name="project")
    settings: OMOPSettings = evaluator.var(var_name="settings")
    cfg_cdm_source: CdmSourceSettings = settings["cfg_cdm_source"]

    return f"""
    with cdm_source as (
        select '{cdm_source}' as cdm_source
    )
    """
