{#
	This test is basically a "not_null" and "unique"
	rolled into one.

	It fails if a column is NULL or occurs more than once
#}

{% test primary_key(model, column_name) %}

WITH validations AS (
	SELECT
		{{ column_name }} AS primary_key,
		COUNT(1) AS occurrences

	FROM {{ model }}
	GROUP BY 1
)

SELECT *

FROM validations
WHERE primary_key IS NULL
	OR occurrences > 1

{% endtest %}


{% test col_greater_than(model, column_name, value=0) %}
	Select {{ column_name }} as row_that_failed
	from {{ model }}
	where NOT {{ column_name }} > {{value}}

{% endtest %}
