from pathlib import Path
from typing import Tuple, Type
from sqlmesh.core.config import Config

import os
from omopex.config.omop_config import (
    OMOPSettings,
    SourceShema,
    CdmSourceSettings,
    ModelSettings,
)
from omopex.config.sqlmesh_config import OmopExConfig
import json

project = Path(__file__).parent.stem

cfg_cdm_source = CdmSourceSettings(
    cdm_source_name="IDRIL - Antimicrobial Stewardship",
    cdm_source_abbreviation="IDRIL-1-" + project.upper(),
)
settings = {
    "cfg_visit_occurrence": {"start_date": "2018-01-01"},
    "cfg_cdm_source": dict(cfg_cdm_source.model_dump(mode="json")),
}
print(settings)
variables = OMOPSettings(
    project=project,
    src_catalog=os.getenv("DATABRICKS_CATALOG"),
    src_schema=SourceShema.GOLD,
    dest_catalog=os.getenv("DATABRICKS_CATALOG"),
    settings=settings,
)


config = Config(
    **dict(
        OmopExConfig(
            project=project,
            variables=variables.model_dump(mode="json"),
        )
    )
)
