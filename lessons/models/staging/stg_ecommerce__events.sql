{{
     config(
       materialized = 'incremental',
       unique_key = 'event_id',
       on_schema_change = 'sync_all_columns'
       )
}}
WITH source AS (
    SELECT *
    FROM {{ source('thelook_ecommerce', 'events') }} 
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
{# Only runs this filter on an incremental run #}
{% if is_incremental() %}

{# The {{ this }} macro is essentially a {{ ref('') }} macro that allows for a circular reference #}
{# WHERE created_at > (SELECT MAX(created_at) FROM {{ this }}) #}
 WHERE created_at between "{{ var("min_date") }}" and "{{ var("max_date") }}" 

{% endif %}

