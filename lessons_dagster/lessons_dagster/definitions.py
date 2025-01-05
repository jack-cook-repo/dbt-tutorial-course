from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import lessons_dbt_assets, process_data, incremental_dbt_models
from .project import lessons_project
from .schedules import schedules
from .jobs import lessons_job

defs = Definitions(
    assets=[lessons_dbt_assets,incremental_dbt_models,process_data],
    schedules=schedules,
    jobs=[lessons_job],
    resources={
        "dbt": DbtCliResource(project_dir=lessons_project)
    },
)