{#
    comment that won't appear in the compiled SQL
#}

{% set my_log_variable %}
    select 1 as my_col
{% endset %}

{{ my_log_variable }}

{% set my_list = ['user_id', 'created_at'] %}

select
{% for item in my_list %}
    {{ my_list }}{% if not loop.last %},{% endif %}
{% endfor %}