{% test primary_key(model,column_name) %}
WITH validation as (
    SELECT 

    {{ column_name }} as primary_key,
    count(1) as occurance

    FROM {{ ref('stg_ecommerce__products')}}
    GROUP BY 1
)
SELECT ''
FROM validation
WHERE primary_key IS NULL OR occurance > 1

{% endtest %}