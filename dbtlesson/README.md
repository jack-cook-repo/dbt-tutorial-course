Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test


### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices

## test

## doc files
create document folder and md file which has descriptions of the variable which can be used in yaml.
check [here](models/documents/ecommerce). Run the model and check the schema description in BQ.
Markdown (.md) documents are a great way to store reusable descriptions for your dbt project, and to use more advanced formatting such as bullet point lists.

## seed file
Should be csv file and add a yaml file defining details of the csv data. Run with dbt seed. A table will be created in the project check [here](./seeds)
Seeds are stored in your own schema that you specify in your profiles.yml file (e.g. dbt_jack), and are only created/updated by the dbt seed command, not by dbt run!

However, seeds are tested if you do dbt test.

## snapshots
Creates a table in a separate dataset dbt_snapshots. check [here](./snapshots).Snapshots are SQL queries run against a table in your database that then track any changes to the underlying data. The queries are run using dbt snapshot.

They write to a centrally stored table (i.e. running dbt snapshot will always write to the same place regardless of what your profiles.yml is set to).

There are 2 main strategies for snapshots:

check: Given a unique_key, checks whether the values in check_cols have changed, and if so, writes a new row into the table
timestamp: Given a unique_key, and an updated_at timestamp, checks whether the timestamp has changed, and if so, writes a new row into the table
Snapshots are only as good as the saved table. If you had a table dbt_snapshots.snapshot__distribution_centers that had been tracking changes to distribution centers for 6 months, but then the table was deleted, the next dbt snapshot would just create a brand new table.

## Materialization
Ephemeral
For quick running SQL that’s not worth materialising

View
Doesn’t store data. Faster to run, longer to query

Table
Stores data. Longer to run, faster to query

Incremental
Table appended/merged with new data, rather than drop & replace

## Jinja
There are 3 types of Jinja notation you’ll need to be familiar with:

{# #} single or multiline comments, won’t show up in your compiled SQL
{{ }} expressions, these are effectively variables that will be replaced with whatever is defined in the contents of the expression when the SQL is compiled
{% %} statements, these are effectively functions - and including things like do / if / for / set / macro / test etc. which won’t be in the compiled SQL but can write outputs into the SQL itself

## Macros
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

## functions

Things to watch out for:

Within a jinja statement ({% %}) or expression ({{ }}), as in inside the { } brackets themselves, anything without quotes jinja will assume is a variable
For example, {{ is_weekend(created_at) }} would assume that created_at was a variable that we’d already defined via {% set created_at = X %}
As a result, for macros that you’re using in a SQL file you’ll want to put things in quote marks to make sure it is handled properly - e.g. {{ is_weekend('od.created_at') }} - you can use single or double quotes
This is a good explanation from dbt themselves on why you need to quote column names
Also, when you’re within a jinja statement set of brackets, don’t try to put an expression within it! e.g. {% set my_thing = {{ my_variable }} %}, the above article links out to this page which has a good explanation as to why