{# This is a generic test combining both unique and not_null generic tests in one#}

{% test primary_key(model, column_name) %}

with validation as(
	select
		{{ column_name }} as primary_key,
		count(1) as occurences
	from {{ model }}
	group by 1
)

	select *
	from validation
	where primary_key is null
		or occurences > 1

{% endtest %}