WITH

-- Aggregate measures
order_item_measures AS (
    SELECT
        order_id,
        SUM(item_sale_price) AS total_sale_price,
        SUM(product_cost) AS total_cost,
        SUM(item_profit) AS total_profit,
        SUM(item_discount) AS total_discount,

        {# This is overkill, but a nice way to show how loops work with dbt Jinja templating #}
        {%- set departments = ['Men', 'Women'] -%}
        {%- for department_name in departments %}
        SUM(IF(product_department = '{{department_name}}', item_sale_price, 0)) AS total_sold_{{department_name.lower()}}swear{% if not loop.last %},{% endif -%}
        {% endfor %}

    FROM {{ ref('int_ecommerce__order_details') }}
    GROUP BY 1
),

-- Get distinct dimensions
order_dimensions AS (
    SELECT DISTINCT
        order_id,
        order_created_at,
        order_returned_at,
        order_delivered_at,
        order_shipped_at,
        order_status,
        has_order_been_returned,
        num_items_ordered

    FROM {{ ref('int_ecommerce__order_details') }}
)

SELECT
    od.order_id,
    od.order_created_at,
    od.order_returned_at,
    od.order_delivered_at,
    od.order_shipped_at,
    od.order_status,
    od.has_order_been_returned,
    od.num_items_ordered,
    om.total_sale_price,
    om.total_product_cost,
    om.total_profit,
    om.total_discount,

    -- Columns from our templated Jinja statement
    {%- for department_name in departments %}
    om.total_sold_{{department_name.lower()}}swear{% if not loop.last %},{% endif -%}
    {%- endfor %}

FROM order_dimensions AS od
LEFT JOIN order_item_measures AS om
    ON od.order_id = om.order_id
