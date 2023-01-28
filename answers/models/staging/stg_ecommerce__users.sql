WITH source AS (
    SELECT *

    FROM {{ source('thelook_ecommerce', 'users') }}
)

SELECT
    -- IDs
    id AS user_id,

    -- Timestamps
    created_at,

    -- Other columns
    CONCAT(first_name, ' ', last_name) AS full_name,
    email,
    age,
    gender,
    state,
    street_address,
    postal_code,
    city,
    country,
    latitude,
    longitude,
    traffic_source

FROM source
