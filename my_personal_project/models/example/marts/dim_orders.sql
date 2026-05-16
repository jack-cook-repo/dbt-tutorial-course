WITH

-- Aggregate measures
order_item_measures AS (
	SELECT
		order_id,
		SUM(sale_price) AS total_sale_price,
		SUM(cost) AS total_product_cost,
		SUM(profit) AS total_profit,
		SUM(item_discount) AS total_discount

	FROM {{ ref('int_ecommerce__order_items_products') }}
	GROUP BY 1
)

SELECT
	od.order_id,
	od.created_at AS order_created_at,
	od.shipped_at AS order_shipped_at,
	od.delivered_at AS order_delivered_at,
	od.returned_at AS order_returned_at,
	od.status AS order_status,
	od.num_of_item,
	om.total_sale_price,
	om.total_product_cost,
	om.total_profit,
	om.total_discount,
	fo.first_order_created_at

FROM {{ ref('stg_ecommerce__orders') }} AS od
LEFT JOIN order_item_measures AS om
	ON od.order_id = om.order_id
LEFT JOIN {{ ref('int_ecommerce__first_order_created') }} AS fo
	ON od.user_id = fo.user_id