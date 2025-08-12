



select
    1
from (select * from `local-snow-464514-v3`.`dbt_minas`.`stg_ecommerce__orders` where delivered_at IS NOT NULL AND shipped_at IS NOT NULL) dbt_subquery

where not(delivered_at >= shipped_at)

