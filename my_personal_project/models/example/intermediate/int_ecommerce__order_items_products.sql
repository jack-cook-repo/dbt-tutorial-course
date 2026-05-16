WITH products AS (
	SELECT
		product_id,
		name,
		category,
		department,
		cost,
		retail_price
	FROM {{ ref('stg_ecommerce__products') }}
)

SELECT
	-- Order item details
	oi.order_item_id,
	oi.order_id,
	oi.user_id,
	oi.sale_price,

	-- Product details
	p.name,
	p.category,
	p.department,
	p.cost,
	p.retail_price,

	-- Calculated field
	oi.sale_price - p.cost AS profit,
	p.retail_price - oi.sale_price AS item_discount

	FROM {{ ref('stg_ecommerce__order_items') }} AS oi
	LEFT JOIN products AS p
		ON oi.product_id = p.product_id