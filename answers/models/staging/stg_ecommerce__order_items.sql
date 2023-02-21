WITH source AS (
	SELECT *

	FROM {{ source('thelook_ecommerce', 'order_items') }}
)

SELECT
	-- IDs
	id AS order_item_id,
	order_id,
	user_id,
	product_id,

	-- Timestamps
	created_at,
	shipped_at,
	delivered_at,
	returned_at,

	-- Other columns
	status,
	sale_price AS item_sale_price

	{# Unused columns:
		- inventory_item_id
		- gender
	#}

FROM source
