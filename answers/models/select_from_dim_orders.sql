{{
  config(
		group='sales'
	)
}}

SELECT * FROM {{ ref('dim_orders') }}