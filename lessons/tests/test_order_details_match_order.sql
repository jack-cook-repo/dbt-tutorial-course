with order_items as (

	select
		order_id,
		count(*) as num_of_items_in_order
	from {{ ref('stg_ecommerce__order_items') }}
	group by 1
),

final as (
	select
		oi.*,
		o.*
	from order_items oi
	full outer join `light-relic-399507`.`dbt_muspenski`.`stg_ecommerce__orders` o
		on o.order_id = oi.order_id
	where o.order_id is null or
		oi.order_id is null or
		oi.num_of_items_in_order != o.num_of_item

)

select * from final