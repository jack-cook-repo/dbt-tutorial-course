
    
    

with all_values as (

    select
        status as value_field,
        count(*) as n_records

    from `local-snow-464514-v3`.`dbt_minas`.`stg_ecommerce__orders`
    group by status

)

select *
from all_values
where value_field not in (
    'Processing','Cancelled','Shipped','Complete','Returned'
)


