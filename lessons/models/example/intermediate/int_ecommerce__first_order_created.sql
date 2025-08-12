{#
	Ephemeral models are basically CTEs (Common Table Expressions, or "with" statements).
	They aren't materialised as tables/views, but instead when you ref('') an ephemeral model
	it generates the SQL within the script itself.

	Ephemeral models are usually only used when you have a small, fast running piece of SQL
	that you want to reuse across multiple SQL files downstream.

	Typically, you'll use the following progression of materialisation:
	- Ephemeral: quick to run, basically a reusable SQL snippet
	- View: quick to run, but useful to be able to run the view in your database / data vis tool to look at the output
		without manually copy / pasting the SQL
	- Table: typically when you have models that take longer to run and are used in multiple downstream
		models - or when you'd like to quickly scan the output in your database / data vis tool without needing to run
		the SQL again. Tables are the most common type of materialisation as there's usually not too much processing time
		needed to write the SQL to a table once a query has run, but it's faster to SELECT * a table than
		to run a view
	- Incremental: when your table models start getting very slow when you are doing a drop & replace
#}
{{
	config(materialized='ephemeral')
}}


SELECT
	user_id,
	MIN(created_at) AS first_order_created_at

FROM {{ ref('stg_ecommerce__orders') }}
GROUP BY 1
