import os
from dagster import define_asset_job, job, AssetSelection
from dagster_dbt import build_dbt_asset_selection
from .assets import lessons_dbt_assets, process_data

dbt_selection = build_dbt_asset_selection(
    [lessons_dbt_assets],
    dbt_select='fqn:*'
)

dbt_staging = build_dbt_asset_selection(
    [lessons_dbt_assets],
    dbt_select='fqn:staging'
)

lessons_job = define_asset_job(  
    name="lessons_job",
    selection=AssetSelection.all() - dbt_staging,
    tags={
        "dbt_cli_command": "build"
    }
)


