{{config(
	materialized='ephemeral'
	)
}}

select
		user_id,
		min(created_at) as first_order_created_at

	from {{ ref('stg_ecommerce__orders') }}

	group by 1