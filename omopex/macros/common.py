from sqlmesh import macro, SQL, ExecutionContext
from sqlmesh.core.macros import MacroEvaluator, RuntimeStage
import sqlglot.expressions as exp
from typing import Any
from datetime import datetime


class QueryGenerator:
    def __init__(self, src_catalog: str, src_schema: str, dest_schema: str):
        self.src_catalog = src_catalog
        self.src_schema = src_schema
        self.dest_schema = dest_schema

        self.vocab_tables = [
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
        self.non_vocab_tables = [
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

    def generate_vocab_size_query(self) -> str:
        source = f"{self.src_catalog}.{self.src_schema}"

        queries = []
        for s in [source, self.dest_schema]:
            for t in self.vocab_tables:
                q = f"""
                    select
                        '{s}' as catalog_schema,
                        '{t}' as table_name,
                        count(*) as n
                    from {s}.{t}
                    """
                queries.append(q)

        query = " UNION ".join(queries)

        return query
