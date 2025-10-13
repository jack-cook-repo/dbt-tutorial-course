
{{ config(materialized='table') }}
With source as 
(select * 
from {{source('thelook_ecommerce', 'orders')}} )
select 
    order_id,
    user_id,
    status,
    created_at,
    returned_at as returned  ,
    shipped_at as shipped ,
    delivered_at ,
    num_of_item as num_items_ordered
from source
