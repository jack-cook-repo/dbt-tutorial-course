{% macro get_brand_name() %}
	CREATE OR REPLACE FUNCTION {{ target.schema }}.get_brand_name(web_link STRING)
	RETURNS STRING
	AS (
		REGEXP_EXTRACT(web_link, r'.+/brand/(.+)')
	)
{% endmacro %}