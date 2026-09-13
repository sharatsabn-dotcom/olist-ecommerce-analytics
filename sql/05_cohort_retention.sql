-- Cohort retention analysis: for each customer's first-purchase month (cohort),
-- counts how many customers remained active N months later.
-- Uses customer_unique_id (not customer_id) since Olist assigns a new customer_id per order.
WITH customer_orders AS (
    SELECT
        c.customer_unique_id,
        o.order_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS order_month,
        MIN(DATE_TRUNC('month', o.order_purchase_timestamp)) OVER (
            PARTITION BY c.customer_unique_id
        ) AS first_purchase_month
    FROM orders AS o
    INNER JOIN customers AS c
        ON o.customer_id = c.customer_id
    WHERE o.order_status = 'delivered'
),
cohort_data AS (
    SELECT
        customer_unique_id,
        first_purchase_month,
        EXTRACT(YEAR FROM AGE(order_month, first_purchase_month)) * 12
        + EXTRACT(MONTH FROM AGE(order_month, first_purchase_month)) AS months_since_first_purchase
    FROM customer_orders
)
SELECT
    first_purchase_month,
    months_since_first_purchase,
    COUNT(DISTINCT customer_unique_id) AS active_customers
FROM cohort_data
GROUP BY first_purchase_month, months_since_first_purchase
ORDER BY months_since_first_purchase;