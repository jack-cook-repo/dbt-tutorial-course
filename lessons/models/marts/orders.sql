

WITH

order_item_measures as (
    SELECT
    order_id,
    SUM(item_sale_price) AS total_sale_price,
    SUM(product_cost) as total_product_cost,
    SUM(item_profit) as total_profit,
    SUM(item_discount) as total_discount
    from {{ref('int_ecommerce__order_items_products')}}
    group by 1
)


    SELECT
    --data from staging
    od.order_id,
    od.created_at AS order_created_at,
    od.shipped_at AS order_shipped_at,
	od.delivered_at AS order_delivered_at,
	od.returned_at AS order_returned_at,
	od.status AS order_status,
	od.num_of_item,
    --data from 
	om.total_sale_price,
	om.total_product_cost,
	om.total_profit,
	om.total_discount,

FROM {{ref('stg_ecommerce__orders')}} as od 
left join order_item_measures om
    ON od.order_id = om.order_id