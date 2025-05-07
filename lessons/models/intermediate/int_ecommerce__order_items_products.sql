WITH products AS (
	SELECT
		product_id,
		department AS product_department,
		cost AS product_cost,
		retail_price AS product_retail_price

	FROM {{ ref('stg_ecommerce__products') }}
)

SELECT

	-- IDs
	order_items.order_item_id,
	order_items.order_id,
	order_items.user_id,
	order_items.product_id,

	-- Order item data
	order_items.item_sale_price,

	-- Product data
	products.product_department,
	products.product_cost,
	products.product_retail_price,

	-- Calculated fields
	order_items.item_sale_price - products.product_cost AS item_profit,
	products.product_retail_price - order_items.item_sale_price AS item_discount

FROM {{ ref('stg_ecommerce__order_items') }} AS order_items
LEFT JOIN products ON order_items.product_id = products.product_id
