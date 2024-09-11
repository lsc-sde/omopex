# OMOP Medallion Project Specific ETL

__Data Science Team, Lancashire Teaching Hospitals NHS Foundation Trust__

## Introduction

This repository has the transformations, tests and snapshots for generating project specific models
from either the silver or gold layers of OMOP Medallion.

The source layer must be OMOP v5.4 conformant including all the clinical and vocabulary tables as a minimum.
Avoid non-OMOP models where possible.

The project-specific target layer should ideally be OMOP-conformant too but in selected instances may only contain a subset of these tables.

Additional supporting models that extend the OMOP CDM can be included in exceptional cases.

## Instructions

1. Please read the SQLMesh documentation <https://sqlmesh.readthedocs.io/> for futher information.
2. Clone this repository, create a new python environment (>=3.11) and install the requirements with `pip install -e .[dev]`
3. Setup the `.env` file by copying `.env.sample`, renaming it and modifying the values appropriately.
4. Review the `config.py` file within a project directory which tells SQLMesh what it needs to do.

Alternatively, it is a lot easier to run this using the provided _devcontainer_ setup.

## Folder structure

This repo is setup to manage multiple SQLMesh projects with a single set of configurations that need to be customised per project.

Please see `omopex/slices/p_abx/config.py` for an example of how this is done.

Each new project will need to be created as a sub-folder within `omopex\slices` and the folder name will be used as the schema where the data models will be materialises in the database / lakehouse.

To plan and apply changes to models in a particular project run `sqlmesh -p omopex/projects/<project_dir> plan`

Please see [SQLMesh multi-repo](https://sqlmesh.readthedocs.io/en/stable/guides/multi_repo/) guide for more information.

## Developing in Isolated Systems

We recommend developing and testing against synthetic or anonymised sample of real data in a local system using DuckDb before executing against a production system.

Please read the SQLMesh guide here -> https://sqlmesh.readthedocs.io/en/stable/guides/isolated_systems/ for more information, with particular attention to the difference between _systems_ and _environments_.
