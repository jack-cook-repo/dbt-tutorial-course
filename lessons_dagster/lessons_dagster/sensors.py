import os
from dagster import run_status_sensor, DagsterRunStatus, RunRequest, JobSelector, SkipReason, RunStatusSensorContext

from .jobs import (
    staging_job,
    lessons_job
)

@run_status_sensor(
    name='sensor_lessons_job',
    run_status=DagsterRunStatus.SUCCESS,
    monitored_jobs=[JobSelector(
    location_name='lessons_dagster',
    job_name='staging_job',
    )],
    request_job=lessons_job
)
def sensor_lessons_job(context: RunStatusSensorContext):
    run_id = context.dagster_run.run_id
    return RunRequest(tags={f"parent_job_id": f"{run_id}"})
