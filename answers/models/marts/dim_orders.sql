WITH

-- Aggregate measures
order_item_measures AS (
    SELECT
        order_id,
        SUM(item_sale_price) AS total_sale_price,
        SUM(product_cost) AS total_product_cost,
        SUM(item_sale_price - product_cost) AS total_profit,
        SUM(product_retail_price - item_sale_price) AS total_discount

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
    om.total_discount

FROM order_dimensions AS od
LEFT JOIN order_item_measures AS om
    ON od.order_id = om.order_id
