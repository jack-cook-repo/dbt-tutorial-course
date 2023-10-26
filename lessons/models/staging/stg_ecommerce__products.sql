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
    department,
    {# Adding new column compared to previous version v1 #}
    brand,

    {# category,
    name,
    sku,
    distribution_center_id #}

FROM source