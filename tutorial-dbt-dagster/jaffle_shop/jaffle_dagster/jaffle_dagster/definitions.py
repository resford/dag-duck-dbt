import os

from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import jaffle_shop_dbt_assets
from .constants import dbt_project_dir
from .schedules import schedules

defs = Definitions(
    assets=[jaffle_shop_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)

@op(required_resource_keys={'dbt'})
def run_dbt_models_with_tag(context):
    # Replace 'your_tag' with the specific tag you want to filter by
    context.resources.dbt.run(models='tag:stage')

@job(resource_defs={'dbt': dbt_cli_resource})
def dbt_run_job():
    run_dbt_models_with_tag()