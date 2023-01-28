WITH source AS (
    SELECT *

    FROM {{ source('thelook_ecommerce', 'inventory_items') }}
)

SELECT
    -- IDs
    id AS inventory_item_id,
    product_id,
    product_distribution_center_id,

    -- Timestamps
    created_at,
    sold_at,

    -- Other columns
    cost,
    product_category,
    product_name,
    product_brand,
    product_retail_price,
    product_department,
    product_sku

FROM source
