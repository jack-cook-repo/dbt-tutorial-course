WITH source AS (
	SELECT *

	FROM {{ source('thelook_ecommerce', 'products') }}
)

SELECT
	-- IDs
	id AS product_id,
	distribution_center_id,

	-- Other columns
	cost,
	category,
	name,
	brand,
	retail_price,
	department,
	sku

FROM source
