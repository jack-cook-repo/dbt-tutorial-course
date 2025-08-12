
    
    



select returned_at
from (select * from `local-snow-464514-v3`.`dbt_minas`.`stg_ecommerce__orders` where status = 'Returned') dbt_subquery
where returned_at is null


