from dagster import AssetExecutionContext, AssetKey, asset, get_dagster_logger
from dagster_dbt import DbtCliResource, dbt_assets, DagsterDbtTranslator

from .project import lessons_project
from .constants import *
from .partitions import monthly_partition

import json
INCREMENTAL_SELECTOR = "config.materialized:incremental"

class CustomizedDagsterDbtTranslator(DagsterDbtTranslator):

    def get_group_name(self, dbt_resource_props):
        rt = dbt_resource_props["resource_type"]
        name = dbt_resource_props["name"]
        parts = name.lower().split('_')
        if rt in ("model"):
            return f"{parts[0]}"
        else:
            return super().get_group_name(dbt_resource_props)

@dbt_assets(manifest=lessons_project.manifest_path, dagster_dbt_translator=CustomizedDagsterDbtTranslator(), exclude=INCREMENTAL_SELECTOR )
def lessons_dbt_assets(context: AssetExecutionContext, dbt: DbtCliResource):
    parent_job_id = 0
    if 'parent_job_id' in context.run.tags:
        parent_job_id = context.run.tags["parent_job_id"]
    context.log.info(f"Run attributes: {parent_job_id}" )  
    yield from dbt.cli(["build", "--target", "qa"], context=context).stream()

@dbt_assets(
    manifest=lessons_project.manifest_path,
    dagster_dbt_translator=CustomizedDagsterDbtTranslator(),
    select=INCREMENTAL_SELECTOR,     # select only models with INCREMENTAL_SELECTOR
    partitions_def=monthly_partition   # partition those models using monthly_partition
)
def incremental_dbt_models(
    context: AssetExecutionContext,
    dbt: DbtCliResource
):
    time_window = context.partition_time_window
    parent_job_id = 0
    if 'parent_job_id' in context.run.tags:
        parent_job_id = context.run.tags["parent_job_id"]
    context.log.info(f"Run attributes: {parent_job_id}" )  
    dbt_vars = {
        "min_date": time_window.start.strftime('%Y-%m-%d'),
        "max_date": time_window.end.strftime('%Y-%m-%d')
    }  

    yield from dbt.cli(["build", "--target", "qa", "--vars", json.dumps(dbt_vars)], context=context).stream()

@asset(
    deps=["dim_orders"],description="This asset processes some important data"
)
def process_data():
     return "Some processing here!"
    
