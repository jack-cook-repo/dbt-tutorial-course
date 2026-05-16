/*
	Original source code from dbt that I've edited for this course
	https://github.com/dbt-labs/dbt-codegen/blob/0.9.0/macros/generate_base_model.sql
*/

{% macro generate_base_model(source_name, table_name, case_sensitive_cols=False, materialized=None) %}

{%- set source_relation = source(source_name, table_name) -%}

{%- set columns = adapter.get_columns_in_relation(source_relation) -%}
{% set column_names=columns | map(attribute='name') %}
{% set base_model_sql %}

{%- if materialized is not none -%}
	{{ "{{ config(materialized='" ~ materialized ~ "') }}" }}
{%- endif %}

WITH source AS (
	SELECT *

	FROM {% raw %}{{ source({% endraw %}'{{ source_name }}', '{{ table_name }}'{% raw %}) }}{% endraw %}
)

SELECT
{%- for column in column_names %}
	{%- if column == 'id' -%}
	{# Takes the table name, strips the last letter to make it singular (e.g orders --> order)
	   and appends "_id" to create a primary key that matches the name of foreign keys #}
	id AS {{ table_name[:-1] }}_id{{"," if not loop.last}}
	{%- else -%}
	{# Otherwise, just takes the column name #}
	{{ column }}{{"," if not loop.last}}
	{%- endif -%}
{%- endfor %}

FROM source

{% endset %}

{% if execute %}

{{ log(base_model_sql, info=True) }}
{% do return(base_model_sql) %}

{% endif %}
{% endmacro %}