






    with grouped_expression as (
    select
        
        
    
  
( 1=1 and num_items_ordered >= 0
)
 as expression


    from `local-snow-464514-v3`.`dbt_minas`.`stg_ecommerce__orders`
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors







