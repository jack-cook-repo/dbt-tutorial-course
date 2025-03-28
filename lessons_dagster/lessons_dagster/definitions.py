from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import lessons_dbt_assets, incremental_dbt_models
from .project import lessons_project
from .schedules import schedules
from .jobs import staging_job, lessons_job
from .sensors import sensor_lessons_job

defs = Definitions(
    assets=[lessons_dbt_assets,incremental_dbt_models],
    schedules=schedules,
    jobs=[staging_job,lessons_job],
    sensors=[sensor_lessons_job],
    resources={
        "dbt": DbtCliResource(project_dir=lessons_project)
    },
)