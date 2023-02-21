WITH orders AS (
	SELECT
		order_id,
		created_at AS order_created_at,
		returned_at AS order_returned_at,
		delivered_at AS order_delivered_at,
		shipped_at AS order_shipped_at,
		status AS order_status,
		returned_at IS NOT NULL AS has_order_been_returned,
		num_items_ordered

	FROM {{ ref('stg_ecommerce__orders' ) }}
),

order_items AS (
	SELECT
		order_id,
		product_id,
		item_sale_price

	FROM {{ ref('stg_ecommerce__order_items') }}
),

products AS (
	SELECT
		product_id,
		category AS product_category,
		name AS product_name,
		cost AS product_cost,
		retail_price AS product_retail_price,
		department AS product_department

	FROM {{ ref('stg_ecommerce__products') }}
)

SELECT

	-- IDs
	order_items.order_id,
	order_items.product_id,

	-- Order data
	orders.order_created_at,
	orders.order_returned_at,
	orders.order_delivered_at,
	orders.order_shipped_at,
	orders.order_status,
	orders.has_order_been_returned,
	orders.num_items_ordered,

	-- Order item data
	order_items.item_sale_price,

	-- Product data
	products.product_category,
	products.product_name,
	products.product_cost,
	products.product_retail_price,
	products.product_department,

	-- Calculated fields
	order_items.item_sale_price - products.product_cost AS item_profit,
	products.product_retail_price - order_items.item_sale_price AS item_discount

FROM order_items
LEFT JOIN orders ON order_items.order_id = orders.order_id
LEFT JOIN products ON order_items.product_id = products.product_id
