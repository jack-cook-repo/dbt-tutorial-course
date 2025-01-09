import os
from dagster import define_asset_job, job, AssetSelection
from dagster_dbt import build_dbt_asset_selection
from .assets import lessons_dbt_assets, process_data

dbt_staging = build_dbt_asset_selection(
    [lessons_dbt_assets],
    dbt_select='fqn:staging'
)

dbt_intermediate = build_dbt_asset_selection(
    [lessons_dbt_assets],
    dbt_select='fqn:intermediate'
)

dbt_marts = build_dbt_asset_selection(
    [lessons_dbt_assets],
    dbt_select='fqn:marts'
)

staging_job = define_asset_job(  
    name="staging_job",
    selection=dbt_staging,
    tags={
        "dbt_cli_command": "build"
    }
)

lessons_job = define_asset_job(  
    name="lessons_job",
    selection=dbt_intermediate | dbt_marts,
    tags={
        "dbt_cli_command": "build"
    }
)


