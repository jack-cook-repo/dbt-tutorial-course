A macro is a reusable piece of logic (a function). In this dbt project we use 3 different types:

1. Macros we use in SQL models:
	- An example of this is macro_is_weekend.sql
	- This takes a date and checks if it is a Saturday or a Sunday, and returns TRUE if so or FALSE if not
	- It's used within a SQL file (we use it in dim_orders.sql)
	- These types of macro are great for defining reusable SQL functions to use across multiple models

2. Macros we run before/after our dbt runs:
	- These are called "hooks" https://docs.getdbt.com/docs/build/hooks-operations#about-hooks
	- These can be run before/after a model, or before/after an entire dbt run/test/snapshot
	- An example of this is macro_get_brand_name.sql
	- In this file we define a SQL UDF (User Defined Function) that gets saved into our BigQuery schema
	- In theory, we could have just created a regular SQL macro like macro_is_weekend.sql, but with UDFs
	  you can also write JavaScript functions
	- Hooks are most useful for defining UDFs or granting table permissions after creating a table

3. An "operation":
	- An example of this is macro_generate_base_table.sql. It overrides the default dbt macro for
	  generated_base_table() provided by dbt
	- These are typically run via the terminal by `dbt run-operation macro_name arguments`
	- For example, we'd run `dbt run-operation generate_base_model --args '{"source_name": "thelook_ecommerce",  "table_name": "products"}'`, which would return the SQL for stg_ecommerce__products
	- You can put these macros within dbt SQL files and get the same output, but it makes more sense to run
	  it in the terminal
