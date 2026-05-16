{{ config(materialized='ephemeral') }}

-- Modelo efímero: fecha mínima de creación (primer pedido) por usuario
with orders as (
	select
		user_id,
		created_at
	from {{ ref('stg_ecommerce__orders') }}
	where user_id is not null
)

select
	user_id,
	min(created_at) as first_order_created_at
from orders
group by user_id