WITH source AS (
        SELECT *

        FROM {{ source('thelook_ecommerce', 'users') }}
)

SELECT
        id AS user_id,
        first_name,
        last_name,
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
        traffic_source,
        created_at

FROM source