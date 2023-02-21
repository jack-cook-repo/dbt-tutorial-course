WITH source AS (
	SELECT *

	FROM {{ source('thelook_ecommerce', 'products') }}
)

SELECT
	-- IDs
	id AS product_id,

	-- Other columns
	cost,
	name,
	retail_price,
	department,
	sku

	{# Unused columns:
		- distribution_center_id
		- inventory_item_id
		- category
		- brand
	#}
	--,

FROM source
