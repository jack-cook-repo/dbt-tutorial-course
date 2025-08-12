{%- macro day_check(column) -%}

extract(day from date({{column}})) as day_type

{%- endmacro -%}