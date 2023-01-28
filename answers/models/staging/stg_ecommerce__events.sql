WITH source AS (
    SELECT *

    FROM {{ source('thelook_ecommerce', 'events') }}
)

SELECT
    -- IDs
    id AS event_id,
    user_id,
    session_id,

    -- Timestamps
    created_at,

    -- Other columns
    sequence_number,
    ip_address,
    city,
    state,
    postal_code,
    browser,
    traffic_source,
    uri,
    event_type

FROM source
