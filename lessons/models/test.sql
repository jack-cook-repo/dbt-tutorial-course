{#
This comment will not be avialable 
#}

-- this is just a stadatrt commment
{% set my_variable -%}
    SELECT 1 as my_col
{%- endset %}

{{ my_variable }}

{% set my_list = ['test1','test2','test3'] %}
