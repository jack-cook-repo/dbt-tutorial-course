from dagster import AssetExecutionContext, AssetKey, asset
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator

from .project import lessons_project
from .constants import *

class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):

    def get_group_name(self, dbt_resource_props):
        rt = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        parts = name.lower().split('_')
        if rt in ("model"):
            return f"{parts[0]}"
        else:
            return super().get_group_name(dbt_resource_props)

@dbt_assets(manifest=lessons_project.manifest_path, dagster_dbt_translator=CustomizedDagsterDbtTranslator())
def lessons_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build", "--target", "qa"], context=context).stream()


@asset(
    deps=["dim_orders"],description="This asset processes some important data"
)
def process_data():
     return "Some processing here!"
    
