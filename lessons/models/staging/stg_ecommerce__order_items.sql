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

    {# Unused columns
    inventory_item_id,
    status,
    created_at,
    shipped_at,
    delivered_at,
    returned_at,
    #}

    -- Other columns
    sale_price AS item_sale_price

FROM source