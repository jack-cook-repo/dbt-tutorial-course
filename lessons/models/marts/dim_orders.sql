with orders as (
	select *

	from {{ ref('stg_ecommerce__orders') }}
),

order_items_products as (
	select *

	from {{ ref('int_ecommerce__order_items_products')}}
),

order_items_measures as (
	select
		order_id,
		sum(item_sale_price) as total_sale_price,
		sum(product_cost) as total_product_cost,
		sum(item_profit) as total_profit,
		sum(item_discount) as total_discount

	from order_items_products

	group by 1
),

final as (
	select
		o.order_id,
		o.created_at as order_created_at,
		o.returned_at as order_returned_at,
		o.shipped_at as order_shipped_at,
		o.delivered_at as order_delivered_at,
		o.status as order_status,
		o.num_of_item as num_items_ordered,
		oim.total_sale_price,
		oim.total_product_cost,
		oim.total_profit,
		oim.total_discount

	from orders o
	left join order_items_measures oim
		on oim.order_id = o.order_id
)

select * from final