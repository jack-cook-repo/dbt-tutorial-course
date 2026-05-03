{# Get all columns in a table #}
{% set columns = adapter.get_columns_in_relation(ref('orders')) %}

{# Get all columns in a table, check they start with 'total' #}
SELECT
{% for column in columns -%}
	{%- if column.name.startswith('total') %}
	{{ column.name.upper() }},
	{%- endif -%}
{%- endfor %}


{# Get all values from a column in a table #}
{% set values = dbt_utils.get_column_values(ref('orders'), 'order_status') %}

{{ values }}