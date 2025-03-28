{%- macro is_weekend(column_name) -%}
    EXTRACT(DAYOFWEEK FROM DATE({{ column_name }})) IN (1, 7)
{%- endmacro -%}