import os
from dagster import Definitions
from dagster_dbt import DbtCliResource

from .assets import jaffle_shop_dbt_assets,  run_dbt_build_stage_tag_job  #run_stage_models_job, run_dbt_tests_job,
from .constants import dbt_project_dir
from .schedules import schedules

defs = Definitions(
    assets=[jaffle_shop_dbt_assets],
    jobs=[run_dbt_build_stage_tag_job],  # Include the new jobs here run_stage_models_job, run_dbt_tests_job,
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=os.fspath(dbt_project_dir)),
    },
)
