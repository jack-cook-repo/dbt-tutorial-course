WITH products AS
(SELECT
product_id,
department As product_dep,
cost AS product_cost,
retail_price AS product_retail_price
FROM {{ref('stg_ecommerce_products')}}
)

select
order_id,
order_item_id,
user_id,
p.product_id as product_id,
o.product_id as order_product_id,
sale_price,
product_cost,
product_retail_price,
p.product_dep,
ROUND(p.product_retail_price - o.sale_price,4) AS item_discount

from {{ref('stg_ecommerce_order_items')}} o
join
products p
on o.product_id = p.product_id
