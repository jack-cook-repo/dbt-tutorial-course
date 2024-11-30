{{
    config(
        materialized='incremental',
        unique_key='event_id',
        on_schema_change='sync_all_columns'
    )
}}

WITH source AS (
    SELECT *

    FROM {{ source('thelook_ecommerce', 'events') }}
    WHERE created_at <= '2023-01-01'
)

SELECT
    id AS event_id,
	user_id,
	sequence_number,
	session_id,
	created_at,
	ip_address,
	city,
	state,
	postal_code,
	browser,
	traffic_source,
	uri AS web_link,
	event_type

FROM source

{% if is_incremental() %}

where created_at > (SELECT MAX(created_at) FROM {{ this }})

{% endif %}