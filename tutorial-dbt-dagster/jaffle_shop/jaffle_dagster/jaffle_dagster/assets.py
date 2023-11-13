import os
from pathlib import Path

from dagster import AssetExecutionContext, op, job, Definitions, OpExecutionContext, ResourceDefinition
from dagster_dbt import DbtCliResource, dbt_assets

from .constants import dbt_manifest_path

# Existing dbt assets definition
@dbt_assets(manifest=dbt_manifest_path)
def jaffle_shop_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()

@op(required_resource_keys={'dbt'})
def run_dbt_build_with_stage_tag(context):
    # Execute the dbt build command for models with the 'stage' tag
    context.resources.dbt.cli(["build", "--select", "tag:stage"]).wait()

dbt_project_dir = Path(__file__).resolve().parents[3].joinpath('jaffle_shop')

@job(resource_defs={'dbt': ResourceDefinition.hardcoded_resource(DbtCliResource(project_dir=dbt_project_dir))})
def run_dbt_build_stage_tag_job():
    run_dbt_build_with_stage_tag()
# # Get the absolute path to the dbt project directory
# dbt_project_dir = Path(__file__).resolve().parents[3].joinpath('jaffle_shop')

# dbt = DbtCliResource(project_dir=os.fspath(dbt_project_dir))

# # New dbt operation for running models with tag 'stage'
# @op
# def run_dbt_stage_models(context: AssetExecutionContext, dbt: DbtCliResource):
#     dbt.cli(["run", "--models", "tag:stage"]).wait()

# @op
# def run_dbt_tests(dbt: DbtCliResource):
#     # Run dbt tests
#     dbt.cli(["test"]).wait()

# # Define jobs for each operation
# @job(resource_defs={'dbt': DbtCliResource})
# def run_stage_models_job():
#     run_dbt_stage_models()

# @job(resource_defs={'dbt': DbtCliResource})
# def run_dbt_tests_job():
#     run_dbt_tests()
