from pathlib import Path
from typing import Tuple, Type
from sqlmesh.core.config import Config


from omopex.settings import (
    SQLMeshSettings,
    OMOPSettings,
    CdmSourceSettings,
)

project = Path(__file__).parent.stem

cfg_cdm_source = CdmSourceSettings(
    cdm_source_name="IDRIL - Test/Demo Project",
    cdm_source_abbreviation="IDRIL-1-" + project.upper(),
)

variables = OMOPSettings(
    project=project,
    # src_catalog=os.getenv("DATABRICKS_CATALOG"),
    src_schema="gold",
    # dest_catalog=os.getenv("DATABRICKS_CATALOG"),
    settings={},
).model_dump(mode="json")


variables.update({"study_start_date": "2024-01-01"})
config = Config(**dict(SQLMeshSettings(project=project, variables=variables)))
