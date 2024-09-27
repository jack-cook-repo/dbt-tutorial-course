WITH source AS (
        SELECT *

        FROM {{ source('thelook_ecommerce', 'products') }}
)

SELECT
        id AS product_id,
        cost,
        brand,
        retail_price,
        department

			{#- Unused columns:
		- inventory_item_id
		- distribution_center_id
		- category
		- sku
		- name
	#}

FROM source