{% test primary_key(model, column_name) %}

WITH validation AS (
    SELECT
        {{ column_name }} AS primary_key,
        count(1) as occurrences
    FROM {{ model }}
    GROUP BY 1
)

SELECT *

FROM validation
WHERE primary_key IS NULL
      OR occurrences > 1

{% endtest %}

-- {% test col_greater_than(model, column_name, value=0) %}
--     SELECT
--         column_name AS row_that_failed
--     FROM {{ model }}
--     WHERE NOT({{ column_name }} > {{ value }})
--
-- {% endtest %}