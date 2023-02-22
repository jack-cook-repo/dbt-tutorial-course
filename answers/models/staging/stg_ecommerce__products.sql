WITH source AS (
	SELECT *

	FROM {{ source('thelook_ecommerce', 'products') }}
)

SELECT
	-- IDs
	id AS product_id,

	-- Other columns
	cost,
	retail_price,
	department

	{#- Unused columns:
		- distribution_center_id
		- inventory_item_id
		- category
		- brand
		- sku
		- name
	#}

FROM source
