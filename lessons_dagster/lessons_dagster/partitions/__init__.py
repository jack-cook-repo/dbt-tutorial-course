from dagster import MonthlyPartitionsDefinition, WeeklyPartitionsDefinition
from ..constants import *

start_date = START_DATE
end_date = END_DATE

monthly_partition = MonthlyPartitionsDefinition(
    start_date=start_date,
    end_date=end_date
)

weekly_partition = WeeklyPartitionsDefinition(
    start_date=start_date,
    end_date=end_date
)