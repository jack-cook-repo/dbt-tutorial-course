from dagster import AssetExecutionContext
from dagster_dbt import DbtCliResource, dbt_assets

from .project import lessons_project


@dbt_assets(manifest=lessons_project.manifest_path)
def lessons_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build", "--target", "qa"], context=context).stream()
    