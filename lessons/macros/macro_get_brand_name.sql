{#
	Creates a function in the target schema that can be used to extract the brand name
	from the events table web link column.

	For those not familiar with regex (regular expressions), they are basically a very powerful
	way to search within strings for any pattern of letters/numbers etc.

	In this example, we extract everything after /brand/ as all of the relevantweb links end
	with the brand name.

	e.g., take this web link: "/department/men/category/active/brand/columbia"
	Our regex match pattern, ".+/brand/(.+)", does the following:
	- ".+" matches ANYTHING 1 or more times. By itself, it would return the whole string!
	- "/brand/" matches exactly that in the web link.
		If we used ".+/brand/" as our match pattern, it would return "/department/men/category/active/brand/"
	- "(.+)" does 2 things:
		1. The brackets denote that this is the part we want to return
		2. ".+" will, again, match ANYTHING after "brand/"
#}
{% macro get_brand_name() %}
	CREATE OR REPLACE FUNCTION {{ target.schema }}.get_brand_name(web_link STRING)
	RETURNS STRING
	AS (
		REGEXP_EXTRACT(web_link, r'.+/brand/(.+)')
	)
{% endmacro %}