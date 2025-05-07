WITH products AS (
	SELECT
		id ,
		department AS product_department,
		cost AS product_cost,
		retail_price AS product_retail_price

	FROM {{ ref('stg_ecommerce__products') }} --Refrerencing other data models 
)
SELECT

	-- IDs
	order_items.id AS order_item_id,
	order_items.order_id,
	order_items.user_id,
	order_items.product_id,

	-- Order item data
	order_items.sale_price AS item_sale_price,

	-- Product data
	product_department,
	product_cost,
	product_retail_price,

	-- Calculated fields
	order_items.sale_price - product_cost AS item_profit,
	product_retail_price - order_items.sale_price AS item_discount

FROM {{ ref('stg_ecommerce__order_items') }} AS order_items
LEFT JOIN products ON order_items.id = products.id