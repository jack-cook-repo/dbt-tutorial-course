/*
    Checks that, for any order, that the details associated with the order items match the details of the
    order. For example - we check that the number of items line up, the user_ids line up, everything is
    shipped at the same time etc.

    Returns all of the rows where we don't get a match, meaning one of the checks has failed.

    Note that one column we don't compare is the created_at column, because items in an order can
    be created before the order itself, and can be added to the basket at different times.
*/

WITH order_details AS (
    SELECT
        order_id,
        COUNT(*) AS num_of_items,
        MIN(user_id) AS user_id,
        COUNT(DISTINCT user_id) AS num_of_users,
        MIN(shipped_at) AS min_order_shipped_at,
        COUNT(DISTINCT shipped_at) AS num_of_shipped_at_timestamps,
        MIN(delivered_at) AS min_order_delivered_at,
        COUNT(DISTINCT delivered_at) AS num_of_delivered_at_timestamps,
        MIN(status) AS min_status,
        COUNT(DISTINCT status) AS order_item_statuses

    FROM {{ ref('stg_ecommerce__order_items') }}
    GROUP BY 1
)

SELECT
    o.*,
    od.*

FROM {{ ref('stg_ecommerce__orders') }} AS o
FULL OUTER JOIN order_details AS od USING(order_id)
WHERE
    -- All orders should have at least 1 item, and every item should tie to an order
    o.order_id IS NULL
    OR od.order_id IS NULL
    -- Number of items doesn't match
    OR o.num_of_item != od.num_of_items
    -- user_id in order item doesn't match order user_id, and/or >1 user is associated with an order
    OR o.user_id != od.user_id
    OR od.num_of_users > 1
    -- shipped_at in order item doesn't match order shipped_at, and/or >1 shipped_at is associated with an order
    OR o.shipped_at != od.min_order_shipped_at
    OR od.num_of_shipped_at_timestamps > 1
    -- delivered_at in order item doesn't match order shipped_at, and/or >1 delivered_at is associated with an order
    OR o.delivered_at != od.min_order_delivered_at
    OR od.num_of_delivered_at_timestamps > 1
    -- status in order item doesn't match order status, and/or >1 status is associated with an order
    OR o.status != od.min_status
    OR od.order_item_statuses > 1
