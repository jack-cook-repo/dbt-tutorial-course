-- BigQuery is weird and has weeks starting from Sunday, so Sunday is 1 and Saturday is 7
{%- macro is_weekend(date_column) -%}
	EXTRACT(DAYOFWEEK FROM DATE({{ date_column }})) IN (1, 7)
{%- endmacro -%}