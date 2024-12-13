WITH source AS (
        SELECT *

        FROM {{ source('thelook_ecommerce', 'orders') }}
)

SELECT
        -- IDs
        order_id,
        user_id,

        -- Timestamps
        status,
        created_at,
        returned_at,
        shipped_at,
        delivered_at,

        -- Other columnns
        status,
        num_of_item AS num_of_items_ordered

FROM source