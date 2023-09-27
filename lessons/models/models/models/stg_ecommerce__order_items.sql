WITH source AS (
        SELECT *

        FROM {{ source('thelook_ecommerce', 'order_items') }}
)

SELECT
        id AS order_item_id,
        order_id,
        user_id,
        product_id,
        inventory_item_id,
        status,
        created_at,
        shipped_at,
        delivered_at,
        returned_at,
        sale_price

FROM source
