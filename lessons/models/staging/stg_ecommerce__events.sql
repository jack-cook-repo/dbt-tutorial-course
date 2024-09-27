{{ config(
	materialized='incremental',
	unique_key='event_id',
	on_schema_change='sync_all_columns',
	partition_by={
		"field": "created_at",
		"data_type": "timestamp",
		"granularity": "day"
	}
	)
}}

with source as (

	select *

	from {{ source('thelook_ecommerce','events') }}
)

select
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

from source

{% if is_incremental() %}

where created_at >= (select max(created_at) from {{ this }})

{% endif %}


