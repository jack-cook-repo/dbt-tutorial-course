
    
    



select shipped_at
from (select * from `local-snow-464514-v3`.`dbt_minas`.`stg_ecommerce__orders` where delivered_at IS NOT NULL OR status = 'Shipped') dbt_subquery
where shipped_at is null


