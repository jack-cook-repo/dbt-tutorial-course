from dagster import Definitions
from dagster_dbt import DbtCliResource
from .assets import lessons_dbt_assets
from .project import lessons_project
from .schedules import schedules

defs = Definitions(
    assets=[lessons_dbt_assets],
    schedules=schedules,
    resources={
        "dbt": DbtCliResource(project_dir=lessons_project),
    },
)