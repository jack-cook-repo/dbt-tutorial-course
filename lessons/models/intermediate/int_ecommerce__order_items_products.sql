with order_items as (
	select *
	from {{ ref('stg_ecommerce__order_items') }}
),

products as (
	select *
	from {{ ref('stg_ecommerce__products') }}
),

final as (
	select
		order_items.order_item_id,
		order_items.order_id,
		order_items.user_id,
		order_items.product_id,
		order_items.item_sale_price,
		products.department as product_department,
		products.cost as product_cost,
		products.retail_price as product_retail_price,

		order_items.item_sale_price - products.cost as item_profit,
		products.retail_price - order_items.item_sale_price as item_discount

	from order_items
	left join products
		on products.product_id = order_items.product_id
)

select * from final