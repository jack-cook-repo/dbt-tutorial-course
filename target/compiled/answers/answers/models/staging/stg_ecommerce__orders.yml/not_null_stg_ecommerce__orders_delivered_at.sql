
    
    



select delivered_at
from (select * from `local-snow-464514-v3`.`dbt_minas`.`stg_ecommerce__orders` where returned_at IS NOT NULL OR status = 'Complete') dbt_subquery
where delivered_at is null


